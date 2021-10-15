import os
from database import Database
from flask import Flask, render_template, request, redirect, url_for, g, flash
from datetime import datetime

# Initialize flask application
app = Flask(__name__, static_folder="static",
            template_folder="templates", static_url_path="")
app.secret_key = "Carl.M"


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


# DATETIME UTILS
today = datetime.now().strftime("%Y-%m-%d")

# Server perspective :
# POST  ⟹ used to receive data (from clients)
# GET   ⟹ used to send data to clients


# GET ⟹ Default route ⟹ /
# TODO : Need a search field for LIKE DB
@app.route("/", methods=["GET"])
def get_last_five_articles():
    return render_template('home.html')


# GET ⟹ /article/<string:identifiant>
# ℹ️: 'http://127.0.0.1:5000/article/some_name'
@app.route('/article/<string:name>')
def get_an_article(name):
    return render_template('article.html')


# GET ⟹ /admin
# TODO : list of ∀ articles (title & date) + link to modify (title & paragraph) each article (for ∀) + link to create new article (/admin-nouveau)
# @app.route('/admin')


# GET ⟹  /admin-nouveau
# TODO : page with form for creating new article
# @app.route('/admin-nouveau')


# This is always true if app.py is used as entry point of the interpretor
if __name__ == "__main__":
    app.run(port=5000)
