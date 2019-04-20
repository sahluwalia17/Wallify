from flask import Flask, render_template, redirect, request
import webbrowser
import requests
from urllib.parse import quote
import urllib.request
import json
import pyrebase

app = Flask(__name__)

clientId = "45ba6741126e4af1b9c7fef7f6bd7568"
clientSecret = "be75f467163b4812aee28c45e3bcf860"
baseURL = "https://accounts.spotify.com/authorize"
redirectURL = "http://127.0.0.1:5000/callback/q"
scope = "user-top-read"
spotifyTokenURL = "https://accounts.spotify.com/api/token"
spotifyAPI = "https://api.spotify.com/v1/me/top/tracks?limit=50"

config = {
    "apiKey": None,
    "authDomain": "wallify-bea20.firebaseapp.com",
    "databaseURL": "https://wallify-bea20.firebaseio.com",
    "projectId": "wallify-bea20",
    "storageBucket": "wallify-bea20.appspot.com",
    "messagingSenderId": "974113509801"
}

with open ("config.txt") as f:
    apiKey = str(f.readline())
    config["apiKey"] = apiKey

fb = pyrebase.initialize_app(config)
authentication = fb.auth

@app.route("/")
def index():#add authentication part here
    return render_template("index.html")

@app.route("/authorize")
def authorize():
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
    auth_token = request.args['code']

    code_payload = {
                "grant_type": "authorization_code",
                "code": str(auth_token),
                "redirect_uri": redirectURL,
                "client_id": clientId,
                "client_secret": clientSecret
            }

    post_request = requests.post(spotifyTokenURL, data=code_payload)
    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]
    authorization_header = {"Accept":"application/json", "Authorization":"Bearer {}".format(access_token)}
    top_tracks = requests.get(spotifyAPI, headers = authorization_header)
    tracks_data = json.loads(top_tracks.text)

    links = []
    filteredlinks = []
    for x in range(0,50):
            for y in range(0,1):
                    links.append(tracks_data["items"][x]["album"]["images"][1]["url"])

    for i in links:
            if i not in filteredlinks:
                    filteredlinks.append(i)

    print(filteredlinks)

    for x in range(0,18):
        link = filteredlinks[x]
        urllib.request.urlretrieve(link, "./static/" + str(x+1) + ".jpg")

    return render_template("wallify.html")

if __name__ == "__main__":
    app.run(debug=True)
