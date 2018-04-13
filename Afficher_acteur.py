from flask import Flask, render_template
import pymysql
import pymysql.cursors

conn = pymysql.connect(host='localhost', user="root", password="012345", db="tpbd")
app = Flask(__name__)


@app.route("/acteur/<id_acteur>")
def page_acteur(id_acteur):
    #Requête info acteur.
    req = "SELECT a.nom_acteur, DATE_FORMAT(a.date_naissance, '%D %M %Y'), a.pays_origine, a.sexe, a.biographie  " \
          "FROM acteur a " \
          "WHERE a.id_acteur = x"+id_acteur+";"

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
    req2 = "SELECT f.titre_film " \
           "FROM film f " \
           "JOIN INNER jour j " \
           "ON f.id_film = j.id_film " \
           "WHERE j.id_acteur =" + id_acteur + ";"
    cur.execute(req2)

    liste_filmes_joues = []
    for titre in cur:
        liste_filmes_joues.append(titre)
        titre += 1
    cur.close()

    return render_template('acteur.html', acteur = info_acteur, liste = liste_filmes_joues)

if __name__ == "__main__":
    app.run()



