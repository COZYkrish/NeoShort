from flask import Flask, render_template, request, redirect
from datetime import datetime, timedelta
import json
import os
import random
import string
import re

app = Flask(__name__)

# ======================
# URL VALIDATION
# ======================
def is_valid_url(url):
    regex = re.compile(
        r'^(https?|ftp)://'        # protocol
        r'([A-Za-z0-9-]+\.)+'      # domain
        r'[A-Za-z]{2,}'            # TLD
        r'(:\d+)?(/.*)?$'          # port & path
    )
    return re.match(regex, url) is not None

# ======================
# STORAGE CONFIG
# ======================
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

# ======================
# ROUTES
# ======================

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

    # 🔁 Existing URL check + backward compatibility
    for code, data in urls.items():
        if isinstance(data, str):
            urls[code] = {
                "url": data,
                "clicks": 0,
                "expires_at": None
            }
            data = urls[code]

        if "expires_at" not in data:
            data["expires_at"] = None

        if data["url"] == long_url:
            short_url = request.host_url + code
            save_urls(urls)
            return render_template(
                "index.html",
                short_url=short_url,
                clicks=data["clicks"]
            )

    # 🆕 Create new short URL
    short_code = generate_short_code()
    expires_at = datetime.now() + timedelta(days=7)

    urls[short_code] = {
        "url": long_url,
        "clicks": 0,
        "expires_at": expires_at.isoformat()
    }

    save_urls(urls)

    short_url = request.host_url + short_code
    return render_template(
        "index.html",
        short_url=short_url,
        clicks=0
    )

@app.route("/<short_code>")
def redirect_short_url(short_code):
    urls = load_urls()

    if short_code not in urls:
        return render_template(
            "error.html",
            message="This short URL does not exist or was removed."
        ), 404

    data = urls[short_code]

    # Backward compatibility
    if isinstance(data, str):
        data = {
            "url": data,
            "clicks": 0,
            "expires_at": None
        }
        urls[short_code] = data

    # ⏳ Expiry check
    if data["expires_at"]:
        expiry_time = datetime.fromisoformat(data["expires_at"])
        if datetime.now() > expiry_time:
            return render_template(
                "error.html",
                message="This short link has expired."
            ), 410

    # 📊 Increment clicks
    # data["clicks"] += 1
    # save_urls(urls)

    return redirect(data["url"])


# ======================
# APP RUN
# ======================
if __name__ == "__main__":
    app.run(debug=True)
