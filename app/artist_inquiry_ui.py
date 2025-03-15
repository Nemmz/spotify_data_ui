"""
Author: Isaac Jarrells
Date: March 14, 2025,
Purpose: Displays artist data using helper functions from get_artist_data functions.
Resources:
"""
import streamlit as st
import time
from get_artist_data import get_token, search_artist, get_top_tracks

ARTIST_DATA_FILE = "app/data/artist.json"
SONG_DATA_FILE = "app/data/top_songs.json"
token = get_token()


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
st.header("Spotify Artist Data", divider=True)


if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False

left, right = st.columns(2, gap="small")


text_input = st.sidebar.text_input(
    "Enter Artist Name:", placeholder="Enter Artist Name...",
    key="placeholder", label_visibility=st.session_state.visibility,
    disabled=st.session_state.disabled,
)

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

        except Exception as e:
            st.write(e)

    with st.sidebar:
        st.link_button("Artist's Spotify Page",
                       url=artist_url,
                       type="secondary",
                       icon="🔗",
                       use_container_width=False)

    with left:
        if data:
            st.text(f"Artist Name: {artist['name']}")
            if artist["genres"]:
                st.text(f"Genres: {', '.join(artist['genres']).title()}")
            else:
                st.text("Genres: N/a")
            st.text(f"Popularity: {100 - artist["popularity"]}")
            st.text(f"Top Tracks:\n{'\n'.join(get_top_tracks(artist['id'], token, SONG_DATA_FILE))}")

