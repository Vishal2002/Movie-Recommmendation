import streamlit as st
import pandas as pd
import pickle
from tmdbv3api import TMDb, Movie
import os
from dotenv import load_dotenv, dotenv_values 
load_dotenv() 
 

tmdb = TMDb()
tmdb.api_key = os.getenv("API_KEY")
tmdb.language = 'en'
tmdb_movie = Movie()

def recommend(movie):
    recommendation = []
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    for i in movies_list:
        recommendation.append(movies_df.iloc[i[0]].title)
    return recommendation


def fetch_poster_url(movie_title):
    search_result = tmdb_movie.search(movie_title)
    if search_result:
        movie_id = search_result[0].id
        movie_details = tmdb_movie.details(movie_id)
        poster_path = movie_details.poster_path
        full_path = f"https://image.tmdb.org/t/p/w500{poster_path}"
        return full_path
    return None

movies_df = pd.read_csv('movies.csv')


with open('similarity.pkl', 'rb') as f:
    similarity = pickle.load(f)

movies_list = movies_df['title'].values


st.title('Movie Recommendation System')


selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movies_list
)


st.write('You selected:', selected_movie)


if selected_movie:
    recommendations = recommend(selected_movie)
    st.write('Recommendations:')
    

    cols = st.columns(4)
    
    for i, movie in enumerate(recommendations):
        with cols[i]:
            poster_url = fetch_poster_url(movie)
            if poster_url:
                st.image(poster_url, width=150)
            st.write(f"{movie}")
