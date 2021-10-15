
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

    def get_individual_by_lastname(self):
        connection = self.get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM individual ORDER BY lastname ASC")
        return self.to_dict("individual", cursor)

    def insert_individual(self, individual):
        connection = self.get_connection()
        cursor = connection.cursor()

        cursor.execute("INSERT INTO individual(lastname, firstname, age) values (?, ?, ?)", [
                       individual['lastname'], individual['firstname'], individual['age']])
        connection.commit()
        return 1
# TODO
    # methode qui permet d'effectuer une recherche dans la bd pour recuperer les
    # 5 derniers articles en date du jour
    # Indices :
    # date_aj = date.today()
    # cursor.execute("select * from article where date_publication <= ? limit 5", (date_aj,))
