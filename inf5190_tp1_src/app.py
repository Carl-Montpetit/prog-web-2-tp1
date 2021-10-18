from database.Database import Database
from flask import Flask, render_template, request, redirect, url_for, g
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
ERR_MSG_TITRE = '⚠️Le champs Titre doit impérativement contenir entre 3 et 100 caractères!..'
ERR_MSG_IDENTIFIANT = '⚠️Le champs Identifiant doit impérativement contenir entre 3 et 50 caractères!..'
ERR_MSG_AUTEUR = '⚠️Le champs Auteur doit impérativement contenir entre 4 et 100 caractères!..'
ERR_MSG_DATE = '⚠️Le champs Date doit impérativement être de la forme ⟹ (YYYY-mm-jj) avec des nombres!..'
ERR_MSG_PARAGRAPHE = '⚠️Le champs Auteur doit impérativement contenir entre 1 et 500 caractères!..'
ERR_MSG_ID_NOT_UNIQUE = '⚠️Le ID choisis existe déjà, svp veuillez en choisir un autre!..'
INFO_MSG_CREATED = '✅Merci, votre article a été ajouté avec succès!..'
INFO_MSG_MODIFIED = '✅Merci, votre article a été modifié avec succès!..'
PATTERN_DATE = '^\d{4}-\d{2}-\d{2}$'


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


# TODO : show the last 5 articles
@app.route('/', methods=['GET'])
# []
def get_last_five_articles():
    articles = get_db().get_all_articles()
    return render_template(HOME_PAGE, articles=articles)

# TODO search field for LIKE DB
# @app.route('/', methods=['POST'])
# # []
# def search_articles():
#     search = request.form['search']
#     # TODO search result in database
#     return render_template(SEARCH_RESULT_PAGE)


@app.route('/article/<string:identifiant>', methods=['GET'])
# [x]
def get_an_article(identifiant):
    try:
        article = get_db().get_article_by_identifiant(identifiant)
        titre = article[0]['titre']
        identifiant = article[0]['identifiant']
        auteur = article[0]['auteur']
        date_publication = article[0]['date_publication']
        paragraphe = article[0]['paragraphe']
    except Exception:
        return render_template(ERR_404_PAGE), 404
    return render_template(ARTICLE_PAGE, titre=titre, identifiant=identifiant, auteur=auteur, date_publication=date_publication, paragraphe=paragraphe)


@app.route('/admin/<string:identifiant>', methods=['GET'])
# [x]
def get_an_article_modify(identifiant):
    try:
        article = get_db().get_article_by_identifiant(identifiant)
        titre = article[0]['titre']
        identifiant = article[0]['identifiant']
        auteur = article[0]['auteur']
        date_publication = article[0]['date_publication']
        paragraphe = article[0]['paragraphe']
    except Exception:
        return render_template(ERR_404_PAGE), 404
    return render_template(MODIFY_ARTICLE_PAGE, titre=titre, identifiant=identifiant, auteur=auteur, date_publication=date_publication, paragraphe=paragraphe)


@app.route('/admin/<string:identifiant>', methods=['POST'])
# []
def modify_article(identifiant):
    try:
        article = get_db().get_article_by_identifiant(identifiant)
    except Exception:
        return render_template(ERR_404_PAGE), 404
    get_db().modify_article(article)
    return redirect(url_for('get_admin', msg=INFO_MSG_MODIFIED))

@app.route('/admin', methods=['GET'])
# [x]
def get_admin():
    articles = get_db().get_all_articles()
    return render_template(ADMIN_PAGE, articles=articles)


@app.route('/admin-nouveau', methods=['GET'])
# [x]
def get_admin_new():
    return render_template(ADMIN_NEW_ARTICLE_PAGE)


@app.route('/admin-nouveau', methods=['POST'])
# []
def add_new_article_in_bd():
    titre = request.form['titre']
    identifiant = request.form['identifiant']
    auteur = request.form['auteur']
    date_publication = request.form['date_publication']
    date_validation = re.match(PATTERN_DATE, date_publication)
    paragraphe = request.form['paragraphe']
    article = [titre, identifiant, auteur, date_publication, paragraphe]

    # if there's error(s) the page show error message(s) to the user
    # TODO not refresh the input fields AJAX ??
    if titre == "" or identifiant == "" or auteur == "" or date_publication == "" or paragraphe == "":
        return render_template(ADMIN_NEW_ARTICLE_PAGE, error=ERR_MSG_EMPTY_FIELDS, titre=titre, identifiant=identifiant, auteur=auteur, date_publication=date_publication, paragraphe=paragraphe)
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
        get_db().insert_article(article)
        append_article_to_logfile(
            titre, identifiant, auteur, date_publication, paragraphe)
        return render_template('home.html', titre=titre, identifiant=identifiant, auteur=auteur, date_publication=date_publication, paragraphe=paragraphe, msg=INFO_MSG_CREATED)


def append_article_to_logfile(titre, identifiant, auteur, date_publication, paragraphe):
    file = open('log.txt', 'a')
    file.write(
        f"titre\t\t\t\t⟹\t{titre}\nidentifiant\t\t\t⟹\t{identifiant}\nauteur\t\t\t\t⟹\t{auteur}\ndate_publication\t\t⟹\t{date_publication}\nparagraphe\t\t⬇︎\n{paragraphe}\n================================================================================\n")


def append_modified_to_logfile(titre, paragraphe):
    file = open('log.txt', 'a')
    file.write(
        f"Modification :\ntitre\t\t\t\t⟹\t{titre}\nparagraphe\t\t⬇︎\n{paragraphe}\date\t\t⟹\t{today}\n================================================================================\n")

# This is always true if app.py is used as entry point of the interpretor
if __name__ == '__main__':
    app.run(port=5000)
