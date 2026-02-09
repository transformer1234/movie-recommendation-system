def recommend(movie, df, similarity):
    movie = movie.lower()
    if movie not in df['title'].str.lower().values:
        print("Movie not found in database.")
        return
    
    # get index of the movie
    idx = df[df['title'].str.lower() == movie].index[0]
    
    # get list of similarity scores
    distances = similarity[idx]
    
    # sort the movies based on similarity in descending order
    movies_list = sorted(
        list(enumerate(distances)), 
        reverse=True, 
        key=lambda x: x[1]
    )
    
    # print top 5 recommended movies (skip the first one: itself)
    recommended = [df.iloc[i[0]].title for i in movies_list[1:6]]
    return recommended