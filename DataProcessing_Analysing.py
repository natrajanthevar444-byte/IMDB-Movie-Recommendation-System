# ==========================================
# 📌 STEP 1: Import Required Libraries
# ==========================================

import pandas as pd
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ==========================================
# 📌 STEP 2: Load the Dataset
# ==========================================

df = pd.read_csv("imdb_2024_movies.csv")

print("Dataset Loaded Successfully ✅")
print(df.head())


# ==========================================
# 📌 STEP 3: Basic Text Cleaning Function
# ==========================================

def clean_text(text):
    """
    This function:
    1. Converts text to lowercase
    2. Removes punctuation
    3. Returns cleaned text
    """
    
    # Convert to string (important if there are missing values)
    text = str(text)
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    return text


# Apply cleaning to Storyline column
df['cleaned_story'] = df['Storyline'].apply(clean_text)

print("Text Cleaning Completed ✅")


# ==========================================
# 📌 STEP 4: Convert Text to Numerical Vectors (TF-IDF)
# ==========================================

"""
TF-IDF:
Gives importance to important words
Removes common English stopwords automatically
"""

vectorizer = TfidfVectorizer(stop_words='english')

tfidf_matrix = vectorizer.fit_transform(df['cleaned_story'])

print("TF-IDF Vectorization Completed ✅")


# ==========================================
# 📌 STEP 5: Calculate Cosine Similarity
# ==========================================

cosine_sim = cosine_similarity(tfidf_matrix)

print("Cosine Similarity Matrix Created ✅")


# ==========================================
# 📌 STEP 6: Movie Recommendation Function
# ==========================================

def recommend_movies(movie_name, top_n=5):

    movie_name = movie_name.lower().strip()

    df['lower_name'] = df['Movie Name'].str.lower().str.strip()

    if movie_name not in df['lower_name'].values:
        return "Movie not found in dataset!"

    movie_index = df[df['lower_name'] == movie_name].index[0]

    similarity_scores = list(enumerate(cosine_sim[movie_index]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    similarity_scores = similarity_scores[1:top_n+1]

    movie_indices = [i[0] for i in similarity_scores]

    return df['Movie Name'].iloc[movie_indices]

# ==========================================
# 📌 STEP 7: Test the Recommendation System
# ==========================================

print("\nRecommended Movies:")
print(recommend_movies("Trap", top_n=5))