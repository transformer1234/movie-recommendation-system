import pandas as pd
import os
import ast

def preprocess():
    """
    Loads TMDB movies and credits dataset.
    Expected file structure:
    data/movies.csv
    data/credits.csv
    """

    movies_path = "../data/tmdb_5000_movies.csv"
    credits_path = "../data/tmdb_5000_credits.csv"

    if not os.path.exists(movies_path) or not os.path.exists(credits_path):
        raise FileNotFoundError("Movies or Credits file missing in data/ folder")

    movies_df = pd.read_csv(movies_path)
    credits_df = pd.read_csv(credits_path)

    df = movies_df.merge(credits_df, on="title")
    df.head()

    df = df[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]
    df.head()

    df['genres'] = df['genres'].apply(convert)
    df['keywords'] = df['keywords'].apply(convert)

    df['cast'] = df['cast'].apply(convert_cast)

    df['crew'] = df['crew'].apply(fetch_director)

    df['overview'] = df['overview'].astype(str).apply(lambda x: x.split())

    df['genres'] = df['genres'].apply(lambda x: [i.replace(" ", "") for i in x])
    df['keywords'] = df['keywords'].apply(lambda x: [i.replace(" ", "") for i in x])
    df['cast'] = df['cast'].apply(lambda x: [i.replace(" ", "") for i in x])
    df['crew'] = df['crew'].apply(lambda x: [i.replace(" ", "") for i in x])

    print("Data loaded successfully:")
    print("Movies shape:", movies_df.shape)
    print("Credits shape:", credits_df.shape)
    print("Merged shape:", df.shape)

    return df

def convert(obj):
    L = []
    for item in ast.literal_eval(obj):
        L.append(item['name'])
    return L

def convert_cast(obj):
    L = []
    for i, item in enumerate(ast.literal_eval(obj)):
        if i < 3:
            L.append(item['name'])
    return L

def fetch_director(obj):
    for item in ast.literal_eval(obj):
        if item['job'] == 'Director':
            return [item['name']]
    return []

if __name__ == "__main__":
    df = preprocess()
    df.head()