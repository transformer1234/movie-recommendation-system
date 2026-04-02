def recommend(movie: str, df, similarity, n: int = 8):
    """Return top-n recommended movie titles + their movie_ids."""
    titles_lower = df["title"].str.lower()
    matches = df[titles_lower == movie.lower()]

    if matches.empty:
        return []

    idx = matches.index[0]
    distances = list(enumerate(similarity[idx]))
    distances = sorted(distances, key=lambda x: x[1], reverse=True)

    results = []
    for i, score in distances[1 : n + 1]:
        row = df.iloc[i]
        results.append({
            "title": row["title"],
            "movie_id": int(row["movie_id"]),
            "score": round(float(score), 4),
        })
    return results