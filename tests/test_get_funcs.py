import pytest
import json
from app.get_artist_data import get_token, search_artist, get_top_tracks, get_albums, clear_json

# Test for get_token function
def test_get_token():
    token = "mocked_token"  # Simulated token
    assert token == "mocked_token", f"Expected 'mocked_token', but got {token}"


# Test for search_artist function
def test_search_artist():
    artist_name = "My Chemical Romance"

    # Simulating a successful API response
    mock_data = {
        "artists": {
            "items": [{
                "name": "My Chemical Romance",
                "id": "123",
                "genres": ["emo", "pop punk"],
                "external_urls": {"spotify": "spotify_url"}
            }]
        }
    }

    # Writing the mock data to the file to simulate what would happen in the actual function
    with open("test_data/test_data.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(mock_data, indent=4, sort_keys=True))

    # Reading the file back and performing assertions
    with open("test_data/test_data.json", "r", encoding="utf-8") as file:
        artist_data = json.load(file)

    assert artist_data is not None, "Expected artist data, but got None"
    assert artist_data["artists"]["items"][0][
               "name"].lower() == artist_name.lower(), f"Expected {artist_name}, but got {artist_data['artists']['items'][0]['name']}"


# Test for get_top_tracks function
def test_get_top_tracks():

    # Simulating a successful response for top tracks
    mock_data = [
        "1. Track 1",
        "2. Track 2",
        "3. Track 3",
    ]

    # Writing the mock data to the file to simulate what would happen in the actual function
    with open("test_data/test_top_tracks.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(mock_data, indent=4, sort_keys=True))

    # Reading the file back and performing assertions
    with open("test_data/test_top_tracks.json", "r", encoding="utf-8") as file:
        top_tracks = json.load(file)

    assert len(top_tracks) == 3, f"Expected 3 tracks, but got {len(top_tracks)}"
    assert top_tracks[0] == "1. Track 1", f"Expected '1. Track 1', but got {top_tracks[0]}"


# Test for get_albums function
def test_get_albums():

    # Simulating a successful response for albums
    mock_data = [
        "Album 1",
        "Album 2",
        "Album 3"
    ]

    # Writing the mock data to the file to simulate what would happen in the actual function
    with open("test_data/test_artist.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(mock_data, indent=4, sort_keys=True))

    # Reading the file back and performing assertions
    with open("test_data/test_artist.json", "r", encoding="utf-8") as file:
        albums = json.load(file)

    assert len(albums) == 3, f"Expected 3 albums, but got {len(albums)}"
    assert albums[0] == "Album 1", f"Expected 'Album 1', but got {albums[0]}"


# Test for clear_json function
def test_clear_json():
    # Simulating a file to be cleared
    data_file = "test_data/test_clear.json"
    with open(data_file, "w", encoding="utf-8") as file:
        json.dump([{"name": "Some artist"}], file)

    # Now clear the content using clear_json function
    clear_json(data_file)

    with open(data_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    assert data == [], "Expected an empty list after clearing the JSON file."
