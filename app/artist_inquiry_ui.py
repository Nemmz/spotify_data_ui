"""
Author:
Date:
Purpose:
Resources:
"""
import streamlit as st
import time
from get_artist_data import get_token, search_artist

DATA_FILE = "app/data/artist.json"
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
    progress_bar = st.progress(0, text="Searching for Artist...")
    for percent_complete in range(100):
        time.sleep(0.01)
        progress_bar.progress(percent_complete + 1, text="Searching for Artist...")
    time.sleep(1)
    progress_bar.empty()
    with right:
        try:
            data = search_artist(text_input, token, DATA_FILE)
            artist = data["artists"]["items"][0]
            right = right.container(border=True).image(artist["images"][0]["url"], use_container_width=True)
            left = st.write(f"Popularity: {100-artist["popularity"]}")

        except Exception as e:
            st.write(e)
