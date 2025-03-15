"""
Author: Isaac Jarrells
Date: March 14, 2025,
Purpose: To grab the important data from Spotify's API. The data will vary and could be changed
         in the future. At the time of creation they are:
Resources: Spotify Development Examples
"""
import json
import urllib.parse
from wsgiref import headers

from dateutil import tz
import requests
import streamlit as st
from datetime import datetime

CLIENT_ID = st.secrets["SPOTIFY_CLIENT_ID"]
CLIENT_SECRET = st.secrets["SPOTIFY_CLIENT_SECRET"]

def get_token() -> str | None:
    """Grabs an access token from Spotify to allow access to API data."""
    token_url = "https://accounts.spotify.com/api/token"
    token_headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }

    try:
        response = requests.post(token_url, headers=token_headers, data=data)
        response.raise_for_status()
        return response.json().get("access_token")
    except requests.exceptions.RequestException as err:
        return None


def search_artist(artist: str, access_token: tuple, data_file: str) -> dict | None:
    """Uses artist name to search for Artist ID to display data."""
    search_artist_headers = {"Authorization": f"Bearer {access_token}"}
    query = urllib.parse.quote(artist)
    search_url = f"https://api.spotify.com/v1/search?q={query}&type=artist&limit=1"

    try:
        artist_data = requests.get(search_url, headers=search_artist_headers, timeout=5).json()

        if artist_data and artist_data["artists"]["items"][0]["name"].lower() == artist.lower():
            with open(data_file, "w", encoding="utf-8") as file:
                file.write(json.dumps(artist_data, indent=4, sort_keys=True))
            return artist_data
        else:
            clear_json(data_file)
        with open(data_file, "r", encoding="utf-8") as file:
            artist_data = json.load(file)
        st.warning("Invalid Input: Ensure the Name is Exactly As Appears on Spotify...",icon="⚠️")
        return artist_data

    except TypeError as error:
        st.error(str(error), icon="🛠️")
        print(error)
    except OSError as error:
        st.error(str(error), icon="🛠️")
        print(error)
    st.error("No artist data found.", icon="❌")
    return {}


def get_top_tracks(artist_id: str, access_token: tuple, data_file: str) -> dict | list:
    """Grabs the top songs from an artist using the Artist ID and will put into a json"""
    top_tracks_url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks"
    track_headers= {"Authorization": f"Bearer {access_token}"}
    try:
        top_tracks_data = requests.get(top_tracks_url, headers=track_headers, timeout=5).json()
        top_tracks = [f"{idx + 1}. {track['name']}" for idx, track in enumerate(top_tracks_data["tracks"])]

        if top_tracks:
            with open(data_file, "w", encoding="utf-8") as file:
                file.write(json.dumps(top_tracks, indent=4, sort_keys=True))
            return top_tracks
        else:
            clear_json(data_file)
        with open(data_file, "r", encoding="utf-8") as file:
            top_tracks = json.load(file)
        return top_tracks
    except requests.exceptions.RequestException as err:
        st.error(str(err), icon="🛠️")
    st.error("No songs found.", icon="❌")
    return {}


def last_updated() -> str:
    """Returns the last updated date for an artist."""
    current_time = datetime.now(tz.gettz("America/New_York"))
    current_time = current_time.replace(tzinfo=tz.gettz('UTC')).astimezone(tz.gettz("MST"))
    return current_time.strftime("%B %d, %Y, %I:%M %p")

def clear_json(data_file)-> None:
    """Clears the JSON file from the previous searches"""
    with open(data_file, "w", encoding="utf-8") as file:
        json.dump([],file)