# server.py
import random
from flask import Flask, render_template

app = Flask(__name__, static_folder="../static/dist", template_folder="../static")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    return render_template("Search.html")

if __name__ == "__main__":
    app.run()
