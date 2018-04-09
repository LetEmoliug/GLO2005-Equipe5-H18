SELECT titre, note_moyenne, synopsis FROM film WHERE note_moyenne > 7.5 LIMIT 5 ORDER DESC;

SELECT * FROM film WHERE id_film=[id];

SELECT * FROM utilisateur WHERE nom_usager=[nom];

SELECT * FROM critique WHERE id_film=[id];

SELECT * FROM critique WHERE nom_usager=[nom];

SELECT * FROM acteur JOIN jouer ON jouer.id_acteur = acteur.id_acteur JOIN film ON jouer.id_film = film.id_film;

SELECT * FROM realisateur JOIN jouer ON jouer.id_realisateur = realisateur.id_realisateur JOIN film ON jouer.id_film = film.id_film;
