# ==========================================
# 🎬 IMDb Movie Recommendation Streamlit App
# ==========================================

import streamlit as st
import pandas as pd
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ==========================================
# 📌 PAGE CONFIGURATION
# ==========================================

st.set_page_config(page_title="Movie Recommender", layout="wide")


st.title("🎬 IMDb Movie Recommendation System")
st.write("Enter a movie storyline and get top 5 similar movie recommendations!")


# ==========================================
# 📌 LOAD DATA
# ==========================================

@st.cache_data
def load_data():
    df = pd.read_csv("imdb_2024_movies.csv")
    df = df[['Movie Name', 'Storyline']]   # Keep only needed columns
    return df

df = load_data()


# ==========================================
# 📌 TEXT CLEANING FUNCTION
# ==========================================

def clean_text(text):
    text = str(text)
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text


df['cleaned_story'] = df['Storyline'].apply(clean_text)


# ==========================================
# 📌 TF-IDF VECTORIZATION
# ==========================================

vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(df['cleaned_story'])


# ==========================================
# 📌 USER INPUT
# ==========================================

user_input = st.text_area("✍️ Enter Movie Storyline Here:", height=150)


# ==========================================
# 📌 RECOMMENDATION FUNCTION
# ==========================================

def recommend_from_story(user_story, top_n=5):
    
    # Clean user input
    cleaned_input = clean_text(user_story)
    
    # Convert input into TF-IDF vector
    user_vector = vectorizer.transform([cleaned_input])
    
    # Compute cosine similarity with dataset
    similarity_scores = cosine_similarity(user_vector, tfidf_matrix)
    
    # Get top movie indices
    similarity_scores = list(enumerate(similarity_scores[0]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    
    top_movies = similarity_scores[:top_n]
    
    return top_movies


# ==========================================
# 📌 DISPLAY RESULTS
# ==========================================

if st.button("🔍 Get Recommendations"):
    
    if user_input.strip() == "":
        st.warning("Please enter a storyline first!")
    
    else:
        recommendations = recommend_from_story(user_input, top_n=5)
        
        st.subheader("🎯 Top 5 Recommended Movies")
        
        for idx, score in recommendations:
            
            st.markdown("---")
            st.markdown(f"### 🎥 {df['Movie Name'][idx]}")
            st.write(df['Storyline'][idx])
            st.write(f"Similarity Score: {round(score, 3)}")