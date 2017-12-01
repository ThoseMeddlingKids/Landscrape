# static

# What's in this folder?
This is where the html templates for our app are located. Flask utilizes a Python Templating Engine called Jinja2, which is why you'll see curly braces and percent signs scattered throughout our html files. This allows us to nest Python functionality in our template rendering (i.e. `{% for entry in booleanTestResults %}`)

# Core Files/Folders
- search.html & results.html: this is how the search queries are entered and results pages are rendered
- about.html & testresults.html: this is how our test suite results are rendered and displayed
