## @file server.py
#
# Server run File that provides the main interface between our app and th Server
#Includes routing Information and Rendering of HTML
import random
from flask import Flask, render_template, request, flash, redirect, url_for, session, logging
from wtforms import Form, StringField, validators

from Scraper import scrape

app = Flask(__name__, static_folder="../static", template_folder="../static")
app.debug = True

## @package Flask
# Documentation for the Server
# Flask is a Microframework for Web Development thtat Utilizes Python
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
## @File Handle
#
## Deprecated
def HandleData(data):
    app.logger.info('%s processed', data)
    return data

## Function
#
# Creates a new python dictionary
def CreateDict(name):
    LandScrape = scrape.Scraper([name,"lawrence","KS"])
    return LandScrape.get_results()

########################################################
#                                       ROUTES
########################################################
## Class "/"
#
# Main Landing Page for the App
# Renders Index from Static/index.html
@app.route("/")
def index():
    return render_template("index.html")


## Class "/search"
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
        # 'session' stores the query in order to be used on a different page.
        # in this case it is the results page that must recall this info
        # think of session as a cookie.
        session['query'] = query
        return redirect(url_for('loading'))
    return render_template('Search.html', form= form)

## Function "/about"
#
# Documentation
# Renders HTML with Documentation links
@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/loading', methods = ['GET', 'POST'])
def loading():
    return render_template("loadingpage.html")

## Function "/searchresults"
#
# Process Data from the Scraping function
# Renders HTML with Results
@app.route('/results', methods = ['GET', 'POST'])
def results():
    # query being set to what was stored in the session
    query = session['query']
    py_dict = CreateDict(query)
    HandleData(py_dict)
    return render_template("results.html", pyDict = py_dict)

##Runs the Server
if __name__ == "__main__":
    # setting key for the session in order to pass the search query to the results page
    # this is just initialization info. shouldn't need to ever touch this.
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run()
