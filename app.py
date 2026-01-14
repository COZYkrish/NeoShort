from flask import Flask, render_template, request, redirect
import json
import os
import random
import string

app = Flask(__name__)

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

    urls = load_urls()

    # Check if URL already exists
    for code, saved_url in urls.items():
        if saved_url == long_url:
            short_url = request.host_url + code
            return render_template("index.html", short_url=short_url)

    short_code = generate_short_code()
    urls[short_code] = long_url
    save_urls(urls)

    short_url = request.host_url + short_code
    return render_template("index.html", short_url=short_url)

@app.route("/<short_code>")
def redirect_short_url(short_code):
    urls = load_urls()

    if short_code in urls:
        return redirect(urls[short_code])

    return "Short URL not found", 404

# ======================
# APP RUN
# ======================

if __name__ == "__main__":
    app.run(debug=True)
