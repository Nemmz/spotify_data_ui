"""
Author: Isaac Jarrells
Date: March 14, 2025,
Purpose: To grab the important data from Spotify's API. The data will vary and could be changed
         in the future. At the time of creation they are:
Resources: Spotify Development Examples
"""
import json
import urllib.parse
from dateutil import tz
import requests
import streamlit as st
from datetime import datetime

CLIENT_ID = st.secrets["SPOTIFY_CLIENT_ID"]
CLIENT_SECRET = st.secrets["SPOTIFY_CLIENT_SECRET"]

def get_token() -> str | None:
    """Grabs an access token from Spotify to allow access to API data."""
    token_url = "https://accounts.spotify.com/api/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }

    try:
        response = requests.post(token_url, headers=headers, data=data)
        response.raise_for_status()
        return response.json().get("access_token")
    except requests.exceptions.RequestException as err:
        return None


def search_artist(artist: str, access_token: tuple, data_file: str) -> dict | None:
    """Uses artist name to search for Artist ID to display data."""
    headers = {"Authorization": f"Bearer {access_token}"}
    query = urllib.parse.quote(artist)
    search_url = f"https://api.spotify.com/v1/search?q={query}&type=artist&limit=1"

    try:
        artist_data = requests.get(search_url, headers=headers, timeout=5).json()

        if artist_data:
            with open(data_file, "w", encoding="utf-8") as file:
                file.write(json.dumps(artist_data, indent=4, sort_keys=True))
            return artist_data
        with open(data_file, "r", encoding="utf-8") as file:
            artist_data = json.load(file)
        st.warning("Using cached artist data", icon="⚠️")
        return artist_data

    except TypeError as error:
        st.error(str(error), icon="🛠️")
        print(error)
    except OSError as error:
        st.error(str(error), icon="🛠️")
        print(error)
    st.error("No artist data found.", icon="❌")
    return {}


def last_updated() -> str:
    """Returns the last updated date for an artist."""
    current_time = datetime.now(tz.gettz("America/New_York"))
    current_time = current_time.replace(tzinfo=tz.gettz('UTC')).astimezone(tz.gettz("MST"))
    return current_time.strftime("%B %d, %Y, %I:%M %p")