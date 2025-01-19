import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Spotify API credentials
CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

sp_oauth = SpotifyOAuth(client_id=CLIENT_ID,
                        client_secret=CLIENT_SECRET,
                        redirect_uri=REDIRECT_URI,
                        scope="user-library-read playlist-read-private")

def login_user():
    auth_url = sp_oauth.get_authorize_url()
    st.write(f"Please log in: [Login to Spotify]({auth_url})")

def handle_callback():
    query_params = st.query_params
    if 'code' in query_params:
        st.session_state['auth_code'] = query_params['code'][0]
        try:
            st.write(f"Authorization Code: {st.session_state['auth_code']}")
            token_info = sp_oauth.get_access_token(code=st.session_state['auth_code'])
            st.write(f"Token Info: {token_info}")
            st.session_state['access_token'] = token_info['access_token']
            st.session_state['logged_in'] = True
            st.write("Authentication successful! Reloading...")
            st.experimental_rerun()
        except spotipy.SpotifyOauthError as e:
            st.error(f"OAuth Error: {e}")
            st.session_state['logged_in'] = False
            st.session_state.pop('auth_code', None)
            st.session_state.pop('access_token', None)
            st.write("Please try logging in again.")
            login_user()

def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if not st.session_state['logged_in']:
        # Clear session state to ensure a fresh start
        st.session_state.clear()
        login_user()
        handle_callback()
    else:
        home_page()

def home_page():
    st.title('My Spotify Playlists')

    token = st.session_state.get('access_token')
    sp = spotipy.Spotify(auth=token)

    def display_playlists():
        playlists = sp.current_user_playlists()
        for playlist in playlists['items']:
            st.write(playlist['name'])

    if st.button('Show my playlists'):
        display_playlists()

if __name__ == "__main__":
    main()
