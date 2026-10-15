import uuid
from urllib.parse import urlparse

from flask import Flask, render_template, request, redirect, url_for

import am_funcs
import spotify_funcs
from compare import compare_playlists

RESULTS_CACHE = {}

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/process")
def process():
	first_url = request.args.get("playlist_one", "").strip()
	second_url = request.args.get("playlist_two", "").strip()

	if not first_url or not second_url:
		return render_template(
			"results.html",
			heading="Invalid request",
			error="Two playlist links are required.",
		), 400

	try:
		first = fetch_playlist(first_url)
		second = fetch_playlist(second_url)
		comparison = compare_playlists(first, second)
	except Exception:
		return render_template(
			"results.html",
			heading="We couldn't compare those.",
			error="Unable to process one or both playlists. Check links and try again.",
		), 502

	result_uuid = str(uuid.uuid4())
	RESULTS_CACHE[result_uuid] = comparison
	return redirect(url_for("results", id=result_uuid))

@app.route("/results")
def results():
	result_uuid = request.args.get("id")
	if not result_uuid or result_uuid not in RESULTS_CACHE:
		return render_template(
			"results.html",
			heading="Page not found",
			error="This result is no longer available. Please try again",
		), 404
	else:
		comparison = RESULTS_CACHE[result_uuid]
		return render_template("results.html", comparison=comparison)

def fetch_playlist(url: str):
	host = (urlparse(url).hostname or "").lower().removeprefix("www.")
	if host == "open.spotify.com":
		return spotify_funcs.get_playlist_from_url(url)
	if host == "music.apple.com":
		return am_funcs.get_playlist_from_url(url)
	raise ValueError("Unsupported playlist service")

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8081)