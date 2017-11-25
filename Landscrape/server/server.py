## @file server.py
#
# Server run File that provides the main interface between our app and th Server
#Includes routing Information and Rendering of HTML
import random
from flask import Flask, render_template, request, flash, redirect, url_for, session, logging
from wtforms import Form, StringField, SelectField, validators

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
    search_query = StringField(u'Enter Your Search:', render_kw={"placeholder": "Please Enter Queries as a Comma-Seperated list."}, validators = [validators.input_required()])
    search_state = SelectField(u'State:', choices=[('AL','Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'),('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'),('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')], default='KS')
    search_city = StringField(u'City:', validators = [validators.input_required()], default="Lawrence")

# class DynamicForm(Form):
#     @classmethod
#     def append_field(cls, name, field):
#         setattr(cls, name, field)
#         return cls





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
def CreateDict(query, city, state):
    LandScrape = scrape.Scraper([query,city,state])
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
        query = form.search_query.data
        state = form.search_state.data
        city = form.search_city.data
        HandleData([query,city,state])
        # 'session' stores the query in order to be used on a different page.
        # in this case it is the results page that must recall this info
        # think of session as a cookie.
        session['query'] = query
        session['state'] = state
        session['city'] = city
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
    city = session['city']
    state = session['state']
    try:
        py_dict = CreateDict(query, city, state)
        HandleData(py_dict)
    except:
        return '<h1> Whoops! There was an Error Somewhere! </h1>'
    return render_template("results.html", pyDict = py_dict)

##Runs the Server
if __name__ == "__main__":
    # setting key for the session in order to pass the search query to the results page
    # this is just initialization info. shouldn't need to ever touch this.
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run()
