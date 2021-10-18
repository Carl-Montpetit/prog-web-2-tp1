from database.Database import Database
from flask import Flask, render_template, request, redirect, url_for, g, flash
from datetime import datetime
import re
from article import Article

# Initialize flask application
app = Flask(__name__, static_folder="static",
            template_folder="templates", static_url_path="")
app.secret_key = "Carl.M"

# CONSTANTS
ADMIN_PAGE = 'admin.html'
ADMIN_NEW_ARTICLE_PAGE = 'admin-new.html'
ARTICLE_PAGE = 'article.html'
HOME_PAGE = 'home.html'
ERR_404_PAGE = '404.html'
MODIFY_ARTICLE_PAGE = 'modify-article.html'
SEARCH_RESULT_PAGE = 'search-result.html'
ERR_MSG_EMPTY_FIELDS = '⚠️Tous les champs doivent impérativement être remplis!..'
ERR_MSG_ID = '⚠️Le champs ID doit impérativement être un nombre positif!..'
ERR_MSG_TITRE = '⚠️Le champs Titre doit impérativement contenir entre 3 et 100 caractères!..'
ERR_MSG_IDENTIFIANT = '⚠️Le champs Identifiant doit impérativement contenir entre 3 et 50 caractères!..'
ERR_MSG_AUTEUR = '⚠️Le champs Auteur doit impérativement contenir entre 4 et 100 caractères!..'
ERR_MSG_DATE = '⚠️Le champs Date doit impérativement être de la forme ⟹ (YYYY-mm-jj) avec des nombres!..'
ERR_MSG_PARAGRAPHE = '⚠️Le champs Auteur doit impérativement contenir entre 1 et 500 caractères!..'
ERR_MSG_ID_NOT_UNIQUE = '⚠️Le ID choisis existe déjà, svp veuillez en choisir un autre!..'


# DATETIME UTILS
today = datetime.now().strftime("%Y-%m-%d")


def get_db():
    # [x]
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database


@app.teardown_appcontext
# [x]
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()


@app.errorhandler(404)
# [x]
def page_not_found(error):
    return render_template(ERR_404_PAGE), 404


# TODO : Need a search field for LIKE DB & show the last 5 articles
@app.route('/', methods=['GET'])
# []
def get_last_five_articles():
    articles = get_db().get_all_articles()
    return render_template(HOME_PAGE, articles=articles)


# @app.route('/', methods=['POST'])
# # []
# def search_articles():
#     search = request.form['search']
#     # TODO search result in database
#     return render_template(SEARCH_RESULT_PAGE)

@app.route('/article/<string:identifiant>', methods=['GET'])
# []
def get_an_article(identifiant):
    article = Article()
    article = get_db().get_article_by_identifiant(identifiant)

    return render_template(ARTICLE_PAGE, article=article)


@app.route('/admin', methods=['GET'])
# [x]
def get_admin():
    return render_template(ADMIN_PAGE)


@app.route('/admin-nouveau', methods=['GET'])
# [x]
def get_admin_new():
    return render_template(ADMIN_NEW_ARTICLE_PAGE)


@app.route('/admin-nouveau', methods=['POST'])
# []
def add_new_article_in_bd():
    """[Page with form for creating a new article]

    Returns:
        [Text]: [redirect ⟹ '/' or home.html]
    """
    PATTERN_DATE = '^\d{4}-\d{2}-\d{2}$'
    PATTERN_ID = '^\d+$'

    id_article = request.form['id_article']
    id_validation = re.match(PATTERN_ID, id_article)
    titre = request.form['titre']
    identifiant = request.form['identifiant']
    auteur = request.form['auteur']
    date = request.form['date']
    date_validation = re.match(PATTERN_DATE, date)
    paragraphe = request.form['paragraphe']
    article = [id_article, titre, identifiant, auteur, today, paragraphe]

    # if there's error(s) the page show error message(s) to the user
    if id_article == "" or titre == "" or identifiant == "" or auteur == "" or date == "" or paragraphe == "":
        return render_template(ADMIN_NEW_ARTICLE_PAGE, error=ERR_MSG_EMPTY_FIELDS, id_article=id_article, titre=titre, identifiant=identifiant, auteur=auteur, date=date, paragraphe=paragraphe)
    elif id_validation is None:
        return render_template(ADMIN_NEW_ARTICLE_PAGE, error=ERR_MSG_ID)
    elif len(titre) < 3 or len(titre) > 100:
        return render_template(ADMIN_NEW_ARTICLE_PAGE, error=ERR_MSG_TITRE, err_titre=ERR_MSG_TITRE)
    elif len(identifiant) < 3 or len(identifiant) > 50:
        return render_template(ADMIN_NEW_ARTICLE_PAGE, error=ERR_MSG_IDENTIFIANT)
    elif len(auteur) < 3 or len(auteur) > 100:
        return render_template(ADMIN_NEW_ARTICLE_PAGE, error=ERR_MSG_AUTEUR)
    elif date_validation is None:
        return render_template(ADMIN_NEW_ARTICLE_PAGE, error=ERR_MSG_DATE)
    elif len(paragraphe) < 1 or len(auteur) > 500:
        return render_template(ADMIN_NEW_ARTICLE_PAGE, error=ERR_MSG_PARAGRAPHE)
    else:
        # add the new article in the database + append it in the log file
        try:
            get_db().insert_article(article)
        except Exception:
            return render_template(ADMIN_NEW_ARTICLE_PAGE, error=ERR_MSG_ID_NOT_UNIQUE)
        file = open('log.txt', 'a')
        file.write(
            f"id_article\t\t⟹\t{id_article}\ntitre\t\t\t⟹\t{titre}\nidentifiant\t\t⟹\t{identifiant}\nauteur\t\t\t⟹\t{auteur}\ndate\t\t\t⟹\t{today}\nparagraphe\t\t⬇︎\n{paragraphe}\n================================================================================\n")
        # TODO not refresh the input fields AJAX ??
        return render_template('home.html', id_article=id_article, titre=titre, identifiant=identifiant, auteur=auteur, date=date, paragraphe=paragraphe)


# This is always true if app.py is used as entry point of the interpretor
if __name__ == '__main__':
    app.run(port=5000)
