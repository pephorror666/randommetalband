# RandomMetal

## Overview

RandomMetal is a Streamlit application that helps you discover new metal albums.  It pulls from a CSV database of approximately 6000 metal albums and their Spotify URLs to present a random selection to the user.  If you're looking to expand your metal horizons, this app is for you!

## Features

*   **Random Album Selection:**  Displays a random metal album from a database of thousands.
*   **Spotify Integration:** Provides a direct link to the album's Spotify page (if available).
*   **Artist Tracking:**  Keeps track of previously shown artists to avoid repetition (until all artists have been shown).
*   **Simple and Intuitive Interface:**  Easy to use, with a focus on quickly discovering new music.

## Usage

The application is deployed on Streamlit Community Cloud and can be accessed at:

[https://randommetal.streamlit.app](https://randommetal.streamlit.app)

Simply visit the link and click the "New Record" button to see a new random metal album.

## Data Source

The application uses a CSV file (`metal_records.csv`) as its database. This file should contain the following columns:

*   `Band`: The name of the metal band.
*   `Album`: The title of the album.
*   `Spotify_URL` (or similar):  A URL linking to the album on Spotify.  (The exact column name may vary based on your CSV file).

## Repository Contents

*   `app_randommetal.py`: The main Streamlit application code.
*   `metal_records.csv`: The CSV file containing the metal album data.  (Note:  Due to size restrictions or licensing, a sample or a link to where the data was sourced might be provided instead of the full dataset).
*   `Readme.txt`: This file.
*   `manometa.png`: The icon used for the app (Optional).

## Dependencies

*   streamlit
*   pandas

You can install these dependencies using pip:

