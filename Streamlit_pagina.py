import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve client_id, client_secret, and redirect_uri from environment variables
CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
SCOPE = "user-library-read,playlist-read-private"

print("CLIENT_ID:", CLIENT_ID)
print("CLIENT_SECRET:", CLIENT_SECRET)
print("REDIRECT_URI:", REDIRECT_URI)


# Spotify Authentication Setup
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
))

# Function to check if the user is authenticated
def is_authenticated():
    try:
        sp.current_user()  # Try fetching user data
        return True
    except spotipy.exceptions.SpotifyOAuthError:
        return False

# Home page content after successful login
def home_page():
    st.title("Good afternoon")

    # Custom CSS for Gradient Background
    st.markdown("""
        <style>
            .main {
                background: linear-gradient(to top, #000000, #121212, #1e1e1e);
                color: white;
                font-family: Arial, sans-serif;
                height: 100vh;
            }

            /* Sidebar */
            .sidebar .sidebar-content {
                background-color: #181818;
                color: white;
            }

            /* Titles */
            h1, h2, h3, h4, h5, h6 {
                color: white;
            }

            /* Buttons */
            .stButton button {
                background-color: #1DB954;
                color: white;
                border-radius: 5px;
                border: none;
            }
        </style>
    """, unsafe_allow_html=True)

    # Sidebar Content
    user_profile = sp.current_user()  # Get user profile
    st.sidebar.title("Spotify")
    st.sidebar.markdown("**Home**")
    st.sidebar.markdown("**Search**")
    st.sidebar.markdown("**Your Library**")
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Playlists**")
    st.sidebar.markdown("- Create Playlist")
    st.sidebar.markdown("- Liked Songs")

    # User Info in the sidebar
    st.sidebar.image(user_profile["images"][0]["url"], width=50)
    st.sidebar.write(f"Logged in as: {user_profile['display_name']}")

    # Fetch and Display Playlists
    playlists = sp.current_user_playlists(limit=8)['items']
    playlist_names = [playlist['name'] for playlist in playlists]
    playlist_images = [playlist['images'][0]['url'] if playlist['images'] else "https://via.placeholder.com/150" for playlist in playlists]

    # Display Playlists in two rows
    rows = [playlist_names[:4], playlist_names[4:]]
    images = [playlist_images[:4], playlist_images[4:]]
    
    for row, row_images in zip(rows, images):
        cols = st.columns(4)
        for col, name, img in zip(cols, row, row_images):
            with col:
                st.image(img, use_column_width=True, caption=name)

# Display the login button if not authenticated
if not is_authenticated():
    st.title("Spotify Login Page")
    st.markdown("### Please log in to access your playlists!")

    # Spotify login button (calls authentication process)
    auth_url = sp.auth_manager.get_authorize_url()
    st.markdown(f"[Login to Spotify]({auth_url})", unsafe_allow_html=True)

else:
    # If user is authenticated, show the home page
    home_page()
