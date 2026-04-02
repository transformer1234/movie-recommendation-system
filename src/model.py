"""
Run this once to generate data/movies.pkl and data/similarity.pkl.
Place tmdb_5000_movies.csv and tmdb_5000_credits.csv in data/ first.

Usage (from project root):
    python src/model.py
"""

import os
import sys
import pickle

# Ensure imports work from project root
sys.path.insert(0, os.path.dirname(__file__))

from preprocess import preprocess
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def build_model():
    df = preprocess(data_dir=DATA_DIR)

    df["tags"] = df["overview"] + df["genres"] + df["keywords"] + df["cast"] + df["crew"]
    df["tags"] = df["tags"].apply(lambda x: " ".join(x))
    df["tags"] = df["tags"].apply(lambda x: x.lower())
    df = df[["movie_id", "title", "tags"]]

    cv = CountVectorizer(max_features=5000, stop_words="english")
    vector = cv.fit_transform(df["tags"]).toarray()
    similarity = cosine_similarity(vector)

    os.makedirs(DATA_DIR, exist_ok=True)

    with open(os.path.join(DATA_DIR, "movies.pkl"), "wb") as f:
        pickle.dump(df, f)

    with open(os.path.join(DATA_DIR, "similarity.pkl"), "wb") as f:
        pickle.dump(similarity, f)

    print(f"✅ Saved movies.pkl ({len(df)} movies) and similarity.pkl to {DATA_DIR}")
    return df, similarity


if __name__ == "__main__":
    build_model()