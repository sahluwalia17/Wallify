from flask import Flask, render_template, redirect, request, url_for, send_file, jsonify, session
from flask_cachebuster import CacheBuster
import webbrowser
import re
import requests
from urllib.parse import quote
from PIL import Image
import os
import shutil
import time
import urllib.request
import json
import pyrebase
import random
import importlib
import sys
import logging
import re

#Global Declarations
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
user = None #This becomes the user after signing in
clientId = "45ba6741126e4af1b9c7fef7f6bd7568"
clientSecret = "be75f467163b4812aee28c45e3bcf860"
baseURL = "https://accounts.spotify.com/authorize"
#change redirect URL to proper URL
# redirectURL = "http://127.0.0.1:5000/callback/q"
redirectURL = "https://wallifyy.herokuapp.com/callback/q"

scope = "user-top-read"
spotifyTokenURL = "https://accounts.spotify.com/api/token"
refresh_token = ""
refreshTime = 0
token = 0
logging.basicConfig(level=logging.DEBUG)


#need to change this

app.secret_key = clientSecret
#cache-buster config
config = { 'extensions': ['.jpg', '.css'], 'hash_size': 5 }
cache_buster = CacheBuster(config=config)
cache_buster.init_app(app)
config = {
    "apiKey": None,
    "authDomain": "wallify-bea20.firebaseapp.com",
    "databaseURL": "https://wallify-bea20.firebaseio.com",
    "projectId": "wallify-bea20",
    "storageBucket": "wallify-bea20.appspot.com",
    "messagingSenderId": "974113509801"
}
fb = pyrebase.initialize_app(config)
authentication = fb.auth()
database = fb.database()
database_key = None

@app.after_request
def add_header(response):
    #attach no_cache headers
    response.cache_control.public = True
    response.no_cache = True
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    # response.headers['Cache-Control'] = 'public, max-age=0'
    response.cache_control.max_age = 0

    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-store'

    return response

@app.route("/", methods = ["POST", "GET"])
def index():
    #landing page for users
    if request.method ==  "POST":
        if request.form["sign"] == 'Get Started!':
            return redirect(url_for('authorize'))
    return render_template("index.html")

@app.route("/authorize")
def authorize():
    #redirect to spotify authorization
    global refreshTime
    refreshTime = 0

    auth_query_parameters = {
        "response_type": "code",
        "redirect_uri": redirectURL,
        "scope": scope,
        "client_id": clientId
    }

    url_args = "&".join(["{}={}".format(key, quote(val)) for key, val in auth_query_parameters.items()])
    auth_url = "{}/?{}".format(baseURL, url_args)
    return redirect(auth_url)

def spotify(spotifyAPI):
    #authorization succeeded -> download tracks
    global refreshTime
    global refresh_token

    #organize payload to push to API
    if refreshTime > 0:
        code_payload = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": clientId,
            "client_secret": clientSecret,
        }

    dateTime = random.randint(1,100000)

    try:

        authorization_header = {"Accept":"application/json", "Authorization":"Bearer {}".format(session["token"])}
        top_tracks = requests.get(spotifyAPI, headers = authorization_header) #request made and received
        tracks_data = json.loads(top_tracks.text)

        links = []
        filteredlinks = []
        trackinfo = {}

        counter = 0

        try:
            for x in range(0,50):
                    for y in range(0,1):
                            if not tracks_data["items"][x]["album"]["images"]:
                                continue
                            else:
                                albumurl = tracks_data["items"][x]["album"]["images"][0]["url"]
                                if albumurl not in links and counter < 18:
                                    links.append(albumurl)
                                    urlid = tracks_data["items"][x]["id"]
                                    aname = tracks_data["items"][x]["artists"][0]["name"]
                                    artistname = re.sub(r'[^A-Za-z0-9\s$-_.+!*(),\']', '', aname)
                                    tname = tracks_data["items"][x]["name"]
                                    trackname = re.sub(r'[^A-Za-z0-9\s$-_.+!*(),\']', '', tname)
                                    alname = tracks_data["items"][x]["album"]["name"]
                                    albumname = re.sub(r'[^A-Za-z0-9\s$-_.+!*(),\']', '', alname)
                                    trackinfolist = []
                                    trackinfolist.append(artistname)
                                    trackinfolist.append(trackname)
                                    trackinfolist.append(albumname)
                                    trackinfo[urlid] = trackinfolist
                                    counter = counter + 1
                                if counter == 18:
                                    break

            final_links = []

            app.logger.info(trackinfo)
            app.logger.info("size of trackinfo:" + str(len(trackinfo)))

            try:
                for x in range(0,18):
                    link = links[x]
                    final_links.append(link)
                    urllib.request.urlretrieve(link, "./static/" + str(x+1) + ".jpg") #download images
            except Exception as e:
                print (e)

            if user != None:
                if "long_term" in spotifyAPI:
                    database.child(database_key).child("long term").set(final_links, user["idToken"])
                elif "medium_term" in spotifyAPI:
                    database.child(database_key).child("mid term").set(final_links, user["idToken"])
                elif "short_term" in spotifyAPI:
                    database.child(database_key).child("mid term").set(final_links, user["idToken"])

        except Exception as e:
            print (e)

    except Exception as e:
        print (e)

    return trackinfo
    #return redirect(url_for('wallify'))

@app.route("/choices", methods=["POST","GET"])
def intermediate():
    onMobile = False
    #landing page for users
    for key in request.form:
        if key.startswith('true'):
            onMobile = True
    print(onMobile)
    #perform redirects based on the option that the user picks
    if request.method == "POST" and onMobile == False:
        if request.form["option"] == "Recent Bops":
            trackinfo = spotify("https://api.spotify.com/v1/me/top/tracks?time_range=short_term&limit=50")
            return redirect(url_for('short',data=trackinfo))
        elif request.form["option"] == "Semester Jams":
            print("HEREEE")
            trackinfo = spotify("https://api.spotify.com/v1/me/top/tracks?time_range=medium_term&limit=50")
            return redirect(url_for('medium',data=trackinfo))
        elif request.form["option"] == "Run It Back Turbo":
            trackinfo = spotify("https://api.spotify.com/v1/me/top/tracks?time_range=long_term&limit=50")
            return redirect(url_for('long',data=trackinfo))

    if request.method == "POST" and onMobile == True:
        if request.form["option"] == "Recent Bops":
            trackinfo = spotify("https://api.spotify.com/v1/me/top/tracks?time_range=short_term&limit=50")
            term="Recent Bops"
        elif request.form["option"] == "Semester Jams":
            trackinfo = spotify("https://api.spotify.com/v1/me/top/tracks?time_range=medium_term&limit=50")
            term="Semester Jams"
        elif request.form["option"] == "Run It Back Turbo":
            trackinfo = spotify("https://api.spotify.com/v1/me/top/tracks?time_range=long_term&limit=50")
            term="Run It Back Turbo"
        app.logger.info("HERE IN CHOICES-----")
        return redirect(url_for('mobile', termName=term))

    return render_template("intermediate.html")

@app.route("/callback/q")
def callback():
    #upon successful authorization, redirect for intermediate on callback
    global refreshTime
    global refresh_token
    session.clear()
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
    session["token"] = access_token

    if refreshTime == 0:
        refresh_token = response_data["refresh_token"]
        refreshTime = refreshTime + 1

    return redirect(url_for('intermediate'))

@app.route("/final.jpg")
def returnImage():
    #download wallpaper that has been created
    time.sleep(2)
    global token
    name = "final.jpg"
    return send_file('./static/' + name, 'final.jpg')

@app.route("/short/<data>", methods=["POST", "GET"])
def short(data):
    if request.method == "POST":
        if request.form["option"] == "back":
            return redirect(url_for('intermediate'))
    return render_template('short.html',trackdata=data)

@app.route("/medium/<data>", methods=["POST", "GET"])
def medium(data):
    if request.method == "POST":
        if request.form["option"] == "back":
            return redirect(url_for('intermediate'))
    return render_template('medium.html',trackdata=data)

@app.route("/long/<data>", methods=["POST", "GET"])
def long(data):
    if request.method == "POST":
        if request.form["option"] == "back":
            return redirect(url_for('intermediate'))
    return render_template('long.html',trackdata=data)


@app.route("/wallify")
def wallify():
    return render_template('wallify.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/receive",methods=["POST"])
def get_data():
    #javascript makes an AJAX POST request to pass array here; assemble wallpaper based on sequence of integers in array
    if request.method == "POST":
        ints = request.get_json()
        data = ints.get("ints")
        global token
        token = random.randint(1,100)
        download_desktop(data)
        return str(token),200

@app.route("/mobile/<termName>")
def mobile(termName):
    app.logger.info("HERE IN MOBILE----")
    image1 = Image.open("./static/1.jpg")
    image2 = Image.open("./static/2.jpg")
    image3 = Image.open("./static/3.jpg")
    image4 = Image.open("./static/4.jpg")
    image5 = Image.open("./static/5.jpg")

    image6 = Image.open("./static/6.jpg")
    image7 = Image.open("./static/7.jpg")
    image8 = Image.open("./static/8.jpg")
    image9 = Image.open("./static/9.jpg")
    image10 = Image.open("./static/10.jpg")

    image11 = Image.open("./static/11.jpg")
    image12 = Image.open("./static/12.jpg")
    image13 = Image.open("./static/13.jpg")
    image14 = Image.open("./static/14.jpg")
    image15 = Image.open("./static/15.jpg")

    (width, height) = image1.size
    result_width = width
    result_height = height * 5

    result = Image.new('RGB', (result_width, result_height))
    result2 = Image.new('RGB', (result_width, result_height))
    result3 = Image.new('RGB', (result_width, result_height))

    result.paste(im=image1, box=(0, 0))
    result.paste(im=image2, box=(0, height))
    result.paste(im=image3, box=(0, 2 * height))
    result.paste(im=image4, box=(0, 3 * height))
    result.paste(im=image5, box=(0, 4 * height))

    result2.paste(im=image6, box=(0, 0))
    result2.paste(im=image7, box=(0, height))
    result2.paste(im=image8, box=(0, 2 * height))
    result2.paste(im=image9, box=(0, 3 * height))
    result2.paste(im=image10, box=(0, 4 * height))

    result3.paste(im=image11, box=(0, 0))
    result3.paste(im=image12, box=(0, height))
    result3.paste(im=image13, box=(0, 2 * height))
    result3.paste(im=image14, box=(0, 3 * height))
    result3.paste(im=image15, box=(0, 4 * height))

    result.save('result1.jpg')
    result2.save('result2.jpg')
    result3.save('result3.jpg')
    shutil.move("./result1.jpg", "./static/result1.jpg")
    shutil.move("./result2.jpg", "./static/result2.jpg")
    shutil.move("./result3.jpg", "./static/result3.jpg")

    imageres = Image.open("./static/result1.jpg")
    imageres2 = Image.open("./static/result2.jpg")
    imageres3 = Image.open("./static/result3.jpg")

    (width,height) = imageres.size

    result_width = width * 3
    result_height = height
    result = Image.new('RGB', (result_width, result_height))

    result.paste(im = imageres, box=(0, 0))
    result.paste(im = imageres2, box=(width,0))
    result.paste(im = imageres3, box=(width * 2,0))

    name = "final.jpg"
    result.save(name)
    shutil.move("./" + name, "./static/" + name)
    return render_template('mobile.html', data=termName)


def download_desktop(data):
    image1 = Image.open("./static/"+str(data[0]) + ".jpg")
    image2 = Image.open("./static/"+str(data[6]) + ".jpg")
    image3 = Image.open("./static/"+str(data[12]) + ".jpg")

    image4 = Image.open("./static/"+str(data[1]) + ".jpg")
    image5 = Image.open("./static/"+str(data[7]) + ".jpg")
    image6 = Image.open("./static/"+str(data[13]) + ".jpg")

    image7 = Image.open("./static/"+str(data[2]) + ".jpg")
    image8 = Image.open("./static/"+str(data[8]) + ".jpg")
    image9 = Image.open("./static/"+str(data[14]) + ".jpg")

    image10 = Image.open("./static/"+str(data[3]) + ".jpg")
    image11 = Image.open("./static/"+str(data[9]) + ".jpg")
    image12 = Image.open("./static/"+str(data[15]) + ".jpg")

    image13 = Image.open("./static/"+str(data[4]) + ".jpg")
    image14 = Image.open("./static/"+str(data[10]) + ".jpg")
    image15 = Image.open("./static/"+str(data[16]) + ".jpg")

    image16 = Image.open("./static/"+str(data[5]) + ".jpg")
    image17 = Image.open("./static/"+str(data[11]) + ".jpg")
    image18 = Image.open("./static/"+str(data[17]) + ".jpg")

    (width1, height1) = image1.size
    (width2, height2) = image2.size
    (width3, height3) = image3.size
    (width4, height4) = image4.size
    (width5, height5) = image5.size
    (width6, height6) = image6.size

    result_width = width1
    result_height = height1 + height2 + height3


    result = Image.new('RGB', (result_width, result_height))
    result2 = Image.new('RGB', (result_width, result_height))
    result3 = Image.new('RGB', (result_width, result_height))
    result4 = Image.new('RGB', (result_width, result_height))
    result5 = Image.new('RGB', (result_width, result_height))
    result6 = Image.new('RGB', (result_width, result_height))

    result.paste(im=image1, box=(0, 0))
    result.paste(im=image2, box=(0, height1))
    result.paste(im=image3, box=(0, 2 * height1))

    result2.paste(im=image4, box=(0, 0))
    result2.paste(im=image5, box=(0, height3))
    result2.paste(im=image6, box=(0, 2 * height4))

    result3.paste(im=image7, box=(0, 0))
    result3.paste(im=image8, box=(0, height1))
    result3.paste(im=image9, box=(0, 2 * height1))

    result4.paste(im=image10, box=(0, 0))
    result4.paste(im=image11, box=(0, height3))
    result4.paste(im=image12, box=(0, 2* height4))

    result5.paste(im=image13, box=(0, 0))
    result5.paste(im=image14, box=(0, height3))
    result5.paste(im=image15, box=(0, 2* height4))

    result6.paste(im=image16, box=(0, 0))
    result6.paste(im=image17, box=(0, height3))
    result6.paste(im=image18, box=(0, 2* height4))


    result.save('result1.jpg')
    result2.save('result2.jpg')
    result3.save('result3.jpg')
    result4.save('result4.jpg')
    result5.save('result5.jpg')
    result6.save('result6.jpg')

    shutil.move("./result1.jpg", "./static/result1.jpg")
    shutil.move("./result2.jpg", "./static/result2.jpg")
    shutil.move("./result3.jpg", "./static/result3.jpg")
    shutil.move("./result4.jpg", "./static/result4.jpg")
    shutil.move("./result5.jpg", "./static/result5.jpg")
    shutil.move("./result6.jpg", "./static/result6.jpg")

    imageres = Image.open("./static/result1.jpg")
    imageres2 = Image.open("./static/result2.jpg")
    imageres3 = Image.open("./static/result3.jpg")
    imageres4 = Image.open("./static/result4.jpg")
    imageres5 = Image.open("./static/result5.jpg")
    imageres6 = Image.open("./static/result6.jpg")

    (widthres1, heightres1) = imageres.size
    (widthres2, heightres2) = imageres2.size
    (widthres3, heightres3) = imageres3.size
    (widthres4, heightres4) = imageres4.size
    (widthres5, heightres5) = imageres5.size
    (widthres6, heightres6) = imageres6.size

    result_width = widthres1 + widthres2 + widthres3 + widthres4 + widthres5 + widthres6
    result_heigth = heightres1

    result = Image.new('RGB', (result_width, result_height))

    result.paste(im = imageres, box=(0, 0))
    result.paste(im = imageres2, box=(widthres1,0))
    result.paste(im = imageres3, box=(widthres1 * 2,0))
    result.paste(im = imageres4, box=(widthres1 * 3,0))
    result.paste(im = imageres5, box=(widthres1 * 4,0))
    result.paste(im = imageres6, box=(widthres1 * 5,0))

    name = "final.jpg"
    result.save(name)
    shutil.move("./" + name, "./static/" + name)    


if __name__ == "__main__":
    app.run(debug=True)
