from flask import Flask, render_template, request, redirect
import json
import os
import random
import string
import re

app = Flask(__name__)


def is_valid_url(url):
    regex = re.compile(
        r'^(https?|ftp)://'        # protocol
        r'([A-Za-z0-9-]+\.)+'      # domain
        r'[A-Za-z]{2,}'            # TLD
        r'(:\d+)?(/.*)?$'          # port & path
    )
    return re.match(regex, url) is not None


DATA_FILE = "data/urls.json"

def load_urls():
    if not os.path.exists(DATA_FILE):
        return {}

    with open(DATA_FILE, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return {}

def save_urls(urls):
    with open(DATA_FILE, "w") as file:
        json.dump(urls, file, indent=4)

# ======================
# SHORT CODE GENERATOR
# ======================
def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/shorten", methods=["POST"])
def shorten_url():
    long_url = request.form.get("url")

    if not long_url:
        return render_template("index.html", error="Please enter a URL")

    if not is_valid_url(long_url):
        return render_template(
            "index.html",
            error="Invalid URL. Please include http:// or https://"
        )

    urls = load_urls()

    for code, data in urls.items():
        if isinstance(data, str):
            urls[code] = {
                "url": data,
                "clicks": 0
            }
            data = urls[code]

        if data["url"] == long_url:
            short_url = request.host_url + code
            save_urls(urls)
            return render_template("index.html", short_url=short_url)

    short_code = generate_short_code()
    urls[short_code] = {
        "url": long_url,
        "clicks": 0
    }

    save_urls(urls)

    short_url = request.host_url + short_code
    return render_template("index.html", short_url=short_url)

@app.route("/<short_code>")
def redirect_short_url(short_code):
    urls = load_urls()

    if short_code in urls:
        if isinstance(urls[short_code], str):
            urls[short_code] = {
                "url": urls[short_code],
                "clicks": 0
            }

        urls[short_code]["clicks"] += 1
        save_urls(urls)

        return redirect(urls[short_code]["url"])

    return "Short URL not found", 404


if __name__ == "__main__":
    app.run(debug=True)
