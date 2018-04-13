from flask import Flask, render_template
import pymysql
import pymysql.cursors

conn = pymysql.connect(host='localhost', user="root", password="012345", db="tpbd")
app = Flask(__name__)


@app.route("/realisateur/<id_realisateur>")
def page_acteur(id_realisateur):
    #Requête info realisateur.
    req = "SELECT r.nom_realisateur, DATE_FORMAT(r.date_naissance, '%D %M %Y'), r.pays_origine, r.sexe, r.biographie  FROM realisateur r WHERE r.id_realisateur = x"+id_realisateur+";"

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
    req2 = "SELECT f.titre_film " \
           "FROM film f " \
           "JOIN INNER creer c " \
           "ON f.id_film = c.id_film " \
           "WHERE c.id_realisateur =" + id_realisateur + ";"
    cur.execute(req2)

    liste_filmes_crees = []
    for titre in cur:
        liste_filmes_crees.append(titre)
        titre += 1
    cur.close()

    return render_template('realisateur.html', realisateur = info_realisateur, liste = liste_filmes_crees)

if __name__ == "__main__":
    app.run()