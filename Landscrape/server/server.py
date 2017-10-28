## @file server.py
#
# Server run File that provides the main interface between our app and th Server
#Includes routing Information and Rendering of HTML
import random
from flask import Flask, render_template, request

app = Flask(__name__, static_folder="../static/dist", template_folder="../static")
app.debug = True

## @package Flask
#Documentation for the Server
#
# @file server.py
# Runs the Server that Landscrape runs on

## @Route "/"
#
# Main Landing Page for the App
# Renders Index from Static/index.html
@app.route("/")
def index():
    return render_template("index.html")

## @Route "/search"
#
# Search Page for Landscrape
# Renders the Search HTML file
# This is the Page where users can input search queries
@app.route("/search")
def search():
    return render_template("Search.html")

## @Route "/handle_data"
#
# Attempt at handling data using the Request Library
# Unsure of how to actually do this.
# Currently returns a "402 Bad Request" Error
@app.route('/handle_data', methods = ['POST'])
def handle_data():
    print("woah")
    print(request.form['Search.html'])

## @Route "/searchresults"
#
# Process Data from the Scraping function
# Renders HTML with Results
@app.route('/searchresults', methods = ['GET', 'POST'])
def processJSON():
    dataToProcess = request.json

##Runs the Server
if __name__ == "__main__":
    app.run()
