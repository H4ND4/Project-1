import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configure page
st.set_page_config(
    page_title="Movie App",
    page_icon="🎥",
    initial_sidebar_state="collapsed",
)

# Title of the page
st.markdown("<h1 style='text-align: center;'>Welcome to the Movie App 🎬</h1>", unsafe_allow_html=True)

# Home Page content
st.write("""
Welcome to the **Movie App**! This is your one-stop destination to explore, search, and discover the best movies from various genres and regions.

### Explore Movies
You can dive into a wide variety of movies by exploring:
- **Trending Movies**: Check out the latest movies that are trending worldwide.
- **Top Rated**: Discover the highest-rated movies of all time or filter by release year.
- **Recently Released**: Stay updated with the most recent movie releases.
- **Movies by Genre**: Choose from various genres like Action, Drama, Comedy, and more to find movies tailored to your preferences.

### Movie Search
You can search for any movie by title and get detailed information, including:
- Movie plot
- Cast and crew
- Ratings (IMDb, Rotten Tomatoes)
- Box office earnings
- And much more!
""")

# EDA Analysis Section
st.subheader("EDA Analysis")

image_path = "C:\\Users\\handd\\OneDrive\\Desktop\\Intermediate Python\\GitHub\\intermediate-python-fall-2024\\Week 06 - Web Scraping\\download.png"
st.image(image_path, caption='Popularity by Genre (Average IMDb Rating by Genre)', use_column_width=True)

image_path = r"C:\Users\handd\OneDrive\Desktop\Intermediate Python\GitHub\intermediate-python-fall-2024\Week 06 - Web Scraping\2.png"
st.image(image_path, caption='Top Directors by Movie Count', use_column_width=True)

image_path = r"C:\Users\handd\OneDrive\Desktop\Intermediate Python\GitHub\intermediate-python-fall-2024\Week 06 - Web Scraping\3.png"
st.image(image_path, caption='Top 10 Movies by IMDb Rating', use_column_width=True)
