from flask import Flask, render_template, redirect
from urllib.parse import quote
import webbrowser
import requests

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/authorize")
def authorize():
    clientId = "45ba6741126e4af1b9c7fef7f6bd7568"
    baseURL = "https://accounts.spotify.com/authorize"
    redirectURL = "http://127.0.0.1:5000/callback/q"
    scope = "user-top-read"

    auth_query_parameters = {
        "response_type": "code",
        "redirect_uri": redirectURL,
        "scope": scope,
        "client_id": clientId
    }

    url_args = "&".join(["{}={}".format(key, quote(val)) for key, val in auth_query_parameters.items()])
    auth_url = "{}/?{}".format(baseURL, url_args)

    return redirect(auth_url)

@app.route("/callback/q")
def callback():
    return render_template("wallify.html")

if __name__ == "__main__":
    app.run(debug=True)
