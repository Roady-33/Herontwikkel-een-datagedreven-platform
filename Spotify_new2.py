import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
SCOPE = "user-library-read"

# Initialize SpotifyOAuth object
sp_oauth = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
)

# Function to initialize Spotify client
def initialize_spotify_client():
    token = st.session_state.get("token")
    if token:
        return spotipy.Spotify(auth=token)
    else:
        st.error("Token not found. Please log in again.")
        return None

# Function to render the home page
def home_page():
    """Home page to show user info and logged-in data."""
    
    # Custom CSS for Gradient Background
    st.markdown("""
        <style>
            .main {
                background: linear-gradient(to top, #000000, #121212, #1e1e1e);
                color: white;
                font-family: Arial, sans-serif;
                height: 100vh;
                margin: 0;
            }
            .playlist-container {
                width: 200px !important;
                height: 100px !important;
                background-color: #2a2a2a;
                border-radius: 10px;
                padding: 10px;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 10px;
            }
            .playlist-image {
                width: 100px !important;
                height: 60px !important;
                object-fit: cover;
            }
            .title {
                margin-left: 34px;
            }
        </style>
    """, unsafe_allow_html=True)

    # Title content in the center of the screen
    st.markdown('<div class="title"><h1>Good afternoon</h1></div>', unsafe_allow_html=True)

    # Fetch and Display Playlists
    sp = initialize_spotify_client()
    if sp:
        playlists = sp.current_user_playlists(limit=8)['items']  # Fetching 8 playlists
        playlist_names = [playlist['name'] for playlist in playlists]
        playlist_images = [playlist['images'][0]['url'] if playlist['images'] else "https://via.placeholder.com/150" for playlist in playlists]

        # Display Playlists in a 2-row, 4-column grid
        rows = [playlist_names[:4], playlist_names[4:]]
        images = [playlist_images[:4], playlist_images[4:]]

        for row, row_images in zip(rows, images):
            cols = st.columns(4)  # Create 4 columns for each row
            for col, name, img in zip(cols, row, row_images):
                with col:
                    # Create the greyish container with the image inside it
                    st.markdown(f'<div class="playlist-container"><img class="playlist-image" src="{img}" alt="{name}"></div>', unsafe_allow_html=True)
                    st.write(name)  # Display playlist name under the image

# Main section of the app
if "token" in st.session_state:
    # If token exists in session state, initialize Spotify client and go to home page
    sp = initialize_spotify_client()
    if sp:
        home_page()
else:
    # Handle login flow
    code = st.query_params.get('code', [None])[0]  # Fixed query_params usage

    if code:
        try:
            # Exchange code for access token
            token_info = sp_oauth.get_access_token(code)
            if token_info:
                st.session_state.token = token_info['access_token']
                st.experimental_rerun()
            else:
                st.error("Failed to retrieve access token.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        # Display login page
        st.title("Spotify Login")
        st.markdown("### Please log in to access your Spotify playlists!")
        auth_url = sp_oauth.get_authorize_url()
        st.markdown(f"[Login with Spotify]({auth_url})", unsafe_allow_html=True)
