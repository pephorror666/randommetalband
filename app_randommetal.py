import streamlit as st
import pandas as pd
import random

# Load the CSV data
@st.cache_data
def load_data():
    return pd.read_csv("metal_records.csv")

# Function to get a random record, excluding artists already shown
def get_random_record(df, shown_artists):
    available_records = df[~df['Band'].isin(shown_artists)]
    if available_records.empty:
        st.warning("All artists have been shown. Resetting the list.")
        shown_artists.clear()
        available_records = df
    random_record = available_records.sample(n=1).iloc[0]
    shown_artists.append(random_record['Band'])
    return random_record

# Initialize session state to keep track of shown artists
if 'shown_artists' not in st.session_state:
    st.session_state.shown_artists = []

# Load the data
df = load_data()

# Get a random record
record = get_random_record(df, st.session_state.shown_artists)

# Display the record in a nice HTML card
st.markdown(
    f"""
    <div style="border: 2px solid #e0e0e0; border-radius: 10px; padding: 20px; text-align: center;">
        <img src="{record['Image URL']}" alt="{record['Album']}" style="width: 200px; border-radius: 10px;">
        <h2>{record['Band']}</h2>
        <h3>{record['Album']}</h3>
        <p><strong>Genre:</strong> {record['Genre']}</p>
        <a href="{record['Spotify URL']}" target="_blank" style="text-decoration: none;">
            <button style="background-color: #1DB954; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;">
                Listen on Spotify
            </button>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

# Button to get a new random record
if st.button("Get Another Random Record"):
    record = get_random_record(df, st.session_state.shown_artists)
    st.experimental_rerun()