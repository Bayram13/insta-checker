from flask import Flask, render_template, request
import requests, random, string

app = Flask(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}
INSTAGRAM_PROFILE_URL = "https://www.instagram.com/{}/"

def random_5_letter():
    return ''.join(random.choices(string.ascii_lowercase, k=5))

def check_username(username):
    try:
        resp = requests.head(INSTAGRAM_PROFILE_URL.format(username), headers=HEADERS, allow_redirects=True, timeout=8)
        if resp.status_code == 404:
            return True
        if resp.status_code == 200:
            return False
        resp = requests.get(INSTAGRAM_PROFILE_URL.format(username), headers=HEADERS, timeout=8)
        return resp.status_code == 404
    except requests.RequestException:
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    username = ""
    if request.method == "POST":
        if request.form.get("action") == "random":
            username = random_5_letter()
            result = check_username(username)
        else:
            username = request.form.get("username", "").strip().lower()
            if len(username) == 5:
                result = check_username(username)
            else:
                result = "length_error"
    return render_template("index.html", username=username, result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
