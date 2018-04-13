from flask import Flask, render_template, abort, request
import pymysql
import pymysql.cursors

conn = pymysql.connect(host='localhost', user="root", password="root", db="projetsession")
app = Flask(__name__)

@app.route("/")
def main():
    requete = "SELECT id_film, titre_film, note_moyenne, CONCAT(LEFT(synopsis, 330), '...') FROM film WHERE note_moyenne > 7.5 ORDER BY RAND() LIMIT 5;"
    cur = conn.cursor()
    cur.execute(requete)

    films = []
    i = 0
    for Tuple in cur:
        films.append({})
        films[i]['film_url'] = "/film/" + str(Tuple[0])
        films[i]['titre'] = Tuple[1]
        films[i]['moyenne'] = Tuple[2]
        films[i]['synopsis'] = Tuple[3]
        i += 1
    return render_template('index.html', films=films)

@app.route("/film/<film_id>")
def film_page(film_id):
    r1 = "SELECT titre_film, DATE_FORMAT(date_parution, '%D %M %Y'), duree, note_moyenne, genre, synopsis FROM film WHERE id_film=" + film_id + ";"
    cur = conn.cursor()
    cur.execute(r1)
    film_info = {}
    for Tuple in cur:
        film_info['titre'] = Tuple[0]
        film_info['date'] = Tuple[1]
        film_info['duree'] = Tuple[2]
        film_info['note'] = Tuple[3]
        film_info['genre'] = Tuple[4]
        film_info['synopsis'] = Tuple[5]

    if not bool(film_info):
        abort(404)
    r2 = "SELECT jouer.id_acteur AS id_acteur, nom_acteur FROM jouer JOIN acteur ON jouer.id_acteur=acteur.id_acteur WHERE jouer.id_film=" + film_id + ";"
    cur.execute(r2)
    acteurs = []
    i = 0
    for Tuple in cur:
        acteurs.append({})
        acteurs[i]['acteur_url'] = "/acteur/" + str(Tuple[0])
        acteurs[i]['nom'] = Tuple[1]
        i += 1

    r3 = "SELECT creer.id_realisateur AS id_realisateur, nom_realisateur FROM creer JOIN realisateur ON creer.id_realisateur=realisateur.id_realisateur WHERE creer.id_film=" + film_id + ";"
    cur.execute(r3)
    realisateurs = []
    i = 0
    for Tuple in cur:
        realisateurs.append({})
        realisateurs[i]['realisateur_url'] = "/realisateur/" + str(Tuple[0])
        realisateurs[i]['nom'] = Tuple[1]
        i += 1
    cur.close()

    return render_template('film.html', film=film_info, acteurs=acteurs, realisateurs=realisateurs)

@app.route("/user/<user_id>")
def user_page(user_id):
    return render_template('user.html', username=user_id)

@app.route("/ResultatRecherche", methods=['POST'])
def ResultatsRecherche():
    recherche = request.form.get('recherche')
    requete_films = "SELECT id_film, titre_film FROM film WHERE titre_film LIKE '%" + recherche + "%';"
    cur = conn.cursor()
    cur.execute(requete_films)

    film = []
    i = 0
    for Tuple in cur:
        film.append({})
        film[i]['film_url'] = "/film/" + str(Tuple[0])
        film[i]['titre'] = Tuple[1]
        i += 1

    requete_acteur = "SELECT id_acteur, nom_acteur FROM acteur WHERE nom_acteur LIKE '%" + recherche + "%';"
    cur = conn.cursor()
    cur.execute(requete_acteur)

    acteur = []
    i = 0
    for Tuple in cur:
        acteur.append({})
        acteur[i]['acteur_url'] = "/acteur/" + str(Tuple[0])
        acteur[i]['nom'] = Tuple[1]
        i += 1

    requete_realisateur = "SELECT id_realisateur, nom_realisateur FROM realisateur WHERE nom_realisateur LIKE '%" + recherche + "%';"
    cur = conn.cursor()
    cur.execute(requete_realisateur)

    realisateur = []
    i = 0
    for Tuple in cur:
        realisateur.append({})
        realisateur[i]['realisateur_url'] = "/realisateur/" + str(Tuple[0])
        realisateur[i]['nom'] = Tuple[1]
        i += 1

    requete_utilisateur = "SELECT nom_usager FROM utilisateur WHERE nom_usager LIKE '%" + recherche + "%';"
    cur = conn.cursor()
    cur.execute(requete_utilisateur)

    utilisateur = []
    i = 0
    for Tuple in cur:
        utilisateur.append({})
        utilisateur[i]['utilisateur_url'] = "/utilisateur/" + str(Tuple[0])
        utilisateur[i]['nom'] = Tuple[0]
        i += 1
    return render_template('ResultatRecherche.html', film=film, acteur=acteur, realisateur=realisateur, utilisateur=utilisateur)

@app.route("/Films")
def Films():
    requete = "SELECT id_film, titre_film, note_moyenne, CONCAT(LEFT(synopsis, 330), '...') FROM film;"
    cur = conn.cursor()
    cur.execute(requete)

    films = []
    i = 0
    for Tuple in cur:
        films.append({})
        films[i]['film_url'] = "/film/" + str(Tuple[0])
        films[i]['titre'] = Tuple[1]
        films[i]['moyenne'] = Tuple[2]
        films[i]['synopsis'] = Tuple[3]
        i += 1
    return render_template('films.html', films=films)

if __name__ == "__main__":
    app.run()
