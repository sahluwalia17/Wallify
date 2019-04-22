from flask import Flask, render_template, redirect, request, url_for
import webbrowser
import re
import requests
from urllib.parse import quote
import urllib.request
import json
import pyrebase

app = Flask(__name__)
user = None #This becomes the user after signing in
clientId = "45ba6741126e4af1b9c7fef7f6bd7568"
clientSecret = "be75f467163b4812aee28c45e3bcf860"
baseURL = "https://accounts.spotify.com/authorize"
redirectURL = "http://127.0.0.1:5000/callback/q"
scope = "user-top-read"
spotifyTokenURL = "https://accounts.spotify.com/api/token"
spotifyAPI = "https://api.spotify.com/v1/me/top/tracks?time_range=short_term&limit=50"

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
authentication = fb.auth()
database = fb.database()
database_key = None
@app.route("/", methods = ["POST", "GET"])
def index():#add authentication part here
    #print("made it")
    invalid = "Please enter a valid email or password"
    weak = "Password length must be at least 6 characters"
    exist = "This email is already in use"
    incorrect = "Either email or passwords is incorrect"
    #print ("made it")
    if request.method ==  "POST":
        #print ("jkl")
        if request.form["sign"] == 'Sign In': #this needs to be determined in html
            #print ("asdf")
            email = request.form['email']#'name' depends on html tag
            password = request.form['pwd']#'password' depends on html tag
            try:
                global user
                user = authentication.sign_in_with_email_and_password(email,password)
                #authorize()
                new_email = email[:email.find('@')]
                global database_key
                database_key = re.sub('[^A-Za-z0-9]','',new_email)
                return redirect(url_for('authorize'))
            except Exception as e:
                print (e)
                return render_template("index.html", r=incorrect)#all this depends on html
        elif request.form["sign"] == 'Sign Up':
            email = request.form['email']#html tag <input... name = 'name'...>
            password = request.form['pwd']#html tag<input... name_ = 'password'...>
            try:
                #user = authentication.create_user_with_email_and_password(email,password)
                user = authentication.create_user_with_email_and_password(email, password)
                #refactor template to go to wallify page
                #return render_template("wallify.html")
                database_key = re.sub('[^A-Za-z0-9]','',new_email)
                return redirect(url_for('authorize'))
                #return render_template("index.html")
            except Exception as e:
                
                get_error = e.args[1]
                error = json.loads(get_error)['error']
                #print(error['message'])
                msg = error['message']
                #the render_template will be done in html the i = and w = and x = will bring up bars
                #WORK WITH PUJA ON THIS
                if msg == "INVALID_EMAIL" or msg == "INVALID PASSWORD":
                    return render_template("index.html", i=invalid)
                    #pass
                    #reload the page with a header this is done in html
                elif "WEAK_PASSWORD" in msg:
                    return render_template("index.html", w=weak)
                    #pass
                elif msg == "EMAIL_EXISTS":
                    return render_template("index.html", x=exist)
                
                #print (e)
        elif request.form["sign"] == 'Guest':
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
    final_links = []
    for x in range(0,18):
        link = filteredlinks[x]
        final_links.append(link)
        urllib.request.urlretrieve(link, "./static/" + str(x+1) + ".jpg")
    if user != None:
        database.child(database_key).child("long term").set(final_links, user["idToken"])
    return redirect(url_for('wallify'))

@app.route("/wallify")
def wallify():
    return render_template("wallify.html")

if __name__ == "__main__":
    app.run(debug=True)
