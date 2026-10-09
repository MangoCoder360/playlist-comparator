import requests, re

def get_dev_token():
    # fetch AM homepage to search for index.js url
    try:
        homepage_response = requests.get("https://music.apple.com/")
        if homepage_response.status_code == 200:
            homepage = homepage_response.text
        else:
            raise Exception(f"Failed to fetch the homepage, status code: {homepage_response.status_code}")
    except Exception as e:
        raise Exception(f"Error fetching the homepage: {e}")

    index_js_uri_match = re.search(
        r"/(assets/index[~-][^/\"]+\.js)",
        homepage,
    )

    if index_js_uri_match:
        index_js_url = f"https://music.apple.com/{index_js_uri_match.group(1)}"
    else:
        raise Exception("Could not find the index.js URL in the homepage.")

    try:
        response = requests.get(index_js_url)
    except Exception as e:
        raise Exception(f"Error fetching the index.js file: {e}")

    # search for the dev token in the index.js content and return it if found
    if response.status_code == 200:
        content = response.text
        token_match = re.search(r'"(eyJ[A-Za-z0-9\-_]+\.eyJ[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+)"', content)
        if token_match:
            dev_token = token_match.group(1)
            return dev_token
        else:
            raise Exception("Could not find the dev token in the response.")
    else:
        raise Exception(f"Failed to fetch the page, status code: {response.status_code}")