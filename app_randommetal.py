import streamlit as st
import requests
import random
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from bs4 import BeautifulSoup

# Last.fm API key
lastfm_api_key = "41e86ee4787f1a444ba944478a89190c"

# Spotify API credentials
spotify_client_id = 'eec45e33c824444a889a6a94cb70ad32'
spotify_client_secret = 'b124829f4d014b31a98329712276dd79'

# Initialize Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=spotify_client_id, client_secret=spotify_client_secret))

# List of metal genres and subgenres
metal_genres = [
    "Heavy Metal", "Death Metal", "Thrash Metal", "Blackened", "Brutal Death Metal",
    "Melodic Death Metal", "Folk Metal", "Black Metal", "Grindcore", "Stoner Metal",
    "Sludge", "Powerviolence", "Hardcore Metal", "Power Metal", "Goth Metal", "Speed Metal", "Industrial Metal", "Doom Metal",
    "NWOBHM", "Viking Metal", "Deathgrind"
]

def get_random_metal_band():
    # Get a random metal genre
    genre = random.choice(metal_genres)
    
    # Search for artists by genre
    url = f"http://ws.audioscrobbler.com/2.0/?method=tag.gettopartists&tag={genre}&api_key={lastfm_api_key}&format=json"
    response = requests.get(url)
    data = response.json()
    
    # Extract artists from the response
    artists = data.get("topartists", {}).get("artist", [])
    
    if artists:
        # Return a random artist from the list
        return random.choice(artists)
    else:
        return None

def get_artist_info(artist_name):
    # Get artist info from Last.fm
    url = f"http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={artist_name}&api_key={lastfm_api_key}&format=json"
    response = requests.get(url)
    data = response.json()
    
    artist_info = data.get("artist", {})
    
    return artist_info

def get_spotify_url_and_image(artist_name):
    # Search for the artist on Spotify
    results = sp.search(q=artist_name, type="artist", limit=1)
    if results and results["artists"]["items"]:
        artist = results["artists"]["items"][0]
        # Verify that the artist name matches closely
        if artist_name.lower() in artist["name"].lower():
            spotify_url = artist["external_urls"]["spotify"]
            # Get the artist's image (if available)
            if artist["images"]:
                image_url = artist["images"][0]["url"]
            else:
                image_url = None
            return spotify_url, image_url
    return None, None

def get_bandcamp_artist_url_and_image(artist_name):
    # Construct the search query
    search_query = f"{artist_name}".replace(" ", "+")
    search_url = f"https://bandcamp.com/search?q={search_query}&item_type=a"

    # Make a request to the search URL
    response = requests.get(search_url)
    if response.status_code != 200:
        return None, None

    # Parse the HTML content of the search results
    soup = BeautifulSoup(response.content, 'html.parser')
    result_info = soup.find('li', class_='searchresult data-search')

    if result_info:
        artist_url_tag = result_info.find('a', href=True)
        if artist_url_tag:
            artist_url = artist_url_tag['href']
            # Clean up the URL
            url_modificada = artist_url.split("?from")[0]
            # Try to get the artist's image from Bandcamp
            image_tag = result_info.find('img', src=True)
            if image_tag:
                image_url = image_tag['src']
            else:
                image_url = None
            return url_modificada, image_url
    return None, None

def generate_share_text(artist_name, tags, spotify_url, bandcamp_url):
    # Prepare hashtags
    hashtags = ["#nowplaying"] + [f"#{tag.replace(' ', '')}" for tag in tags[:3]]
    hashtags_str = " ".join(hashtags)
    
    # Prepare links
    links = []
    if spotify_url:
        links.append(f"Spotify: {spotify_url}")
    if bandcamp_url:
        links.append(f"Bandcamp: {bandcamp_url}")
    links_str = "\n".join(links)
    
    # Full share text
    share_text = f"I'm listening to {artist_name} {hashtags_str}\n{links_str}"
    return share_text

def display_artist_info(artist_info, spotify_url, bandcamp_url, image_url):
    st.write(f"**Name:** {artist_info.get('name', 'N/A')}")
    
    # Display tags
    tags = artist_info.get("tags", {}).get("tag", [])
    if tags:
        st.write("**Tags:**")
        tag_names = [tag["name"] for tag in tags]
        st.write(", ".join(tag_names))
    
    # Display bio summary
    bio = artist_info.get("bio", {}).get("summary", "No bio available.")
    st.write(f"**Bio:** {bio}")
    
    # Display artist image
    if image_url:
        st.image(image_url, caption=artist_info.get('name', 'N/A'), width=300)
    
    # Display Spotify and Bandcamp links if available
    if spotify_url or bandcamp_url:
        st.write("**Links:**")
        if spotify_url:
            st.markdown(f"🎵 [Listen on Spotify]({spotify_url})")
        if bandcamp_url:
            st.markdown(f"🎸 [Listen on Bandcamp]({bandcamp_url})")
    else:
        st.warning("No external links found for this artist.")
    
    # Generate share text
    if tags:
        share_text = generate_share_text(artist_info.get('name', 'N/A'), tag_names, spotify_url, bandcamp_url)
        st.write("**Share:**")
        st.code(share_text)

# Streamlit app
def main():
    st.set_page_config(page_title="Random Metal Band", page_icon="🎸", layout="centered")
    
    # Custom CSS for dark theme
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #1e1e1e;
            color: #ffffff;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 16px;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.title("🎸 Random Metal Band Finder")
    st.write("Discover a random metal band every time you click the button below!")
    
    if st.button("Find a Random Metal Band"):
        while True:
            artist = get_random_metal_band()
            if artist:
                artist_name = artist["name"]
                
                # Get artist info from Last.fm
                artist_info = get_artist_info(artist_name)
                
                # Get Spotify URL and image
                spotify_url, spotify_image_url = get_spotify_url_and_image(artist_name)
                
                # Get Bandcamp URL and image
                bandcamp_url, bandcamp_image_url = get_bandcamp_artist_url_and_image(artist_name)
                
                # Determine the final image URL (prefer Spotify image)
                image_url = spotify_image_url if spotify_image_url else bandcamp_image_url
                
                # If neither Spotify nor Bandcamp links are found, retry with a new random band
                if not spotify_url and not bandcamp_url:
                    continue
                
                # Display artist info and links
                st.write(f"### {artist_name}")
                display_artist_info(artist_info, spotify_url, bandcamp_url, image_url)
                break
            else:
                st.error("No metal bands found. Try again!")
                break

if __name__ == "__main__":
    main()