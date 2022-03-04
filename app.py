from email import message
from flask import Flask, render_template, redirect, url_for, request
import requests
import re

app = Flask(__name__)

# Use requests library to get the page source html
def get_response(url):
    r = requests.get(url)
    return r.text

# create matches and clean up the raw html item
def prepare_urls(matches):
    return list({match.replace("\\u0026", "&") for match in matches})

# route to main page
@app.route("/", methods = ["GET", "POST"])
def home():

    # Get the home page
    if request.method == "GET":
        return render_template("index.html")
    
    # Check if any post is made
    if request.method == "POST":
        getLink = request.form["link"]
        
        url = getLink
        response = get_response(url)

        # check for the video and picture urls in the json from the url
        vid_matches = re.findall('"video_url":"([^"]+)"', response)
        pic_matches = re.findall('"display_url":"([^"]+)"', response)
        
        vid_urls = prepare_urls(vid_matches)
        pic_urls = prepare_urls(pic_matches)

        # check if theere is a video in the post
        if vid_urls:
            return render_template("loading.html", message = "Video downloading")
        
        # Check if there is a picture in the post
        if pic_urls:
            return render_template("loading.html", message = "Picture downloading")
        
        # return the error if no post found
        else:
            return render_template("error.html", err = "Link is broken Please try again")

    else:
        return render_template("error", err = "Unknown method")

# route to landing page for the loading
@app.route("/landing")
def landing():
    return render_template("loading.html", message = "Kindly wait")

# route for the error page
@app.route("/error")
def error():
    return render_template("error.html", err = "")

# run app script
if __name__ == "__main__":
    app.run()
