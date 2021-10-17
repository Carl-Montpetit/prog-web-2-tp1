from database import Database
from flask import Flask, render_template, request, redirect, url_for, g, flash
from datetime import datetime

# Initialize flask application
app = Flask(__name__, static_folder="static",
            template_folder="templates", static_url_path="")
app.secret_key = "Carl.M"


def get_db():
    """[Get the database data in a variable]

    Returns:
        [Any]: [the database]
    """
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database

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


# DATETIME UTILS
today = datetime.now().strftime("%Y-%m-%d")

# Server perspective :
# POST  ⟹ used to receive data (from clients)
# GET   ⟹ used to send data to clients


# GET ⟹ Default route ⟹ /
# TODO : Need a search field for LIKE DB
@app.route('/', methods=['GET'])
def get_last_five_articles():
    """[The home page containing the last 5 articles from now]

    Returns:
        [Text]: [home.html]
    """
    return render_template('home.html')


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
def create_new_article():
    """[Page with form for creating a new article]

    Returns:
        [Text]: [redirect ⟹ '/' or home.html]
    """
    id_article = request.form['id-article']
    titre = request.form['titre']
    identifiant = request.form['identifiant']
    auteur = request.form['auteur']
    date = request.form['date']
    paragraphe = request.form['paragraphe']

    # if there's error the page show error messages to the user
    if id_article == "" or titre == "" or identifiant == "" or auteur == "" or date == "" or paragraphe == "":
        return render_template('admin-new.html', error='⚠️Les champs doivent impérativement être remplis!..')

    else:
        file = open('log.txt', 'a')
        file.write(f"id\t\t\t\t⟹\t{id_article}\ntitre\t\t\t⟹\t{titre}\nidentifiant\t\t⟹\t{identifiant}\nauteur\t\t\t⟹\t{auteur}\ndate\t\t\t⟹\t{date}\nparagraphe\t\t⬇︎\n{paragraphe}\n================================================================================\n")
        return render_template('home.html', id_article=id_article, titre=titre, identifiant=identifiant, auteur=auteur, date=date, paragraphe=paragraphe)


# This is always true if app.py is used as entry point of the interpretor
if __name__ == '__main__':
    app.run(port=5000)
