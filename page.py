from flask import Flask, render_template, abort, request, redirect, make_response
import pymysql
import pymysql.cursors
import hashlib

conn = pymysql.connect(host='localhost', user="root", password="root", db="projetsession")
app = Flask(__name__)

VarGlobal = {}

def getUserToken():
    return request.cookies.get('token')

@app.route("/")
def main():
    token = getUserToken()
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
    return render_template('index.html', films=films, token=token)

@app.route("/film/<film_id>", methods=['GET', 'POST'])
def film_page(film_id):
    token = getUserToken()
    titre_crit = request.form.get("titre_crit")
    note = request.form.get('note')
    texte = request.form.get("texte")
    modification = request.form.get("update_button")
    suppression = request.form.get("delete_button")
    titre_crit_modif = request.form.get("titre_crit_modif")
    note_modif = request.form.get('note_modif')
    texte_modif = request.form.get("texte_modif")

    cur = conn.cursor()

    if suppression:
        delete_crit = "delete from critique where nom_usager = '" + token + "' and id_film = " + film_id + ";"
        cur.execute(delete_crit)
        conn.commit()

        auto_inc = "select max(id_critique)from critique;"
        cur.execute(auto_inc)
        for Tuple in cur:
            inc_value = str(Tuple[0])

        update_auto_increment = "alter table critique AUTO_INCREMENT = " + inc_value + ";"
        cur.execute(update_auto_increment)
        conn.commit()

    if titre_crit_modif and note_modif and texte_modif:
        req_update = "update critique set texte='"+texte_modif+"', note="+note_modif+", titre_critique='"+titre_crit_modif+"' where nom_usager='"+token+"' and id_film="+film_id+";"
        cur.execute(req_update)
        conn.commit()

    if titre_crit and note and texte:
        insertion = "insert into critique(nom_usager, id_film, titre_critique, date_ecriture, texte, note) values('"+token+"', "+film_id+", '"+titre_crit+"', curdate(), '"+texte+"', '"+note+"');"
        cur.execute(insertion)
        conn.commit()

    r1 = "SELECT titre_film, DATE_FORMAT(date_parution, '%D %M %Y'), duree, note_moyenne, genre, synopsis FROM film WHERE id_film=" + film_id + ";"
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
    usagers = []
    usager_courant = {}
    i = 0
    for Tuple in cur:
        critiques.append({})
        critiques[i]['nom_usager'] = Tuple[0]
        critiques[i]['titre_critique'] = Tuple[1]
        critiques[i]['date_ecriture'] = Tuple[2]
        critiques[i]['texte'] = Tuple[3]
        critiques[i]['note'] = Tuple[4]
        critiques[i]['nom_usager_url'] = "/user/" + str(Tuple[0])

        usagers.append(Tuple[0]) #liste d'usagers qui ont critiqué le film

        if Tuple[0] == token:
            usager_courant['titre_critique'] = Tuple[1]
            usager_courant['texte'] = Tuple[3]
            usager_courant['note'] = Tuple[4]

        i += 1
    cur.close()

    return render_template('film.html', film=film_info, acteurs=acteurs, realisateurs=realisateurs, critiques=critiques,
                           token=token, usagers=usagers, modification=modification, usager_courant=usager_courant)

@app.route("/user/<user_id>")
def user_page(user_id):
    token = getUserToken()
    cur = conn.cursor()

    req1 = "select u.date_creation from utilisateur u where user_id = " + user_id + ";"
    cur.execute(req1)
    date_creation = cur

    req2 = "select f.titre_film from film f inner join favoris fv on f.id_film = fv.id_film where fv.nom_usager = " + user_id + ";"
    cur.exsecute(req2)

    liste_filmes_favoris = []
    i = 0
    for Tuple in cur:
        liste_filmes_favoris.append({})
        liste_filmes_favoris[i]['film_url'] = "/film/" + str(Tuple[0])
        liste_filmes_favoris[i]['titre'] = Tuple[1]
        i += 1

    req3 = "select usager_qui_suit from suivre where usager_suivi = " + user_id + ";"
    cur.execute(req3)

    liste_users_qui_suivent = []
    i = 0
    for Tuple in cur:
        liste_users_qui_suivent.append({})
        liste_users_qui_suivent[i]['user_url'] = "/user/" + str(Tuple[0])
        liste_users_qui_suivent[i]['username'] = Tuple[0]
        i += 1

    req4 = "select usager_suivit from suivre where usager_qui_suit = " + user_id + ";"
    cur.execute(req4)

    liste_users_suivit = []
    i = 0
    for Tuple in cur:
        liste_users_suivit.append({})
        liste_users_suivit[i]['user_url'] = "/user/" + str(Tuple[0])
        liste_users_suivit[i]['username'] = Tuple[0]
        i += 1

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
    return render_template('user.html', liste= liste_filmes_favoris, date = date_creation, suivit = liste_users_qui_suivent, suit = liste_users_suivit, nom_usager=user_id, critiques=critiques, token=token)

@app.route("/ResultatRecherche", methods=['POST'])
def ResultatsRecherche():
    token = getUserToken()

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
        utilisateur[i]['utilisateur_url'] = "/user/" + str(Tuple[0])
        utilisateur[i]['nom'] = Tuple[0]
        i += 1
    return render_template('ResultatRecherche.html', film=film, acteur=acteur, realisateur=realisateur, utilisateur=utilisateur, token=token)

@app.route("/Films")
def Films():
    token = getUserToken()
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
    #return render_template('ResultatRecherche.html', films=films)
    return render_template('films.html', films=films, token=token)

@app.route("/signup")
def signup():
    token = getUserToken()
    return render_template('signup.html', token=token)

@app.route("/checksignup", methods=['POST'])
def checksignup():
    username = request.form.get('username')
    password = request.form.get('password')
    if username == password:
        return redirect('/signup')
    r = "SELECT COUNT(nom_usager) FROM utilisateur WHERE nom_usager LIKE '" + username + "';"
    cur = conn.cursor()
    cur.execute(r)
    for Tuple in cur:
        if Tuple[0] == 1:
            return redirect('/signup')
    insert = "INSERT INTO utilisateur VALUES('" + username + "', DATE(NOW()), SHA2('" + password + "', 256));"
    cur.execute(insert)
    conn.commit()
    #username = hashlib.sha256(bytes(username), encoding='utf-8').hexdigest()
    resp = make_response(redirect('/'))
    resp.set_cookie('token', username)
    return resp

@app.route("/login")
def login():
    token = getUserToken()
    return render_template('login.html', token=token)

@app.route("/checklogin", methods=['POST'])
def checklogin():
    username = request.form.get('username')
    password = request.form.get('password')

    r = "SELECT COUNT(nom_usager) FROM utilisateur WHERE nom_usager LIKE '" + username + "' AND mot_de_passe LIKE SHA2('" + password + "', 256);"
    cur = conn.cursor()
    cur.execute(r)

    for Tuple in cur:
        if Tuple[0] == 0:
            return redirect('/login')
    #username = hashlib.sha256(bytes(username, encoding='utf-8')).hexdigest()
    resp = make_response(redirect('/'))
    resp.set_cookie('token', username)
    return resp

@app.route("/logout")
def logout():
    resp = make_response(redirect('/'))
    resp.set_cookie('token', '', expires=0)
    return resp

@app.route("/acteur/<id_acteur>")
def page_acteur(id_acteur):
    token = getUserToken()
    #Requête info acteur.
    req = "SELECT a.nom_acteur, DATE_FORMAT(a.date_naissance, '%D %M %Y'), a.pays_origine, a.sexe, a.biographie FROM acteur a WHERE a.id_acteur LIKE '" + id_acteur + "';"

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
    req2 = "SELECT f.id_film, f.titre_film FROM film f JOIN jouer j ON f.id_film = j.id_film WHERE j.id_acteur=" + id_acteur + ";"
    cur.execute(req2)

    liste_filmes_joues = []
    i = 0
    for Tuple in cur:
        liste_filmes_joues.append({})
        liste_filmes_joues[i]['film_url'] = "/film/" + str(Tuple[0])
        liste_filmes_joues[i]['titre'] = Tuple[1]
        i += 1
    cur.close()

    return render_template('acteur.html', acteur = info_acteur, liste = liste_filmes_joues, token=token)

@app.route("/realisateur/<id_realisateur>")
def page_realisateur(id_realisateur):
    token = getUserToken()
    #Requête info realisateur.
    req = "SELECT a.nom_realisateur, DATE_FORMAT(a.date_naissance, '%D %M %Y'), a.pays_origine, a.sexe, a.biographie FROM realisateur a WHERE a.id_realisateur LIKE '" + id_realisateur + "';"

    cur = conn.cursor()
    cur.execute(req)

    info_realisateur = {}
    for Tuple in cur:
        info_realisateur['nom'] = Tuple[0]
        info_realisateur['date'] = Tuple[1]
        info_realisateur['pays_origine'] = Tuple[2]
        info_realisateur['sexe'] = Tuple[3]
        info_realisateur['biographie'] = Tuple[4]

    #Requête titres des films ou l'realisateur a participé.
    req2 = "SELECT f.id_film, f.titre_film FROM film f JOIN creer j ON f.id_film = j.id_film WHERE j.id_realisateur=" + id_realisateur + ";"
    cur.execute(req2)

    liste_filmes_crees = []
    i = 0
    for Tuple in cur:
        liste_filmes_crees.append({})
        liste_filmes_crees[i]['film_url'] = "/film/" + str(Tuple[0])
        liste_filmes_crees[i]['titre'] = Tuple[1]
        i += 1
    cur.close()

    return render_template('realisateur.html', realisateur = info_realisateur, liste = liste_filmes_crees, token=token)

if __name__ == "__main__":
    app.run()
