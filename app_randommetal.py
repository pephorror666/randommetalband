import streamlit as st
import pandas as pd
import random

# SET PAGE CONFIG
st.set_page_config(page_title="RandomMetal", page_icon="manometa.png", layout="centered", initial_sidebar_state="auto", menu_items=None)

# Cargar los datos CSV
@st.cache_data
def load_data():
    return pd.read_csv("metal_records.csv")

# Función para obtener un registro aleatorio, excluyendo artistas ya mostrados
def get_random_record(df, shown_artists, genre_filter=None):
    if genre_filter:
        available_records = df[(~df['Band'].isin(shown_artists)) & (df['Genre'].str.contains(genre_filter, case=False))]
    else:
        available_records = df[~df['Band'].isin(shown_artists)]

    if available_records.empty:
        if genre_filter != 'None':
            st.warning(f"No more bands with that Genre. All artists have been shown. Reiniciando the list.")
        shown_artists.clear()
        available_records = df if not genre_filter else df[df['Genre'].str.contains(genre_filter, case=False)]
        if available_records.empty:
            if genre_filter != 'None':
                st.error(f"No bands found with the genre '{genre_filter}'. Filtering ALL bands")
            available_records = df

    random_record = available_records.sample(n=1).iloc[0]
    shown_artists.append(random_record['Band'])
    return random_record

# Inicializar el estado de la sesión para mantener un registro de los artistas mostrados
if 'shown_artists' not in st.session_state:
    st.session_state.shown_artists = []
if 'current_record' not in st.session_state:
    st.session_state.current_record = None
if 'genre_filter' not in st.session_state:
    st.session_state.genre_filter = None

# Cargar los datos
df = load_data()

# Obtener un registro aleatorio al inicio
if st.session_state.current_record is None:
    st.session_state.current_record = get_random_record(df, st.session_state.shown_artists, st.session_state.genre_filter)

# Custom CSS to style the app
st.markdown(
    """
    <style>
    .metal-card {
        border: 1px solid #444;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(255, 255, 255, 0.1);
        background-color: #1E1E1E;
        margin-bottom: 20px;
    }
    /* Style for the band name (all caps) */
    .band-name {
        font-size: 28px;
        font-weight: bold;
        text-transform: uppercase;
        color: #E0E0E0;
        margin-bottom: 10px;
    }

    /* Style for the album and genre (capitalize first letter of each word) */
    .album {
        font-size: 18px;
        color: #B0B0B0;
        margin-bottom: 8px;
        text-transform: capitalize;
    }

    /* Style for the Spotify link */
    .spotify-link {
        display: inline-block;
        background-color: #1DB954;
        color: white !important;
        padding: 10px 20px;
        border-radius: 5px;
        text-decoration: none;
        font-weight: bold;
        margin-top: 10px;
        width: 100%;
    }

    /* Style for the image */
    .album-image {
        max-width: 50%;
        height: auto;
        border-radius: 5px;
        margin-top: 15px;
    }

    /* Style for the button */
    .stButton button {
        width: 100%;
        background-color: #1DB954;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 10px;
        border: none;
        cursor: pointer;
    }

    .stButton button:hover {
        background-color: #1ED760;
    }
    a:link {
        color: #1DB954;
        }
    .genre-link {
        color: #1DB954;
        text-decoration: none;
        margin: 2px;
    }
    .genre-link:hover {
        text-decoration: underline;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Función para formatear los géneros como hipervínculos
def format_genres_as_links(genres):
    genres_list = genres.split(" / ")
    links = []
    for genre in genres_list:
        genre_name = genre.lower().replace(" ", "")
        link_label = f"#{genre_name}"
        link = f'<a class="genre-link" href="?genre_filter={genre}" target="_self">{link_label}</a>'
        links.append(link)
    return " ".join(links)

#Get the genre filter from the URL
#url_params = st.experimental_get_query_params()  ### This line is the one that works locally the next one for the online app in streamlit community cloud
url_params = st.get_query_params
genre_filter_from_url = url_params.get("genre_filter", None)
if genre_filter_from_url:
    st.session_state.genre_filter = genre_filter_from_url[0]
    st.session_state.shown_artists = []
    st.session_state.current_record = get_random_record(df, st.session_state.shown_artists, st.session_state.genre_filter)


# Mostrar el registro en una tarjeta HTML agradable
if st.session_state.current_record is not None:
    record = st.session_state.current_record
    formatted_genres = format_genres_as_links(record['Genre'])

    st.markdown(
        f"""
        <div class="metal-card">
            <div class="band-name">{record['Band']}</div>
            <div class="album">{record['Album']}</div>
            <div class="genre">{formatted_genres}</div>
            <a class="spotify-link" href="{record['Spotify URL']}" target="_blank">Listen on Spotify</a>
            <img class="album-image" src="{record['Image URL']}" alt="{record['Band']} - {record['Album']}">
        </div>
        """,
        unsafe_allow_html=True
    )

# Button to get a new random record
if st.button("Get Another Random Metal Record"):
    st.session_state.genre_filter = None
    # Add this line to clear the genre_filter from the URL
    st.experimental_set_query_params(genre_filter=None)
    st.session_state.current_record = get_random_record(df, st.session_state.shown_artists)
    st.rerun()
    #st.experimental_rerun() ### when locally to run in my laptop change rerun for experimental_rerun
