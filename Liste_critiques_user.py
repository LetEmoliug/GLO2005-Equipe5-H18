import pymysql
import pymysql.cursors

conn= pymysql.connect(host='localhost',user='root',password='Kappa',db='projetsessionoriginal' )

cur=conn.cursor()
requete = "select f.titre_film, c.titre_critique, c.date_ecriture, c.texte, c.note from critique as c inner join film as f using (id_film) where nom_usager = 'overhoud';"
cur.execute(requete)

for Tuple in cur:
    for attrib in Tuple:
        print(attrib)
    print()

cur.close()
conn.close()