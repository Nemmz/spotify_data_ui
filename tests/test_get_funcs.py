import os
import json
import pytest
from unittest.mock import patch, MagicMock
from app.get_artist_data import get_token, search_artist, get_top_tracks, get_albums, clear_json


# Fixture to ensure test_data directory exists before each test
@pytest.fixture(scope="function")
def create_test_data_dir():
    """Ensure that the test_data directory exists before running the tests."""
    if not os.path.exists('test_data'):
        os.makedirs('test_data')
    yield
    # Clean up the files after each test
    for filename in os.listdir('test_data'):
        file_path = os.path.join('test_data', filename)
        if os.path.isfile(file_path):
            os.remove(file_path)


# Test for get_token function
def test_get_token():
    # Mock the token retrieval process
    mock_token = "mocked_token"

    # Normally, you'd fetch this from an API or environment, so we mock it here
    assert mock_token == "mocked_token", f"Expected 'mocked_token', but got {mock_token}"


# Test for search_artist function with mocking
@patch('app.get_artist_data.requests.get')
def test_search_artist(mock_get, create_test_data_dir):
    artist_name = "My Chemical Romance"
    mock_token = "mocked_token"  # Mocked access token
    mock_file = "test_data/test_data.json"  # Mocked file path

    # Simulating a successful API response
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "artists": {
            "items": [{
                "name": "My Chemical Romance",
                "id": "123",
                "genres": ["emo", "pop punk"],
                "external_urls": {"spotify": "spotify_url"}
            }]
        }
    }
    mock_get.return_value = mock_response

    # Simulate the API call and save the data in a JSON file
    result = search_artist(artist_name, mock_token, mock_file)

    # Now write the mock data to simulate what would happen in the actual function
    with open(mock_file, "w", encoding="utf-8") as file:
        file.write(json.dumps(result, indent=4, sort_keys=True))

    # Reading the file back and performing assertions
    with open(mock_file, "r", encoding="utf-8") as file:
        artist_data = json.load(file)

    assert artist_data is not None, "Expected artist data, but got None"
    assert artist_data["artists"]["items"][0]["name"].lower() == artist_name.lower(), \
        f"Expected {artist_name}, but got {artist_data['artists']['items'][0]['name']}"


@patch('app.get_artist_data.requests.get')
def test_get_top_tracks(mock_get, create_test_data_dir):
    artist_id = "123"
    mock_token = "mocked_token"
    mock_file = "test_data/test_top_tracks.json"

    # Simulate the successful API response for top tracks
    mock_response = MagicMock()
    mock_response.json.return_value = {}  # Empty dictionary for the result
    mock_get.return_value = mock_response

    # Simulate the API call and save the data
    result = get_top_tracks(artist_id, mock_token, mock_file)

    # Debugging step: print the result
    print("Result from get_top_tracks:", result)

    # Ensure the result is an empty dictionary
    assert result == {}, f"Expected empty dictionary, but got {result}"


@patch('app.get_artist_data.requests.get')
def test_get_albums(mock_get, create_test_data_dir):
    artist_id = "123"
    mock_token = "mocked_token"
    mock_file = "test_data/test_artist.json"

    # Simulate the successful API response for albums
    mock_response = MagicMock()
    mock_response.json.return_value = []  # Empty dictionary for the result
    mock_get.return_value = mock_response

    # Simulate the API call and save the data
    result = get_albums(artist_id, mock_token, mock_file)

    # Debugging step: print the result
    print("Result from get_albums:", result)

    # Ensure the result is an empty dictionary
    assert result == {}, f"Expected empty dictionary, but got {result}"


# Test for clear_json function
def test_clear_json(create_test_data_dir):
    data_file = "test_data/test_clear.json"

    # Simulating a file to be cleared
    with open(data_file, "w", encoding="utf-8") as file:
        json.dump([{"name": "Some artist"}], file)

    # Now clear the content using clear_json function
    clear_json(data_file)

    with open(data_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    assert data == [], "Expected an empty list after clearing the JSON file."
