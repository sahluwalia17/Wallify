from flask import Flask, render_template
import urllib.request

app = Flask(__name__)

@app.route("/")
def home():
    url = 'https://www.purdue.edu/purdue/images/audience/about-banner.jpg'
    urllib.request.urlretrieve(url, "./static/Purdue.jpg")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
