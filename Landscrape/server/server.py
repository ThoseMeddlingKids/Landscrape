##############################################################################
## @file server.py
#
# Server run File that provides the main interface between our app and th Server
# Includes routing Information and Rendering of HTML

#Importing essential python libraries and other tools
import random, unittest, os

## @package Flask
#
# Flask is a Microframework for Web Development thtat Utilizes Python
# Flask-WTF is a form handling library for Flask. It includes some nice validation tools
from flask import Flask, render_template, request, flash, redirect, url_for, session, logging
from wtforms import Form, StringField, SelectField, validators

# This is where we import the stuff we made into the server
from Scraper import scrape
from tests import TestOutputSingle, TestOutputMulti

#Define Flask App
#This will eventually tell the server what and how to run our app, along with where our templates exist
app = Flask(__name__, static_folder="../static", template_folder="../static")
#Debug allows for console output and continuous update with changes to local files
app.debug = True

##############################################################################

########################################################
#                                       CLASSES
########################################################
## @Class InputForm
#
# Form that Takes the String(s) Given as Input and passes them into the dictionary
#See WTForms Documentation for more information regarding declaration of form classes and their params
class InputForm(Form):
    search_query = StringField(u'Enter Your Search:', render_kw={"placeholder": "Please Enter Queries as a Comma-Seperated list."}, validators = [validators.input_required()])
    search_state = SelectField(u'State:', choices=[('AL','Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'),('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'),('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')], default='KS')
    search_city = StringField(u'City:', validators = [validators.input_required()], default="Lawrence")

##############################################################################

########################################################
#                                       FUNCTIONS
########################################################

## Function CreateDict
#
# Creates a new python dictionary with the results from a search query.
def CreateDict(query, city, state):
    LandScrape = scrape.Scraper([query,city,state])
    return LandScrape.get_results()

##############################################################################
########################################################
#                                       ROUTES
########################################################
# Routing for the application is essential for navigation on the web.

# LANDING PAGE
##############################################################################
## Class "/"
#
# Main Landing Page for the App
# Renders Index from Static/index.html
@app.route("/")
def index():
    return render_template("index.html")
##############################################################################



#TESTS AND TEST RESULTS ROUTING
##############################################################################
## Class "/about"
#
# Renders the "Is LandScrape Complete?" Page with the results of our testing suite
#
@app.route('/about')
def about():
    return render_template("about.html")
##############################################################################
##############################################################################
## Class "/testresults"
#
# Renders the test results page and handles the running of our test suite from within the app
@app.route('/testresults', methods = ['GET','POST'])
def testresults():

    # Declare Test suite for each TestCase Class
    suite1 = unittest.TestLoader().loadTestsFromTestCase(TestOutputSingle)
    suite2 = unittest.TestLoader().loadTestsFromTestCase(TestOutputMulti)

    # run the test suites and create a list of result objects
    Test1_Result = unittest.TextTestRunner(verbosity = 1).run(suite1)
    Test2_Result = unittest.TextTestRunner(verbosity = 1).run(suite2)

    ResultOfTesting = [Test1_Result, Test2_Result]

    #Convert results to boolean output which will be passed to page
    BooleanResults = []
    for result in ResultOfTesting:
        if len(result.errors) == 0:
            BooleanResults.append(True)
        else:
            BooleanResults.append(False)

    #pass the boolean array to the page for loading
    return render_template("testresults.html", BooleanTestResults = BooleanResults)
##############################################################################




# SEARCH AND SEARCH RESULTS ROUTING
##############################################################################
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

        # 'session' stores the query in order to be used on a different page.
        # in this case it is the results page that must recall this info
        # think of session as a cookie.
        session['query'] = query
        session['state'] = state
        session['city'] = city
        return redirect(url_for('loading'))
    return render_template('Search.html', form= form)
##############################################################################
##############################################################################
## Class "/loading"
#
# Placeholder for the time it takes to load results from a search
@app.route('/loading', methods = ['GET', 'POST'])
def loading():
    return render_template("loadingpage.html")
##############################################################################
##############################################################################
## Class "/searchresults"
#
# Process Data from the Scraping function
# Renders HTML with Results
@app.route('/results', methods = ['GET', 'POST'])
def results():
    # query being set to what was stored in the session
    query = session['query']
    city = session['city']
    state = session['state']

    #If for some reason there is an error in dictionary creation, this will handle it
    try:
        py_dict = CreateDict(query, city, state)
    except:
        return '<h2> Whoops! There was an Error Somewhere! </h2>'


    return render_template("results.html", pyDict = py_dict)
##############################################################################

##############################################################################
##############################################################################
##############################################################################
## Function "MAIN"
#
## Runs the Server and deploys the app to a local host.
## This also deals with the heroku environment setup using the "os" call
if __name__ == "__main__":
    # setting key for the session in order to pass the search query to the results page
    # this is just initialization info. shouldn't need to ever touch this.
    app.secret_key = 'super secret key'
    port = int(os.environ.get("PORT", 5000))
    app.run(host = '0.0.0.0' , port = port)
