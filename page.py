from flask import Flask, render_template
import pymysql
import pymysql.cursors

conn = pymysql.connect(host='localhost', user="root", password="root", db="projetsession")
app = Flask(__name__)

@app.route("/")
def main():
    requete = "SELECT titre_film, note_moyenne, synopsis FROM film WHERE note_moyenne > 7.5 LIMIT 5;"
    cur = conn.cursor()
    cur.execute(requete)

    films = []
    i = 0
    for Tuple in cur:
        films.append({})
        films[i]['titre'] = Tuple[0]
        films[i]['moyenne'] = Tuple[1]
        films[i]['synopsis'] = Tuple[2]
        i += 1
    cur.close()
    return render_template('index.html', films=films)

@app.route("/user/<user_id>")
def u(user_id):
    return render_template('user.html', username=user_id)


if __name__ == "__main__":
    app.run()
