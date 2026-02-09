# 🎬 Movie Recommendation System

A machine learning–based movie recommendation system that suggests movies to users based on similarity between movie features.

## 🔍 Project Overview
This project implements a content-based movie recommender using cosine similarity. Movie metadata is processed and transformed into feature vectors to identify similar movies.

## ⚙️ Tech Stack
- Python
- Pandas, NumPy
- Scikit-learn
- NLP (CountVectorizer)
- Streamlit (UI)

## 🧠 Recommendation Approach
- Text feature extraction from movie metadata
- Vectorization using CountVectorizer
- Similarity computation using cosine similarity
- Top-N movie recommendations

## ▶️ How to Run
```bash
pip install -r requirements.txt
cd src
streamlit run app.py