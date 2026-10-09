from dataclasses import dataclass
from enum import Enum

class Source(str, Enum):
    SPOTIFY = "spotify"
    APPLE_MUSIC = "apple_music"

@dataclass
class Song:
    name: str
    artist: str
    album: str
    duration: int
    source: Source
    source_id: str = ""

@dataclass
class Playlist:
    name: str
    author: str
    songs: list[Song]

@dataclass
class PlaylistComparison:
    shared: list[tuple[Song, Song]]
    only_in_first: list[Song]
    only_in_second: list[Song]