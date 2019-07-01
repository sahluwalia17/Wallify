from flask import Flask, render_template, redirect, request, url_for, send_file, jsonify
from flask_cachebuster import CacheBuster
import webbrowser
import re
import requests
from urllib.parse import quote
from PIL import Image
from os import path
import shutil
import time
import urllib.request
import json
import pyrebase
import random
import importlib

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
user = None #This becomes the user after signing in
auth_token = None
clientId = "45ba6741126e4af1b9c7fef7f6bd7568"
clientSecret = "be75f467163b4812aee28c45e3bcf860"
baseURL = "https://accounts.spotify.com/authorize"
redirectURL = "http://127.0.0.1:5000/callback/q"
# redirectURL = "https://wallifyy.herokuapp.com/callback/q"
#change redirect URL to proper URL
scope = "user-top-read"
spotifyTokenURL = "https://accounts.spotify.com/api/token"
refresh_token = ""
refreshTime = 0

#spotifyAPI = "https://api.spotify.com/v1/me/top/tracks?time_range=short_term&limit=50"


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
#begin
authentication = fb.auth()
database = fb.database()
database_key = None
@app.route("/", methods = ["POST", "GET"])
def index():#add authentication part here
    #print("made it")
    # invalid = "Please enter a valid email or password"
    # weak = "Password length must be at least 6 characters"
    # exist = "This email is already in use"
    # incorrect = "Either email or passwords is incorrect"
    #print ("made it")
    if request.method ==  "POST":
        # if request.form["sign"] == 'Sign In': #this needs to be determined in html
        #     #print ("asdf")
        #     email = request.form['email']#'name' depends on html tag
        #     password = request.form['pwd']#'password' depends on html tag
        #     try:
        #         global user
        #         user = authentication.sign_in_with_email_and_password(email,password)
        #         #authorize()
        #         new_email = email[:email.find('@')]
        #         global database_key
        #         database_key = re.sub('[^A-Za-z0-9]','',new_email)
        #         return redirect(url_for('authorize'))
        #     except Exception as e:
        #         print (e)
        #         return render_template("index.html", r=incorrect)#all this depends on html
        # elif request.form["sign"] == 'Sign Up':
        #     email = request.form['email']#html tag <input... name = 'name'...>
        #     password = request.form['pwd']#html tag<input... name_ = 'password'...>
        #     try:
        #         #user = authentication.create_user_with_email_and_password(email,password)
        #         user = authentication.create_user_with_email_and_password(email, password)
        #         #refactor template to go to wallify page
        #         #return render_template("wallify.html")
        #         new_email = email[:email.find('@')]
        #         database_key = re.sub('[^A-Za-z0-9]','',new_email)
        #         return redirect(url_for('authorize'))
        #         #return render_template("index.html")
        #     except Exception as e:
        #
        #         get_error = e.args[1]
        #         error = json.loads(get_error)['error']
        #         #print(error['message'])
        #         msg = error['message']
        #         #the render_template will be done in html the i = and w = and x = will bring up bars
        #         #WORK WITH PUJA ON THIS
        #         if msg == "INVALID_EMAIL" or msg == "INVALID PASSWORD":
        #             return render_template("index.html", i=invalid)
        #             #pass
        #             #reload the page with a header this is done in html
        #         elif "WEAK_PASSWORD" in msg:
        #             return render_template("index.html", w=weak)
        #             #pass
        #         elif msg == "EMAIL_EXISTS":
        #             return render_template("index.html", x=exist)

                #print (e)
        # elif request.form["sign"] == 'Guest':
        if request.form["sign"] == 'Get Started!':

            #print ("pasdf")
            return redirect(url_for('authorize'))
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

def spotify(spotifyAPI):
    global refreshTime
    global refresh_token

    if refreshTime == 0:
        code_payload = {
            "grant_type": "authorization_code",
            "code": str(auth_token),
            "redirect_uri": redirectURL,
            "client_id": clientId,
            "client_secret": clientSecret
        }
    elif refreshTime > 0:
        code_payload = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": clientId,
            "client_secret": clientSecret
        }
    dateTime = random.randint(1,100000)
    try:
        post_request = requests.post(spotifyTokenURL, data=code_payload)

        response_data = json.loads(post_request.text)
        access_token = response_data["access_token"]

        if refreshTime == 0:
            refresh_token = response_data["refresh_token"]
            refreshTime = refreshTime + 1

        authorization_header = {"Accept":"application/json", "Authorization":"Bearer {}".format(access_token)}

        top_tracks = requests.get(spotifyAPI, headers = authorization_header)

        tracks_data = json.loads(top_tracks.text)
    except Exception as e:
        print (e)

    links = []
    filteredlinks = []
    try:
        for x in range(0,50):
                for y in range(0,1):
                        links.append(tracks_data["items"][x]["album"]["images"][1]["url"])
    except Exception as e:
        print (e)

    for i in links:
            if i not in filteredlinks:
                    filteredlinks.append(i)

    print(filteredlinks)
    final_links = []
    try:
        for x in range(0,18):
            link = filteredlinks[x]
            final_links.append(link)
            urllib.request.urlretrieve(link, "./static/" + str(x+1) + ".jpg")
    except Exception as e:
        print (e)


    if user != None:
        if "long_term" in spotifyAPI:
            database.child(database_key).child("long term").set(final_links, user["idToken"])
        elif "medium_term" in spotifyAPI:
            database.child(database_key).child("mid term").set(final_links, user["idToken"])
        elif "short_term" in spotifyAPI:
            database.child(database_key).child("mid term").set(final_links, user["idToken"])

    #return redirect(url_for('wallify'))

@app.route("/choices", methods=["POST","GET"])
def intermediate():
    if request.method == "POST":
        if request.form["option"] == "Recent Bops":
            spotify("https://api.spotify.com/v1/me/top/tracks?time_range=short_term&limit=50")
            return redirect(url_for('wallify'))
        elif request.form["option"] == "Semester Jams":
            spotify("https://api.spotify.com/v1/me/top/tracks?time_range=medium_term&limit=50")
            return redirect(url_for('wallify'))
        elif request.form["option"] == "Run It Back Turbo":
            spotify("https://api.spotify.com/v1/me/top/tracks?time_range=long_term&limit=50")
            return redirect(url_for('wallify'))
    return render_template("intermediate.html")

@app.route("/callback/q")
def callback():
    global auth_token
    auth_token = request.args['code']
    return redirect(url_for('intermediate'))
    #return render_template("intermediate.html")

@app.route("/final.jpg")
def returnImage():
    return send_file('./static/final.jpg', 'final.jpg')

@app.route("/wallify")
def wallify():
    return render_template('wallify.html')

@app.route("/receive",methods=["POST"])
def get_data():
    if request.method == "POST":
        if path.exists("final.jpg"):
            os.remove("final.jpg")
        ints = request.get_json()
        data = ints.get("ints")


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

        result.save('final.jpg')
        shutil.move("./final.jpg", "./static/final.jpg")

        return "",200

if __name__ == "__main__":
    app.run(debug=True)
