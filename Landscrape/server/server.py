## @file server.py
#
# Server run File that provides the main interface between our app and th Server
#Includes routing Information and Rendering of HTML
import random
from flask import Flask, render_template, request, flash, redirect, url_for, session, logging
from wtforms import Form, StringField, validators

app = Flask(__name__, static_folder="../static/dist", template_folder="../static")
app.debug = True

## @package Flask
#Documentation for the Server
#
# @file server.py
# Runs the Landscrape Main Server


########################################################
#                                       CLASSES
########################################################
## @Class InputForm
#
# Form that Takes the String(s) Given as Input
class InputForm(Form):
    searchquery = StringField(u'Enter Your Search:', validators = [validators.input_required()])


########################################################
#                                       FUNCTIONS
########################################################
def HandleData(data):
    app.logger.info('%s processed', data)
    return data

########################################################
#                                       ROUTES
########################################################
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
@app.route("/search", methods = ['GET','POST'])
def search():
    form = InputForm(request.form)
    if request.method == 'POST' and form.validate():
        query = form.searchquery.data
        HandleData(query)

    return render_template("Search.html", form= form)

## @Route "/about"
#
# Documentation
# Renders HTML with Documentation
@app.route('/about')
def about():
    return render_template("about.html")

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
