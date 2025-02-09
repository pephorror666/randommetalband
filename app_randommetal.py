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
def get_random_record(df, shown_artists):
    available_records = df[~df['Band'].isin(shown_artists)]
    if available_records.empty:
        st.warning("Todos los artistas han sido mostrados. Reiniciando la lista.")
        shown_artists.clear()
        available_records = df
    random_record = available_records.sample(n=1).iloc[0]
    shown_artists.append(random_record['Band'])
    return random_record

# Inicializar el estado de la sesión para mantener un registro de los artistas mostrados
if 'shown_artists' not in st.session_state:
    st.session_state.shown_artists = []
if 'current_record' not in st.session_state:
    st.session_state.current_record = None

# Cargar los datos
df = load_data()

# Obtener un registro aleatorio al inicio
if st.session_state.current_record is None:
    st.session_state.current_record = get_random_record(df, st.session_state.shown_artists)

# Custom CSS to style the app
st.markdown(
    """
    <style>
    /* Style for the card */
    .card {
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
    .album, .genre {
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

    </style>
    """,
    unsafe_allow_html=True
)

# Mostrar el registro en una tarjeta HTML agradable
if st.session_state.current_record is not None:
    record = st.session_state.current_record
    st.markdown(
        f"""
        <div class="card">
            <div class="band-name">{record['Band']}</div>
            <div class="album"><strong>Álbum:</strong> {record['Album']}</div>
            <div class="genre"><strong>Género:</strong> {record['Genre']}</div>
            <a class="spotify-link" href="{record['Spotify URL']}" target="_blank">Listen on Spotify</a>
            <img class="album-image" src="{record['Image URL']}" alt="{record['Band']} - {record['Album']}">
        </div>
        """,
        unsafe_allow_html=True
    )

# Mostrar el botón debajo de la tarjeta
if st.button("Random Record", key="unique_button"):
    st.session_state.current_record = get_random_record(df, st.session_state.shown_artists)
    #st.experimental_rerun()  # Force the app to rerun and update the card
    st.rerun() # In local i have to delete this line for it to work