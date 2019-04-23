from flask import Flask, render_template, redirect, request, url_for
from PIL import Image
import webbrowser
import requests
from urllib.parse import quote
import urllib.request
import json

app = Flask(__name__)

clientId = "45ba6741126e4af1b9c7fef7f6bd7568"
clientSecret = "be75f467163b4812aee28c45e3bcf860"
baseURL = "https://accounts.spotify.com/authorize"
redirectURL = "http://127.0.0.1:5000/callback/q"
scope = "user-top-read"
spotifyTokenURL = "https://accounts.spotify.com/api/token"
spotifyAPI = "https://api.spotify.com/v1/me/top/tracks?time_range=short_term&limit=50"
data = []

@app.route("/")
def index():
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

    return redirect(url_for('wallify'))

@app.route("/wallify")
def wallify():
    return render_template("wallify.html")

@app.route("/receive",methods=["POST"])
def get_data():
    if request.method == "POST":
        ints = request.get_json()
        data = ints.get("ints")

    image1 = Image.open("./static/"+str(data[0]) + ".jpg")
    image2 = Image.open("./static/"+str(data[1]) + ".jpg")
    image3 = Image.open("./static/"+str(data[2]) + ".jpg")

    image4 = Image.open("./static/"+str(data[3]) + ".jpg")
    image5 = Image.open("./static/"+str(data[4]) + ".jpg")
    image6 = Image.open("./static/"+str(data[5]) + ".jpg")

    image7 = Image.open("./static/"+str(data[6]) + ".jpg")
    image8 = Image.open("./static/"+str(data[7]) + ".jpg")
    image9 = Image.open("./static/"+str(data[8]) + ".jpg")

    image10 = Image.open("./static/"+str(data[9]) + ".jpg")
    image11 = Image.open("./static/"+str(data[10]) + ".jpg")
    image12 = Image.open("./static/"+str(data[11]) + ".jpg")

    image13 = Image.open("./static/"+str(data[12]) + ".jpg")
    image14 = Image.open("./static/"+str(data[13]) + ".jpg")
    image15 = Image.open("./static/"+str(data[14]) + ".jpg")

    image16 = Image.open("./static/"+str(data[15]) + ".jpg")
    image17 = Image.open("./static/"+str(data[16]) + ".jpg")
    image18 = Image.open("./static/"+str(data[17]) + ".jpg")

    (width1, height1) = image1.size
    (width2, height2) = image2.size
    (width3, height3) = image3.size
    (width4, height4) = image4.size
    (width5, height5) = image5.size
    (width6, height6) = image6.size

    result_width = width1
    result_height = height1 + height2 + height3
    
    return "",200

if __name__ == "__main__":
    app.run(debug=True)
