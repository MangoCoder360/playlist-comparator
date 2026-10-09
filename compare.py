import re
from collections import defaultdict

from models import Playlist, PlaylistComparison, Song


def normalize_text(value: str) -> str:
	"""Normalize text for matching songs across music services."""
	normalized = re.sub(r"[^a-z0-9]+", " ", value.casefold())
	return " ".join(normalized.split())


def normalize_artists(value: str) -> tuple[str, ...]:
	artist_names = re.split(
		r",|&|\b(?:feat\.?|ft\.?|featuring)\b",
		value,
		flags=re.IGNORECASE,
	)
	return tuple(
		sorted(
			normalized_name
			for artist_name in artist_names
			if (normalized_name := normalize_text(artist_name))
		)
	)


def song_key(song: Song) -> tuple[str, tuple[str, ...]]:
    return normalize_text(song.name), normalize_artists(song.artist)


def compare_playlists(
	first: Playlist,
	second: Playlist,
) -> PlaylistComparison:
	songs_by_key: dict[tuple[str, tuple[str, ...]], list[Song]] = defaultdict(list)
	for song in first.songs:
		songs_by_key[song_key(song)].append(song)

	shared: list[tuple[Song, Song]] = []
	only_in_second: list[Song] = []

	for song in second.songs:
		matching_songs = songs_by_key[song_key(song)]
		if matching_songs:
			shared.append((matching_songs.pop(0), song))
		else:
			only_in_second.append(song)

	only_in_first = [
		song
		for remaining_songs in songs_by_key.values()
		for song in remaining_songs
	]

	return PlaylistComparison(
		shared=shared,
		only_in_first=only_in_first,
		only_in_second=only_in_second,
	)
