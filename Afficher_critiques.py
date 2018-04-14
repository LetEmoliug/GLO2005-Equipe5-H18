from flask import Flask, render_template, abort, request
import pymysql
import pymysql.cursors

conn = pymysql.connect(host='localhost', user="root", password="012345", db="tpbd")
app = Flask(__name__)

VarGlobal = {}

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

    r4 = "select nom_usager, titre_critique, DATE_FORMAT(date_ecriture, '%D %M %Y'), texte, note from critique where id_film =" + film_id + ";"
    cur.execute(r4)
    critiques = []
    i = 0
    for Tuple in cur:
        critiques.append({})
        critiques[i]['nom_usager'] = Tuple[0]
        critiques[i]['titre_critique'] = Tuple[1]
        critiques[i]['date_ecriture'] = Tuple[2]
        critiques[i]['texte'] = Tuple[3]
        critiques[i]['note'] = Tuple[4]
        critiques[i]['nom_usager_url'] = "/user/" + str(Tuple[0])
        i += 1
    cur.close()

    return render_template('film.html', film=film_info, acteurs=acteurs, realisateurs=realisateurs, critiques=critiques)

@app.route("/user/<user_id>")
def user_page(user_id):
    cur = conn.cursor()

    requete1 = "select f.titre_film, c.titre_critique, c.date_ecriture, c.texte, c.note, id_film from critique as c inner join film as f using(id_film) where nom_usager ='" + user_id + "';"
    cur.execute(requete1)
    critiques = []
    i = 0
    for Tuple in cur:
        critiques.append({})
        critiques[i]['titre_film'] = Tuple[0]
        critiques[i]['titre_critique'] = Tuple[1]
        critiques[i]['date_ecriture'] = Tuple[2]
        critiques[i]['texte'] = Tuple[3]
        critiques[i]['note'] = Tuple[4]
        critiques[i]['film_url'] = "/film/" + str(Tuple[5])
        i += 1

    cur.close()
    return render_template('user.html', nom_usager=user_id, critiques=critiques)

@app.route("/ResultatRecherche", methods=['POST'])
def ResultatsRecherche():
    recherche = request.form.get('recherche')
    requete = "SELECT id_film, titre_film, note_moyenne, CONCAT(LEFT(synopsis, 330), '...') FROM film WHERE titre_film LIKE '%" + recherche + "%';"
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
    return render_template('ResultatRecherche.html', films=films)

@app.route("/realisateur/<id_realisateur>")

def page_realisateur(id_realisateur):
    #Requête info realisateur.
    req = "SELECT r.nom_realisateur, DATE_FORMAT(r.date_naissance, '%D %M %Y'), r.pays_origine, r.sexe, r.biographie FROM realisateur r WHERE r.id_realisateur = " + id_realisateur +";"
           #SELECT r.nom_realisateur, DATE_FORMAT(r.date_naissance, '%D %M %Y'), r.pays_origine, r.sexe, r.biographie FROM realisateur r WHERE r.id_realisateur = 23;
    cur = conn.cursor()
    cur.execute(req)

    info_realisateur = {}
    for Tuple in cur:
        info_realisateur['nom'] = Tuple[0]
        info_realisateur['date'] = Tuple[1]
        info_realisateur['pays_origine'] = Tuple[2]
        info_realisateur['sexe'] = Tuple[3]
        info_realisateur['biographie'] = Tuple[4]

    #Requête titres des films que le realisateur a crée.
    req2 = "SELECT f.titre_film FROM film f INNER JOIN creer c ON f.id_film = c.id_film WHERE c.id_realisateur = " + id_realisateur + ";"
    cur.execute(req2)


    liste_filmes_crees = []
    for Tuple in cur:
        liste_filmes_crees.append(Tuple)

    cur.close()

    return render_template('realisateur.html', realisateur = info_realisateur, liste = liste_filmes_crees)

@app.route("/acteur/<id_acteur>")
def page_acteur(id_acteur):
    #Requête info acteur.
    req = "SELECT a.nom_acteur, DATE_FORMAT(a.date_naissance, '%D %M %Y'), a.pays_origine, a.sexe, a.biographie FROM acteur a WHERE a.id_acteur = "+id_acteur+";"

    cur = conn.cursor()
    cur.execute(req)

    info_acteur = {}
    for Tuple in cur:
        info_acteur['nom'] = Tuple[0]
        info_acteur['date'] = Tuple[1]
        info_acteur['pays_origine'] = Tuple[2]
        info_acteur['sexe'] = Tuple[3]
        info_acteur['biographie'] = Tuple[4]

    #Requête titres des films ou l'acteur a participé.
    req2 = "SELECT f.titre_film, f.id_film FROM film f INNER JOIN jouer j ON f.id_film = j.id_film WHERE j.id_acteur =" + id_acteur + ";"
    cur.execute(req2)

    dictionaire_film = {}

    for film, id in cur:
        if id not in dictionaire_film:
            dictionaire_film[film] = [id]
        else:
            dictionaire_film[film].append(id)
    cur.close()

    return render_template('acteur.html', acteur=info_acteur, liste=dictionaire_film)

if __name__ == "__main__":
    app.run()