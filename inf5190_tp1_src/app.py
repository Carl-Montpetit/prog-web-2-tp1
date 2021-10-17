from database.Database import Database
from flask import Flask, render_template, request, redirect, url_for, g, flash
from datetime import datetime
import re

# Initialize flask application
app = Flask(__name__, static_folder="static",
            template_folder="templates", static_url_path="")
app.secret_key = "Carl.M"

# DATETIME UTILS
today = datetime.now().strftime("%Y-%m-%d")


def get_db():
    """[Get the database in a variable]

    Returns:
        [Any]: [the database]
    """
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database


def add_article_in_db(today):
    news = ['enfer', 'hell is hot', 'Satan', today, 'On a jamais vu ca']
    get_admin().insert_article(news)
    return 1


@app.teardown_appcontext
def close_connection(exception):
    """[Closing the connection with the database]

    Args:
        exception ([Exception]): [an exception]
    """
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()


@app.errorhandler(404)
def page_not_found(error):
    """[Return a page for 404 error code]

    Args:
        error ([int]): [404]

    Returns:
        [Text]: [404.html]
    """
    return render_template("404.html"), 404


# GET ⟹ Default route ⟹ /
# TODO : Need a search field for LIKE DB
@app.route('/', methods=['GET'])
def get_last_five_articles():
    """[The home page containing the last 5 articles from now]

    Returns:
        [Text]: [home.html]
    """
    articles = get_db().get_all_articles()
    return render_template('home.html', articles=articles)


@app.route('/article/<string:identifiant>', methods=['GET'])
def get_an_article(identifiant):
    return render_template('article.html', identifiant=identifiant)


@app.route('/admin', methods=['GET'])
def get_admin():
    """[list of ∀ articles (title & date) + link to modify (title & paragraph) each article (for ∀) + link to create new article to "/admin-nouveau"]

    Returns:
        [Text]: [admin.html]
    """
    return render_template('admin.html')


@app.route('/admin-nouveau', methods=['GET'])
def get_admin_new():
    return render_template('admin-new.html')


@app.route('/admin-nouveau', methods=['POST'])
def add_new_article_in_bd(today=today):
    """[Page with form for creating a new article]

    Returns:
        [Text]: [redirect ⟹ '/' or home.html]
    """
    pattern_date = '^\d{4} -\d{2} -\d{2}$'
    id_article = request.form['id_article']
    titre = request.form['titre']
    identifiant = request.form['identifiant']
    auteur = request.form['auteur']
    date = request.form['date']
    date_validate = re.match(pattern_date, date)
    paragraphe = request.form['paragraphe']
    article = [id_article, titre, identifiant, auteur, today, paragraphe]

    # if there's error(s) the page show error message(s) to the user
    if id_article == "" or titre == "" or identifiant == "" or auteur == "" or date == "" or paragraphe == "":
        return render_template('admin-new.html', error='⚠️Tous les champs doivent impérativement être remplis!..', id_article=id_article, titre=titre, identifiant=identifiant, auteur=auteur, date=date, paragraphe=paragraphe)
    elif type(id_article) is not int:
        return render_template('admin-new.html', error='⚠️Le champs ID doit impérativement être un nombre!..')
    elif len(titre) < 3 or len(titre) > 100:
        return render_template('admin-new.html', error='⚠️Le champs Titre doit impérativement contenir entre 3 et 100 caractères!..')
    elif len(identifiant) < 3 or len(identifiant) > 50:
        return render_template('admin-new.html', error='⚠️Le champs Identifiant doit impérativement contenir entre 3 et 50 caractères!..')
    elif len(auteur) < 3 or len(auteur) > 100:
        return render_template('admin-new.html', error='⚠️Le champs Auteur doit impérativement contenir entre 4 et 100 caractères!..')
    elif date_validate is None:
        return render_template('admin-new.html', error='⚠️Le champs Date doit impérativement être de la forme ⟹ (YYYY-mm-jj)!..')
    elif len(paragraphe) < 1 or len(auteur) > 500:
        return render_template('admin-new.html', error='⚠️Le champs Auteur doit impérativement contenir entre 1 et 500 caractères!..')
    else:
        # add the nuew article in the database + append it in the log file
        get_db().insert_article(article)
        file = open('log.txt', 'a')
        file.write(
            f"id_article\t\t\t⟹\t{id_article}\ntitre\t\t\t⟹\t{titre}\nidentifiant\t\t⟹\t{identifiant}\nauteur\t\t\t⟹\t{auteur}\ndate\t\t\t⟹\t{today}\nparagraphe\t\t⬇︎\n{paragraphe}\n================================================================================\n")
        return render_template('home.html', id_article=id_article, titre=titre, identifiant=identifiant, auteur=auteur, date=date, paragraphe=paragraphe)


# This is always true if app.py is used as entry point of the interpretor
if __name__ == '__main__':
    app.run(port=5000)
