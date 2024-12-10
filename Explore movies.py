import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import random
from datetime import datetime

# API Key for additional details
omdb_api_key = "28b8fdee"  
tmdb_api_key = "ffb7d4aeadc7e47d9d97c7a54bfadd6b"
tmdb_base_url = "https://api.themoviedb.org/3/"
omdb_base_url = "http://www.omdbapi.com/"

# Configure page
st.set_page_config(
    page_title="Movie App",
    page_icon="🎥",
    initial_sidebar_state="collapsed",
)

# Custom CSS for small buttons
st.markdown(
    """
    <style>
    .small-button button {
        padding: 4px 8px;
        font-size: 12px;
        border-radius: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title
st.markdown("<h1 style='text-align: center;'>EXPLORE MOVIES</h1>", unsafe_allow_html=True)

# Feature options
FEATURES = ["Trending Movies", "Top Rated", "Recently Released", "Movies by Genre"]

# Uniform-sized feature buttons
columns = st.columns(len(FEATURES))
for i, feature in enumerate(FEATURES):
    with columns[i]:
        if st.button(feature, key=f"button_{feature}"):
            st.session_state["selected_feature"] = feature

# Helper functions
def fetch_movies(api_url):
    movie_list = []
    for page in range(1, 6):  # Fetching up to 5 pages (20 movies per page)
        response = requests.get(f"{api_url}&page={page}")
        if response.status_code == 200:
            movie_list.extend(response.json().get("results", []))
    return movie_list

def fetch_omdb_details(movie_title):
    url = f"{omdb_base_url}?apikey={omdb_api_key}&t={movie_title}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return {}

def remove_duplicates(movie_list):
    seen_titles = set()
    unique_movies = []
    for movie in movie_list:
        title = movie.get("title", "Unknown")
        if title not in seen_titles:
            seen_titles.add(title)
            unique_movies.append(movie)
    return unique_movies

def format_release_date(date_string):
    try:
        return datetime.strptime(date_string, "%Y-%m-%d").strftime("%d %b, %Y")
    except:
        return "Unknown Release Date"

GENRES = {
    "Action": 28,
    "Family": 10751,
    "Comedy": 35,
    "Drama": 18,
    "Horror": 27,
    "Romance": 10749,
    "Adventure": 12,
    "Sci-Fi": 878,
}

selected_feature = st.session_state.get("selected_feature", None)

# Search Bar
st.markdown("<h2 style='text-align: center;'>Search for a Movie</h2>", unsafe_allow_html=True)
query = st.text_input("Search for a movie by title:")

if query:
    search_url = f"{tmdb_base_url}search/movie?api_key={tmdb_api_key}&query={query}"
    search_results = fetch_movies(search_url)
    
    if search_results:
        st.write(f"### Search Results for '{query}'")
        for i, movie in enumerate(search_results[:4]):
            cols = st.columns(4)
            for j, col in enumerate(cols):
                if i * 4 + j < len(search_results):
                    result_movie = search_results[i * 4 + j]
                    title = result_movie.get("title", "Unknown")
                    release_date = format_release_date(result_movie.get("release_date", "Unknown"))
                    rating = result_movie.get("vote_average", "N/A")
                    poster_url = result_movie.get("poster_path", "")
                    poster_url = f"https://image.tmdb.org/t/p/w500{poster_url}" if poster_url else "https://via.placeholder.com/500x750"
                    plot = fetch_omdb_details(title).get("Plot", "No plot available.")
                    
                    with col:
                        st.image(poster_url, caption=f"{title[:20]} ({release_date})", use_column_width=True)
                        st.write(f"⭐ {rating}")
                        st.write(f"Plot: {plot}")
    else:
        st.write(f"No results found for '{query}'.")

if selected_feature:
    st.write(f"### {selected_feature}")

    if selected_feature == "Trending Movies":
        trending_movies = remove_duplicates(fetch_movies(f"{tmdb_base_url}trending/movie/day?api_key={tmdb_api_key}"))
        if trending_movies:
            for i in range(0, len(trending_movies), 4):
                cols = st.columns(4)
                for j, col in enumerate(cols):
                    if i + j < len(trending_movies):
                        movie = trending_movies[i + j]
                        title = movie.get("title", "Unknown")
                        release_date = format_release_date(movie.get("release_date", "Unknown"))
                        rating = movie.get("vote_average", "N/A")
                        poster_url = movie.get("poster_path", "")
                        poster_url = f"https://image.tmdb.org/t/p/w500{poster_url}" if poster_url else "https://via.placeholder.com/500x750"
                        plot = fetch_omdb_details(title).get("Plot", "No plot available.")

                        with col:
                            st.image(poster_url, caption=f"{title[:20]} ({release_date})", use_column_width=True)
                            st.write(f"⭐ {rating}")
                            if st.button(f"The Plot", key=f"plot_trending_{i+j}"):
                                st.write(f"Plot: {plot}")

    elif selected_feature == "Recently Released":
        recent_movies = fetch_movies(f"{tmdb_base_url}movie/now_playing?api_key={tmdb_api_key}&region=US")
        recent_movies = remove_duplicates(recent_movies)
        if recent_movies:
            for i in range(0, len(recent_movies), 4):
                cols = st.columns(4)
                for j, col in enumerate(cols):
                    if i + j < len(recent_movies):
                        movie = recent_movies[i + j]
                        title = movie.get("title", "Unknown")
                        release_date = format_release_date(movie.get("release_date", "Unknown"))
                        rating = movie.get("vote_average", "N/A")
                        poster_url = movie.get("poster_path", "")
                        poster_url = f"https://image.tmdb.org/t/p/w500{poster_url}" if poster_url else "https://via.placeholder.com/500x750"
                        plot = fetch_omdb_details(title).get("Plot", "No plot available.")

                        with col:
                            st.image(poster_url, caption=f"{title[:20]} ({release_date})", use_column_width=True)
                            st.write(f"⭐ {rating}")
                            if st.button(f"The Plot", key=f"plot_recent_{i+j}"):
                                st.write(f"Plot: {plot}")

    elif selected_feature == "Top Rated":
        year_range = st.slider("Filter by Year", 1950, 2024, (2000, 2024))
        top_rated_movies = fetch_movies(f"{tmdb_base_url}movie/top_rated?api_key={tmdb_api_key}&region=US&primary_release_date.gte={year_range[0]}-01-01&primary_release_date.lte={year_range[1]}-12-31")
        filtered_movies = remove_duplicates(top_rated_movies)
        if filtered_movies:
            for i in range(0, len(filtered_movies), 4):
                cols = st.columns(4)
                for j, col in enumerate(cols):
                    if i + j < len(filtered_movies):
                        movie = filtered_movies[i + j]
                        title = movie.get("title", "Unknown")
                        release_date = format_release_date(movie.get("release_date", "Unknown"))
                        rating = movie.get("vote_average", "N/A")
                        poster_url = movie.get("poster_path", "")
                        poster_url = f"https://image.tmdb.org/t/p/w500{poster_url}" if poster_url else "https://via.placeholder.com/500x750"
                        plot = fetch_omdb_details(title).get("Plot", "No plot available.")

                        with col:
                            st.image(poster_url, caption=f"{title[:20]} ({release_date})", use_column_width=True)
                            st.write(f"⭐ {rating}")
                            if st.button(f"The Plot", key=f"plot_top_rated_{i+j}"):
                                st.write(f"Plot: {plot}")

    elif selected_feature == "Movies by Genre":
        year_range = st.slider("Filter by Year", 1950, 2024, (2000, 2024))
        genre = st.selectbox("Select Genre:", list(GENRES.keys()))
        genre_id = GENRES[genre]
        genre_movies = fetch_movies(
            f"{tmdb_base_url}discover/movie?api_key={tmdb_api_key}&with_genres={genre_id}&primary_release_date.gte={year_range[0]}-01-01&primary_release_date.lte={year_range[1]}-12-31"
        )
        genre_movies = remove_duplicates(genre_movies)
        if genre_movies:
            for i in range(0, len(genre_movies), 4):
                cols = st.columns(4)
                for j, col in enumerate(cols):
                    if i + j < len(genre_movies):
                        movie = genre_movies[i + j]
                        title = movie.get("title", "Unknown")
                        release_date = format_release_date(movie.get("release_date", "Unknown"))
                        rating = movie.get("vote_average", "N/A")
                        poster_url = movie.get("poster_path", "")
                        poster_url = f"https://image.tmdb.org/t/p/w500{poster_url}" if poster_url else "https://via.placeholder.com/500x750"
                        plot = fetch_omdb_details(title).get("Plot", "No plot available.")

                        with col:
                            st.image(poster_url, caption=f"{title[:20]} ({release_date})", use_column_width=True)
                            st.write(f"⭐ {rating}")
                            if st.button(f"The Plot", key=f"plot_genre_{i+j}"):
                                st.write(f"Plot: {plot}")