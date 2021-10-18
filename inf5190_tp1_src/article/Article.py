class Article:
    def __init__(self, titre, identifiant, auteur, date_publication, paragraphe):
        self.titre = titre
        self.identifiant = identifiant
        self.auteur = auteur
        self.date_publication = date_publication
        self.paragraphe = paragraphe

    def to_dictionnary(self):
        """[map everything as a dictionnary]
        """
        return {
            "titre": self.titre,
            "identifiant": self.identifiant,
            "auteur": self.auteur,
            "date_publication": self.date_publication,
            "paragraphe": self.paragraphe
        }
            
