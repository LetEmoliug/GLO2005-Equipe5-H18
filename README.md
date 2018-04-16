# GLO2005-Equipe5-H18
Projet de session H18 du projet de GLO-2005

## Structure du projet

Les templates HTML doivent êtres inclus dans `/templates` pour être interprétés par Flask  

Les CSS doivent êtres inclus dans `/static/css` pour que Flask puissent les reconnaître.  

De plus, il faudra inclure la ligne suivante dans le header du fichier HTML dans lequel vous souhaitez intégrer votre CSS `<link rel="stylesheet" type="text/css" href="{{ url_for('static',filename='css/nom_de_fichier.css') }}">`

## Importer la database

En ligne de commande UNIX, il suffit de taper la ligne de commande suivante, où `[username]` correspond à votre nom d'utilisateur :
`mysql -u [username] -p < BD.sql`.

La base de données sera ensuite importée sous le nom `projetsession`.
