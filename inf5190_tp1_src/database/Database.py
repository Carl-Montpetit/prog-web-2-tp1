
import sqlite3


class Database:
    def __init__(self):
        self.connection = None

    # Return cursor as a dict
    def to_dict(self, dict_name, cursor):
        return [dict(dict_name) for dict_name in cursor.fetchall()]

    def get_connection(self):
        """Open database connection. Should be closed after use"""
        if self.connection is None:
            self.connection = sqlite3.connect('database/database.db')
            self.connection.row_factory = sqlite3.Row
        return self.connection

    def disconnect(self):
        """Closes the database connection"""
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def get_article_by_date(self):
        connection = self.get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM article ORDER BY date_publication DESC")
        return self.to_dict("article", cursor)

    def insert_article(self, article):
        connection = self.get_connection()
        cursor = connection.cursor()

        cursor.execute("INSERT INTO article (id, titre, identifiant, auteur, date_publication, paragraphe) values (?, ?, ?, ?, ?)", [
                       article['id_article'], article['titre'], article['identifiant'], article['date'], article['paragraphe']])
        connection.commit()
        return 1
# TODO
    # methode qui permet d'effectuer une recherche dans la bd pour recuperer les
    # 5 derniers articles en date du jour
    # Indices :
    # date_aj = date.today()
    # cursor.execute("select * from article where date_publication <= ? limit 5", (date_aj,))
