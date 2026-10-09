from spotapi import PublicPlaylist
from models import Playlist, Song, Source

def format_playlist(public_playlist: PublicPlaylist):
    info_raw = public_playlist.get_playlist_info()
    info = info_raw.get("data", {}).get("playlistV2", {})
    paginated_playlist = public_playlist.paginate_playlist()

    formatted_playlist = {
        "name": info.get("name", "Untitled"),
        "author": info.get("ownerV2", {}).get("data", {}).get("name", "Unknown"),
        "songCount": info.get("content", {}).get("totalCount", 0)
    }

    playlist_songs = []
    for page in paginated_playlist:
        for item in page.get("items", []):
            track_info = item.get("itemV2", {}).get("data", {})
            artist_names = [
                artist.get("profile", {}).get("name", "")
                for artist in track_info.get("artists", {}).get("items", [])
            ]
            song = {
                "name": track_info.get("name", "Unknown Track"),
                "artist": ", ".join(name for name in artist_names if name)
                or "Unknown Artist",
                "album": track_info.get("albumOfTrack", {}).get("name", "Unknown Album"),
                "duration": track_info.get("trackDuration", {}).get("totalMilliseconds", 0),
                "spotifyUri": track_info.get("uri", "")
            }
            playlist_songs.append(song)

    formatted_playlist["songs"] = playlist_songs
    return formatted_playlist

def get_playlist_from_url(spotify_url: str):
    """
    This is the primary function for getting a playlist from Spotify. It takes the playlist URL and returns a Playlist object with the playlist's data.
    """
    public_playlist = PublicPlaylist(spotify_url)
    formatted = format_playlist(public_playlist)
    return convert_to_playlist_object(formatted)

def convert_to_playlist_object(playlist_data: dict) -> Playlist:
    songs = [
        Song(
            name=song["name"],
            artist=song["artist"],
            album=song["album"],
            duration=song["duration"],
            source=Source.SPOTIFY,
            source_id=song.get("spotifyUri", "")
        )
        for song in playlist_data.get("songs", [])
    ]
    return Playlist(
        name=playlist_data.get("name", "Untitled"),
        author=playlist_data.get("author", "Unknown"),
        songs=songs
    )