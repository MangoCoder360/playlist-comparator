# playlist comparator

Available at [playlist-comparator.reuben.zip](https://playlist-comparator.reuben.zip)

## What is it?

A simple web tool to find common songs between Apple Music or Spotify playlists. I wanted to create this to make it easier to find songs that I have in common with friends, by placing each of our main playlists into the site.

## Features

- Supports both Apple Music and Spotify playlists
- Finds shared tracks in both playlists
- Uses standard playlist URLs
- Simple and clean web interface
- Lightweight and minimal

## How it works

- Paste playlist URLs from either service into the form on the site's landing page
- Service is automatically detected from URL
- Playlist data is fetched and compared seamlessly
- Results page is rendered with a list of shared songs


## Tech stack

I wanted to keep the codebase as minimal as possible while accomplishing my goal. The frontend is vanilla HTML, CSS, and JS which is rendered by the backend server using Python (3.10) and Flask. The API connection to Apple Music is done via a custom implementation, and for Spotify, it uses the SpotAPI project to fetch playlist data.

## Self-hosting/installation

The code is certainly not production-ready, but it is possible to host your own instance of this application. Tested with Python 3.10.16

### Linux/macOS

Clone the repository to an empty directory, and create a new Python virtual environment with all of the required dependencies.

```bash
git clone https://github.com/MangoCoder360/playlist-comparator.git
cd playlist-comparator
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Flask is configured to run on port 8081. This can be changed at the bottom of `main.py` if needed.

Run the application with the following command:

```bash
python main.py
```

### Windows

It's theoretically possible to host on Windows, and I predict it would work fine, but I have not tested it, so attempt at your own risk.

## Contributing

I don't plan to support and continue updating this project long-term, but pull requests are welcome for bugfixes and security patches.

## License

This project is released under the Creative Commons CC BY-NC-SA 4.0 license. See details [here](https://creativecommons.org/licenses/by-nc-sa/4.0/).