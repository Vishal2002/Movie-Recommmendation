import streamlit as st
import pandas as pd
import pickle
from tmdbv3api import TMDb, Movie
import os
from dotenv import load_dotenv, dotenv_values 
load_dotenv() 
 

print()

# Initialize TMDb
tmdb = TMDb()
tmdb.api_key = os.getenv("API_KEY")  # Replace with your TMDb API key
tmdb.language = 'en'
tmdb_movie = Movie()

# Function to get movie recommendations
def recommend(movie):
    recommendation = []
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    for i in movies_list:
        recommendation.append(movies_df.iloc[i[0]].title)
    return recommendation

# Function to fetch movie poster URL
def fetch_poster_url(movie_title):
    search_result = tmdb_movie.search(movie_title)
    if search_result:
        movie_id = search_result[0].id
        movie_details = tmdb_movie.details(movie_id)
        poster_path = movie_details.poster_path
        full_path = f"https://image.tmdb.org/t/p/w500{poster_path}"
        return full_path
    return None

# Load the movie data
movies_df = pd.read_csv('movies.csv')

# Load the similarity matrix
with open('similarity.pkl', 'rb') as f:
    similarity = pickle.load(f)

# Extract the movie titles
movies_list = movies_df['title'].values

# Create the Streamlit app
st.title('Movie Recommendation System')

# Create a search bar with autocomplete
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movies_list
)

# Display the selected movie
st.write('You selected:', selected_movie)

# Get and display recommendations if a movie is selected
if selected_movie:
    recommendations = recommend(selected_movie)
    st.write('Recommendations:')
    
    # Create 5 columns
    cols = st.columns(4)
    
    for i, movie in enumerate(recommendations):
        with cols[i]:
            poster_url = fetch_poster_url(movie)
            if poster_url:
                st.image(poster_url, width=150)
            st.write(f"{movie}")
