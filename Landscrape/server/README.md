# server

# What's in this folder?
This is where all of the core rendering and backend functionality for LandScrape exists.

# Files/Folders
- server.py

This is where the app is actually run from. All routing information is contained here. This is the primary controller for the app.
- Scraper

This is where the scraping function exists. Here, you can see how we actually scraped Foursqure and Yelp, compared their results, and outputted the final information to a dictionary. You can view automatically generated documentation by navigating to `Scraper/html/index.html` and following the instructions listed in the root readme.

- tests.py

This is the testing suite file for the application. This file is accessible from the webpage, or can be run with more verbosity as a standalone test suite by running `python tests.py` in this folder.

# Documentation
You can view automatically generated Documentation for these functions by navigating to `html/index.html` and following the instructions listed in the root readme.
