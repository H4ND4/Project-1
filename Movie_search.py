import streamlit as st
import requests

# API key for OMDb
api_key = "28b8fdee"

# Function to fetch search suggestions
def fetch_movie_suggestions(query):
    if not query.strip():
        return []  # Return empty if no query
    try:
        # OMDb API's search endpoint
        url = f"http://www.omdbapi.com/?s={query}&apikey={api_key}"
        response = requests.get(url)
        data = response.json()
        if data.get("Response") == "True":
            return [movie['Title'] for movie in data['Search']]  # Extract movie titles
        else:
            return []
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return []

# Function to fetch movie details
def fetch_movie_details(title):
    try:
        # Fetch movie details using OMDb API
        url = f"http://www.omdbapi.com/?t={title}&apikey={api_key}"
        response = requests.get(url)
        return response.json()
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return {}

# Bright blue theme CSS
page_bg_img = '''
<style>
/* Background */
.stApp {
    background-color: transparent; /* Adapt to the theme */
    color: inherit; /* Use the default text color for the theme */
    font-family: 'Arial', sans-serif;
}

/* Heading Style */
h1 {
    font-size: 2.5em;
    font-weight: bold;
    color: #3399FF; /* Bright blue for headings */
    text-align: center;
}

/* Subheader and Text */
h2, h3, p {
    font-size: 1.2em;
    color: inherit; /* Adapt to the theme */
    text-align: center;
}

/* Plot specific font style */
.stPlot {
    font-family: 'Georgia', serif;
    font-size: 1.1em;
    color: inherit; /* Adapt to the theme */
    text-align: center;
}

/* Movie Poster */
.stImage img {
    border-radius: 8px;
    max-width: 250px;
    margin-bottom: 20px;
    border: 2px solid #3399FF; /* Bright blue border for the poster */
}

/* Button style */
button {
    background-color: #3399FF; /* Bright blue */
    color: white;
    padding: 12px 25px;
    border: none;
    border-radius: 5px;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
    display: block;
    margin: 30px auto;
    text-align: center;
}

button:hover {
    background-color: #66B2FF; /* Slightly lighter blue on hover */
}

/* Footer */
footer {
    color: inherit; /* Adapt to the theme */
    font-size: 0.9em;
    text-align: center;
    margin-top: 40px;
}
</style>
'''

# Apply the CSS
st.markdown(page_bg_img, unsafe_allow_html=True)

# Title and instructions
st.title("🔍 SEARCH FOR A MOVIE 🔍")
st.write("Start typing to see movie suggestions below, and click on one to view its details!")

# Input field for the search bar
query = st.text_input("Enter Movie Title:", placeholder="Type something...")

# Display suggestions while typing
if query:
    suggestions = fetch_movie_suggestions(query)
    if suggestions:
        st.write("🔽 **Suggestions:**")
        for suggestion in suggestions:
            if st.button(suggestion):  # Create a button for each suggestion
                # Fetch and display movie details when clicked
                movie_data = fetch_movie_details(suggestion)
                if movie_data.get("Response") == "True":
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.image(movie_data.get('Poster', ''), use_column_width=True)
                    with col2:
                        st.subheader(movie_data.get('Title', 'N/A'))
                        st.caption(f"Genre: {movie_data.get('Genre', 'N/A')} | Year: {movie_data.get('Year', 'N/A')}")
                        st.write(f"**Plot**: {movie_data.get('Plot', 'N/A')}")
                        st.write(f"**Director**: {movie_data.get('Director', 'N/A')}")
                        st.write(f"**Writer**: {movie_data.get('Writer', 'N/A')}")
                        st.write(f"**Actors**: {movie_data.get('Actors', 'N/A')}")
                        st.write(f"**Duration**: {movie_data.get('Runtime', 'N/A')}")
                        st.write(f"**IMDb Rating**: {movie_data.get('imdbRating', 'N/A')}")
                        st.write(f"**Box Office**: {movie_data.get('BoxOffice', 'N/A')}")
                else:
                    st.error("Movie details could not be fetched. Try another suggestion.")
    else:
        st.warning("No suggestions found. Try typing something else.")
else:
    st.info("Start typing to get suggestions.")
