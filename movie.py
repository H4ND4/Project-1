import streamlit as st
import requests

# API key
api_key = "28b8fdee"

# CSS
page_bg_img = '''
<style>
/* Background */
.stApp {
    background-color: #0f1b2b;  /* Navy blue background */
    color: white;  /* White text for contrast */
    font-family: 'Roboto', sans-serif;
}

/* Heading Style */
h1 {
    font-size: 2.5em;
    font-weight: 700;
    color: #3399ff;  /* Soft blue color for the heading */
    text-align: left; /* Align text to the left */
}

/* Subheader and Text */
h2, h3, p {
    font-size: 1.2em;
    color: #d0e1f9;  /* Light blue-grey text */
    text-align: left; /* Align text to the left */
}

/* Plot specific font style */
.stPlot {
    font-family: 'Georgia', serif;  /* Elegant font for the plot */
    font-size: 1.1em;
    color: #d0e1f9;
    text-align: left;
}

.stTextInput input:focus {
    border-color: #2ecc71;  /* Green border when focused */
    outline: none;
}

/* Columns layout */
.stColumns {
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: left; /* Ensure text is left aligned in columns */
}

/* Poster image */
.stImage img {
    border-radius: 8px;
    max-width: 300px;
    border: 5px solid #3399ff;  /* Blue border around the image */
}

/* Button style */
button {
    background-color: #2ecc71;  /* Soft green */
    color: white;
    padding: 12px 25px;
    border: none;
    border-radius: 5px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    width: 100%;
    margin-top: 30px;
    text-align: center;
}

button:hover {
    background-color: #3399ff;  /* Soft blue on hover */
}

/* Footer */
footer {
    color: #d0e1f9;
    font-size: 0.9em;
    text-align: center;
    margin-top: 40px;
}
</style>
'''

# Styles
st.markdown(page_bg_img, unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🔍 Movie Finder")
st.sidebar.write("Search for movie details below.")

# App title
st.title("🎬 Movie Search App 🎬")
st.write("Type the movie title and hit enter to explore details.")

# Movie search input
title_input = st.text_input("Enter Movie Title:")

if title_input:
    try:
        # Use the OMDb API to fetch movie details
        url = f"http://www.omdbapi.com/?t={title_input}&apikey={api_key}"
        response = requests.get(url)
        movie_data = response.json()

        if movie_data.get("Response") == "True":
          
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(movie_data.get('Poster', ''), use_column_width=True)
            with col2:
                st.subheader(movie_data.get('Title', 'N/A'))
                st.caption(f"Genre: {movie_data.get('Genre', 'N/A')} | Year: {movie_data.get('Year', 'N/A')}")
                
                # Plot 
                plot = movie_data.get('Plot', 'No plot available.')
                st.markdown(f"<p class='stPlot'>{plot}</p>", unsafe_allow_html=True)

                # Displaying Cast & Crew (with links to actors if available)
                st.write(f"**Director**: {movie_data.get('Director', 'N/A')}")
                st.write(f"**Writer**: {movie_data.get('Writer', 'N/A')}")
                
                actors = movie_data.get('Actors', 'N/A')
                if actors != 'N/A':
                    # Display link for the actor or show their images (if possible)
                    actor_list = actors.split(', ')
                    actor_links = [f"[{actor}](https://www.imdb.com/find?q={actor.replace(' ', '+')})" for actor in actor_list]
                    st.write(f"**Actors**: {' | '.join(actor_links)}")
                else:
                    st.write(f"**Actors**: {actors}")
                
                # Movie Duration
                runtime = movie_data.get('Runtime', 'N/A')
                st.write(f"**Duration**: {runtime}")

                # Displaying Ratings
                ratings = movie_data.get('Ratings', [])
                imdb_rating = None
                rt_rating = None
                for rating in ratings:
                    if rating['Source'] == 'Internet Movie Database':
                        imdb_rating = rating['Value']
                    elif rating['Source'] == 'Rotten Tomatoes':
                        rt_rating = rating['Value']
                
                st.write(f"**IMDb Rating**: {imdb_rating if imdb_rating else 'N/A'}")
                st.write(f"**Rotten Tomatoes Rating**: {rt_rating if rt_rating else 'N/A'}")
                
                # Displaying Box Office
                st.write(f"**Box Office**: {movie_data.get('BoxOffice', 'N/A')}")
                
                # Handle IMDb rating and display progress bar
                if imdb_rating:
                    imdb_numeric = imdb_rating.split("/")[0]  # Extract number from '8.3/10'
                    try:
                        imdb_numeric = float(imdb_numeric)
                        st.progress(imdb_numeric / 10)
                    except ValueError:
                        st.error("Invalid IMDb rating format.")
        else:
            st.error("No movie found with that title. Please try again.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Button
st.markdown('''
<a href="https://www.omdbapi.com" target="_blank">
    <button>Visit OMDb API</button>
</a>
''', unsafe_allow_html=True)
