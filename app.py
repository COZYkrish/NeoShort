from flask import Flask, render_template
import json
import os
app = Flask(__name__)

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



@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
