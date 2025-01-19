import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Spotify OAuth Setup
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
SCOPE = "user-library-read,playlist-read-private"

print(CLIENT_ID)
print(CLIENT_SECRET)
print(REDIRECT_URI)

# Initialize SpotifyOAuth object
sp_oauth = SpotifyOAuth(client_id=CLIENT_ID,
                         client_secret=CLIENT_SECRET,
                         redirect_uri=REDIRECT_URI,
                         scope=SCOPE)

# Get authorization URL
auth_url = sp_oauth.get_authorize_url()
print("Authorization URL:", auth_url)


# Initialize Spotipy Client (sp) after login
def initialize_spotify_client():
    sp = spotipy.Spotify(auth_manager=sp_oauth)
    return sp

def home_page():
    """Home page to show user info and logged-in data."""
    
    # Custom CSS for Gradient Background
    st.markdown("""
        <style>
            /* Gradient Background */
            .main {
                background: linear-gradient(to top, #000000, #121212, #1e1e1e);
                color: white;
                font-family: Arial, sans-serif;
                height: 100vh;
                margin: 0;
            }

            /* Playlist Container Styling (Greyish Rectangle) */
            .playlist-container {
                width: 200px !important;  /* Set the width of the container */
                height: 100px !important;  /* Set the height of the container */
                background-color: #2a2a2a;  /* Greyish background for the container */
                border-radius: 10px;  /* Optional: Round corners */
                padding: 10px;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 10px;
            }

            /* Playlist Image Styling */
            .playlist-image {
                width: 100px !important;  /* Set the width of the image */
                height: 60px !important;  /* Set the height of the image */
                object-fit: cover;  /* Keep the aspect ratio intact */
            }

            /* Title Styling */
            .title {
                margin-left: 34px;
            }
        </style>
    """, unsafe_allow_html=True)

    # Title content in the center of the screen
    st.markdown('<div class="title"><h1>Good afternoon</h1></div>', unsafe_allow_html=True)

    # Fetch and Display Playlists
    sp = initialize_spotify_client()
    playlists = sp.current_user_playlists(limit=8)['items']  # Fetching 8 playlists for the grid
    playlist_names = [playlist['name'] for playlist in playlists]
    playlist_images = [playlist['images'][0]['url'] if playlist['images'] else "https://via.placeholder.com/150" for playlist in playlists]

    # Display Playlists in a 2-row, 4-column grid
    rows = [playlist_names[:4], playlist_names[4:]]  # Splitting into two rows
    images = [playlist_images[:4], playlist_images[4:]]  # Splitting images into two rows

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
    home_page()
else:
    # Show login page if no token exists
    code = st.query_params.get('code', [None])[0]

    if code:
        # If there's a code in the URL, exchange it for the token
        token_info = sp_oauth.get_access_token(code)
        
        if token_info:
            st.session_state.token = token_info  # Store the token in session state
            st.rerun()  # This ensures the session is updated after login
        else:
            st.error("Failed to authenticate, please try again.")
    else:
        # Display login page if no token or code found
        st.title("Spotify Login Page")
        st.markdown("### Please log in to access your Spotify playlists!")
        auth_url = sp_oauth.get_authorize_url()
        st.markdown(f"[Login with Spotify]({auth_url})", unsafe_allow_html=True)
