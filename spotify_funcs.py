from spotapi import PublicPlaylist

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
            song = {
                "name": track_info.get("name", "Unknown Track"),
                "artist": track_info.get("artists", {}).get("items", [{}])[0].get("profile", {}).get("name", "Unknown Artist"),
                "album": track_info.get("albumOfTrack", {}).get("name", "Unknown Album"),
                "duration": track_info.get("trackDuration", {}).get("totalMilliseconds", 0),
                "spotifyUri": track_info.get("uri", "")
            }
            playlist_songs.append(song)

    formatted_playlist["songs"] = playlist_songs
    return formatted_playlist

def get_playlist_from_url(spotify_url: str):
    public_playlist = PublicPlaylist(spotify_url)
    return format_playlist(public_playlist)