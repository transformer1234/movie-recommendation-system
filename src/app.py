import pickle
import streamlit as st
from recommend import recommend

df = pickle.load(open('../data/movies.pkl', 'rb'))
similarity = pickle.load(open('../data/similarity.pkl', 'rb'))

st.title("🎬 Movie Recommendation System")

# Dropdown with all movie titles
selected_movie = st.selectbox("Select a movie:", df['title'].values)

if st.button("Show Recommendations"):
    recommendations = recommend(selected_movie, df, similarity)
    st.subheader("Top 5 Recommended Movies:")
    for i, movie in enumerate(recommendations):
        st.write(f"{i+1}. {movie}")