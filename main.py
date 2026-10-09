from urllib.parse import urlparse

from flask import Flask, render_template, request

import am_funcs
import spotify_funcs
from compare import compare_playlists

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")


@app.route("/results")
def results():
	first_url = request.args.get("playlist_one", "").strip()
	second_url = request.args.get("playlist_two", "").strip()

	if not first_url or not second_url:
		return render_template(
			"results.html",
			error="Two playlist links are required.",
		), 400

	try:
		first = fetch_playlist(first_url)
		second = fetch_playlist(second_url)
		comparison = compare_playlists(first, second)
	except Exception:
		return render_template(
			"results.html",
			error="We could not load one of those playlists. Check the links and try again.",
		), 502

	return render_template("results.html", comparison=comparison)


def fetch_playlist(url: str):
	host = (urlparse(url).hostname or "").lower().removeprefix("www.")
	if host == "open.spotify.com":
		return spotify_funcs.get_playlist_from_url(url)
	if host == "music.apple.com":
		return am_funcs.get_playlist_from_url(url)
	raise ValueError("Unsupported playlist service")

if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0", port=8080)