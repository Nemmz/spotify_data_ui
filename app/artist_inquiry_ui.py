"""
Author: Isaac Jarrells
Date: March 14, 2025,
Purpose: Displays artist data using helper functions from get_artist_data functions.
Resources:
"""
import streamlit as st
import time
from get_artist_data import get_token, search_artist, get_top_tracks, get_albums

ARTIST_DATA_FILE = "app/data/artist.json"
SONG_DATA_FILE = "app/data/top_songs.json"
ALBUM_DATA_FILE = "app/data/albums.json"
token = get_token()
SPOTIFY_IMAGE_LRG = "app/assets/Spotify_Full_Logo_RGB_Black.png"
SPOTIFY_IMAGE_SML = "app/assets/Spotify_Primary_Logo_RGB_Green.png"


# Edits the Page Name and Icon Next to it.
st.set_page_config(
    page_title="Spotify Artist Data",
    page_icon="💿",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
    body{
        font-size: 21px;
    }
        header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

# Has credits for Spotify API at bottom right corner
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        bottom: 0;
        right: 0;
        text-align: right;
        padding: 7px;
        background-color: black;
    }
    </style>
    <div class="footer">
        Data provided by Spotify API
    </div>
    """,
    unsafe_allow_html=True
)

# Title for App
st.header("Spotify Artist Data", divider="green")

# Adds the Spotify Logo at the Top of the Page
st.logo(
    SPOTIFY_IMAGE_LRG,
    link="https://open.spotify.com/",
    icon_image=SPOTIFY_IMAGE_SML)

if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False

left, right = st.columns(2, gap="small")

# Text Input for Artist Search
text_input = st.sidebar.text_input(
    "Enter Artist Name:", placeholder="Enter Artist Name...",
    key="placeholder", label_visibility=st.session_state.visibility,
    disabled=st.session_state.disabled,
)

# If Text is Inputed
if text_input:
    # Progress Bar Before Search is Completed
    progress_bar = st.progress(0, text="Searching for Artist...")
    for percent_complete in range(100):
        time.sleep(0.01)
        progress_bar.progress(percent_complete + 1, text="Searching for Artist...")
    time.sleep(1)
    progress_bar.empty()

    # Right Column Text: Photo of Artist and Caption of Picture
    with right:
        try:
            data = search_artist(text_input, token, ARTIST_DATA_FILE)
            if data:
                artist = data["artists"]["items"][0]
                artist_url = artist["external_urls"]["spotify"]
                right = right.container(border=True).image(artist["images"][0]["url"],
                                                           use_container_width=True)

        except RuntimeError as err:
            st.error("No Picture Found", icon="❌")
        except NameError as err:
            st.error("No Picture Found", icon="❌")

    # Adds a Link to the Spotify Artist on the Sidebar
    with st.sidebar:
        try:
            st.link_button("Artist's Spotify Page",
                           url=artist_url,
                           type="secondary",
                           icon="🔗",
                           use_container_width=False)
            st.subheader("Artist's Albums", divider="grey")
            st.text("• " + "\n• ".join(get_albums(artist['id'], token, ALBUM_DATA_FILE)))
        except RuntimeError as err:
            st.error("Could Not Find Artist: Ensure the Name is Exactly as Appears on Spotify.", icon="⚠️")
        except NameError as err:
            st.error("Could Not Find Artist: Ensure the Name is Exactly as Appears on Spotify.", icon="⚠️")


    # Displays the data found for the Artist on the left column
    with left:
        try:
            if data:
                st.text(f"Artist Name: {artist['name']}")
                st.text(f"Followers: {artist['followers']['total']}")
                if artist["genres"]:
                    st.text(f"Genres: {', '.join(artist['genres']).title()}")
                else:
                    st.text("Genres: N/a")
                with st.expander(f"Popularity: {101 - artist["popularity"]}"):
                    st.markdown("Popularity is on a scale of 1-100 and is not one to one but rather a general idea "
                                "of their popularity.")
                st.text(f"Top Tracks:\n{'\n'.join(get_top_tracks(artist['id'], token, SONG_DATA_FILE))}")
        except RuntimeError as err:
            st.error("No Data Found", icon="❌")
        except NameError as err:
            st.error("No Data Found", icon="❌")
