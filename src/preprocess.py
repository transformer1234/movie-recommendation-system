import os
import ast
import pandas as pd


def preprocess(data_dir: str = "../data"):
    movies_path = os.path.join(data_dir, "tmdb_5000_movies.csv")
    credits_path = os.path.join(data_dir, "tmdb_5000_credits.csv")

    if not os.path.exists(movies_path) or not os.path.exists(credits_path):
        raise FileNotFoundError(
            f"Missing CSVs in {data_dir}. "
            "Download tmdb_5000_movies.csv and tmdb_5000_credits.csv from Kaggle."
        )

    movies_df = pd.read_csv(movies_path)
    credits_df = pd.read_csv(credits_path)

    df = movies_df.merge(credits_df, on="title")
    df = df[["movie_id", "title", "overview", "genres", "keywords", "cast", "crew"]]
    df = df.dropna(subset=["overview"])

    df["genres"] = df["genres"].apply(convert)
    df["keywords"] = df["keywords"].apply(convert)
    df["cast"] = df["cast"].apply(convert_cast)
    df["crew"] = df["crew"].apply(fetch_director)
    df["overview"] = df["overview"].astype(str).apply(lambda x: x.split())

    for col in ["genres", "keywords", "cast", "crew"]:
        df[col] = df[col].apply(lambda x: [i.replace(" ", "") for i in x])

    print(f"Preprocessed {len(df)} movies.")
    return df


def convert(obj):
    return [item["name"] for item in ast.literal_eval(obj)]


def convert_cast(obj):
    return [item["name"] for i, item in enumerate(ast.literal_eval(obj)) if i < 3]


def fetch_director(obj):
    for item in ast.literal_eval(obj):
        if item["job"] == "Director":
            return [item["name"]]
    return []


if __name__ == "__main__":
    df = preprocess()
    print(df.head())