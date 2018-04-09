from flask import Flask, render_template
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
    cur.close()
    return render_template('index.html', films=films)

@app.route("/film/<film_id>")
def film_page(film_id):
    # Je n'ai pas encore changé le template juste pour éviter un plantage en cliquant sur les liens
    # de la page d'accueil.
    # Changer template pour film.html et changer les variables de template associé
    return render_template('user.html', username=film_id)

@app.route("/user/<user_id>")
def user_page(user_id):
    return render_template('user.html', username=user_id)


if __name__ == "__main__":
    app.run()
