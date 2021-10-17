CREATE TABLE article (
  id integer primary key autoincrement,
  titre varchar(100),
  identifiant varchar(50),
  auteur varchar(100),
  date_publication TEXT,
  paragraphe varchar(500)
);

INSERT INTO article(titre, identifiant, auteur, date_publication, paragraphe) 
VALUES('Article 1', 5, 'Carl', "2021-10-14", "Ceci est un article que j'ai écris pour vous.");