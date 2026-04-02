import os
import sys
import pickle
import requests
import streamlit as st

# ── Path setup ──────────────────────────────────────────────────────────────
ROOT = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(ROOT, "src"))

from recommend import recommend  # noqa: E402

# ── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide",
)

# ── Styling ──────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    .movie-card {
        background: #1a1a2e;
        border-radius: 12px;
        padding: 0;
        overflow: hidden;
        text-align: center;
        transition: transform 0.2s;
        height: 100%;
    }
    .movie-card img {
        width: 100%;
        border-radius: 12px 12px 0 0;
    }
    .movie-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: #f0f0f0;
        padding: 8px 6px 2px 6px;
    }
    .movie-score {
        font-size: 0.75rem;
        color: #a0a0b0;
        padding-bottom: 8px;
    }
    .stSelectbox > div > div { font-size: 1rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Load data ────────────────────────────────────────────────────────────────
DATA_DIR = os.path.join(ROOT, "data")

@st.cache_resource(show_spinner="Loading model…")
def load_data():
    movies_path = os.path.join(DATA_DIR, "movies.pkl")
    similarity_path = os.path.join(DATA_DIR, "similarity.pkl")

    if not os.path.exists(movies_path) or not os.path.exists(similarity_path):
        st.error(
            "❌ `data/movies.pkl` or `data/similarity.pkl` not found. "
            "Run `python src/model.py` first to generate them."
        )
        st.stop()

    with open(movies_path, "rb") as f:
        df = pickle.load(f)
    with open(similarity_path, "rb") as f:
        similarity = pickle.load(f)
    return df, similarity


df, similarity = load_data()

# ── TMDB helpers ─────────────────────────────────────────────────────────────
TMDB_API_KEY = st.secrets.get("TMDB_API_KEY", "")
PLACEHOLDER = "https://via.placeholder.com/300x450?text=No+Poster"


@st.cache_data(ttl=86400, show_spinner=False)
def fetch_movie_details(movie_id: int):
    """Return poster URL + vote_average + genre list from TMDB."""
    if not TMDB_API_KEY:
        return PLACEHOLDER, None, []

    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}"
        r = requests.get(url, params={"api_key": TMDB_API_KEY}, timeout=5)
        r.raise_for_status()
        data = r.json()

        poster = (
            f"https://image.tmdb.org/t/p/w342{data['poster_path']}"
            if data.get("poster_path")
            else PLACEHOLDER
        )
        rating = round(data.get("vote_average", 0), 1)
        genres = [g["name"] for g in data.get("genres", [])][:3]
        return poster, rating, genres
    except Exception:
        return PLACEHOLDER, None, []


# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("## 🎬 Movie Recommendation System")
st.caption("Content-based filtering · TMDB 5000 dataset · Cosine similarity")
st.divider()

# ── Movie selector ───────────────────────────────────────────────────────────
all_titles = sorted(df["title"].values)

col_search, col_btn = st.columns([4, 1], vertical_alignment="bottom")
with col_search:
    selected_movie = st.selectbox(
        "Search for a movie:",
        options=all_titles,
        index=None,
        placeholder="Type a movie title…",
    )
with col_btn:
    search_clicked = st.button("Recommend 🎯", type="primary", use_container_width=True)

# ── Show selected movie card ──────────────────────────────────────────────────
if selected_movie:
    row = df[df["title"] == selected_movie].iloc[0]
    poster, rating, genres = fetch_movie_details(int(row["movie_id"]))

    with st.container():
        c1, c2 = st.columns([1, 4])
        with c1:
            st.image(poster, width=140)
        with c2:
            st.markdown(f"### {selected_movie}")
            if rating:
                st.markdown(f"⭐ **{rating}/10**")
            if genres:
                st.markdown(" · ".join(f"`{g}`" for g in genres))

    st.divider()

# ── Recommendations ───────────────────────────────────────────────────────────
if search_clicked and selected_movie:
    results = recommend(selected_movie, df, similarity, n=8)

    if not results:
        st.warning("Movie not found in database.")
    else:
        st.markdown("### Recommended for you")

        cols = st.columns(4)
        for i, movie in enumerate(results):
            poster, rating, genres = fetch_movie_details(movie["movie_id"])
            with cols[i % 4]:
                rating_str = f"⭐ {rating}" if rating else ""
                genre_str = " · ".join(genres) if genres else ""
                st.markdown(
                    f"""
                    <div class="movie-card">
                        <img src="{poster}" alt="{movie['title']}">
                        <div class="movie-title">{movie['title']}</div>
                        <div class="movie-score">{rating_str}{"  " if rating_str and genre_str else ""}{genre_str}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

elif search_clicked and not selected_movie:
    st.info("Please select a movie first.")