# server.py
import random
from flask import Flask, render_template, request

app = Flask(__name__, static_folder="../static/dist", template_folder="../static")
app.debug = True

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    return render_template("Search.html")

@app.route('/handle_data', methods = ['POST'])
def handle_data():
    print(request.form['Search.html'])


if __name__ == "__main__":
    app.run()
