import requests, os
from models import *
from am_get_token import get_dev_token
#import dotenv

#dotenv.load_dotenv()
#APPLE_MUSIC_AUTH_TOKEN = os.getenv("APPLE_MUSIC_AUTH_TOKEN")
try:
    APPLE_MUSIC_AUTH_TOKEN = get_dev_token()
except Exception as e:
    raise Exception(f"Failed to retrieve Apple Music dev token: {e}")

def format_playlist(playlist_id: str):
    auth_token = APPLE_MUSIC_AUTH_TOKEN
    url = f"https://amp-api.music.apple.com/v1/catalog/us/playlists/{playlist_id}"
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Origin": "https://music.apple.com"
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch playlist: {response.status_code} - {response.text}")

    playlist_data = response.json().get("data", [{}])[0]

    formatted_playlist = {
        "name": playlist_data.get("attributes", {}).get("name", "Untitled"),
        "author": playlist_data.get("attributes", {}).get("curatorName", "Unknown"),
        "songCount": 0
    }

    playlist_songs = []
    tracks = playlist_data.get("relationships", {}).get("tracks", {})

    for item in tracks.get("data", []):
        song = {
            "name": item.get("attributes", {}).get("name", "Unknown Track"),
            "artist": item.get("attributes", {}).get("artistName", "Unknown Artist"),
            "album": item.get("attributes", {}).get("albumName", "Unknown Album"),
            "duration": item.get("attributes", {}).get("durationInMillis", 0),
            "appleMusicId": item.get("id", "")
        }
        playlist_songs.append(song)

    if tracks.get("next"):
        next_url = tracks["next"]
        while next_url:
            response = requests.get("https://amp-api.music.apple.com"+next_url, headers=headers)
            if response.status_code != 200:
                raise Exception(f"Failed to fetch next page of tracks: {response.status_code} - {response.text}")
            next_page_data = response.json()
            for item in next_page_data.get("data", []):
                song = {
                    "name": item.get("attributes", {}).get("name", "Unknown Track"),
                    "artist": item.get("attributes", {}).get("artistName", "Unknown Artist"),
                    "album": item.get("attributes", {}).get("albumName", "Unknown Album"),
                    "duration": item.get("attributes", {}).get("durationInMillis", 0),
                    "appleMusicId": item.get("id", "")
                }
                playlist_songs.append(song)
            next_url = next_page_data.get("next")

    formatted_playlist["songs"] = playlist_songs
    formatted_playlist["songCount"] = len(playlist_songs)
    return formatted_playlist

def get_playlist_from_url(apple_music_url: str):
    """
    This is the primary function for getting a playlist from Apple Music. It takes the playlist URL and returns a Playlist object with the playlist's data.
    """
    playlist_id = apple_music_url.split("/")[-1].split("?")[0]
    formatted = format_playlist(playlist_id)
    return convert_to_playlist_object(formatted)

def convert_to_playlist_object(playlist_data: dict) -> Playlist:
    songs = [
        Song(
            name=song["name"],
            artist=song["artist"],
            album=song["album"],
            duration=song["duration"],
            source=Source.APPLE_MUSIC,
            source_id=song.get("appleMusicId", "")
        )
        for song in playlist_data.get("songs", [])
    ]
    return Playlist(
        name=playlist_data.get("name", "Untitled"),
        author=playlist_data.get("author", "Unknown"),
        songs=songs
    )