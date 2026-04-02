# 🎬 Movie Recommendation System

Content-based movie recommender using TF-IDF + cosine similarity on the TMDB 5000 dataset, with poster images fetched live from the TMDB API.

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Add the TMDB datasets
Download from Kaggle ([TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)) and place in `data/`:
```
data/
├── tmdb_5000_movies.csv
└── tmdb_5000_credits.csv
```

### 3. Build the model (run once)
```bash
python src/model.py
```
This generates `data/movies.pkl` and `data/similarity.pkl`. Commit both files to your repo.

### 4. Add your TMDB API key
Create `.streamlit/secrets.toml`:
```toml
TMDB_API_KEY = "your_key_here"
```
Get a free key at https://www.themoviedb.org/settings/api

### 5. Run locally
```bash
python -m streamlit run app.py
```

## Deploy to Streamlit Cloud

1. Push the repo to GitHub (including `data/movies.pkl` and `data/similarity.pkl`)
2. Connect the repo on [share.streamlit.io](https://share.streamlit.io)
3. Set **Main file path** to `app.py`
4. Under **Advanced settings → Secrets**, add:
   ```toml
   TMDB_API_KEY = "your_key_here"
   ```
5. Deploy 🚀

Deployed at https://mt-movie-recommendation-system.streamlit.app/

> The app works without a TMDB API key — posters just won't load.