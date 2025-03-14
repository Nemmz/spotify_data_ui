"""
Author: Isaac Jarrells
Date: March 14, 2025,
Purpose: To grab the important data from Spotify's API. The data will vary and could be changed
         in the future. At the time of creation they are:
Resources: Spotify Development Examples
"""

import urllib
import urllib.parse
import requests

# Spotify API credentials
CLIENT_ID = "e186a07c48384716bf0ab5da7d7ba70c"
CLIENT_SECRET = "4c103175d97747ed840b5233147a9d2b"


def get_token() -> None:
    """Grabs an access token from Spotify to allow access to API data."""
    token_url = "https://accounts.spotify.com/api/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }

    response = requests.post(token_url, headers=headers, data=data)
    return response.json().get("access_token")


def search_artist(artist, access_token) -> tuple | None:
    """Uses artist name to search for Artist ID to display data."""
    headers = {"Authorization": f"Bearer {access_token}"}
    query = urllib.parse.quote(artist)
    search_url = f"https://api.spotify.com/v1/search?q={query}&type=artist&limit=1"
    response = requests.get(search_url, headers=headers)
    data = response.json()
    #   print(response.json()) *Deeper Dive for JSON debugging

    if data["artists"]["items"]:
        artist = data["artists"]["items"][0]
        return (artist["id"], artist["name"], artist["external_urls"]["spotify"], artist["followers"]["total"],artist["popularity"])
    return ()

token = get_token()
ARTIST_NAME = "Post Malone"
artist_id, name, url, followers, popularity = search_artist(ARTIST_NAME, token)

# Name and Genre, Popularity, Top 3 Songs, most recent album, and Followers
"""Ensures that the artist is received"""
if artist_id:
    print(f"Artist: {ARTIST_NAME}")
    print(f"Artist ID: {artist_id}")
    print(f"Artist URL: {url}")
    print(f"Followers: {followers}")
    print(f"Popularity: {popularity}")
else:
    print("No Artist found.")
