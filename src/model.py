from preprocess import preprocess
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

if __name__ == "__main__":
    df = preprocess()
    df['tags'] = df['overview'] + df['genres'] + df['keywords'] + df['cast'] + df['crew']
    df['tags'] = df['tags'].apply(lambda x: " ".join(x))
    df['tags'] = df['tags'].apply(lambda x: x.lower())
    df = df[['movie_id','title','tags']]
    
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vector = cv.fit_transform(df['tags']).toarray()
    
    similarity = cosine_similarity(vector)

    with open('../data/movies.pkl', 'wb') as f:
        pickle.dump(df, f)

    with open('../data/similarity.pkl', 'wb') as f:
        pickle.dump(similarity, f)

    with open('../data/cv.pkl', 'wb') as f:
        pickle.dump(cv, f)

    