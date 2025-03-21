# Fonctionnement du programme :

Il s’agit d’un fichier python.

Utilise les modules requests et time, importés en début de code.

En début d’utilisation le programme demande à l’opérateur de rentrer l’identifiant de départ (x) et l’identifiant de fin d’extraction (y), permettant d’extraire les données désirées. Les valeurs d’identification sont convertis dans le code pour que cela corresponde à un nombre de jour (ex : rentrer « 1 » en identifiant de départ et de fin extrait toutes les données du 01/12/2017 contenus sur les serveurs).

Le programme intègre une variable « eh » servant à énumérer le nombre de réponses négatives à une extraction.

Le token d’accès donné à notre groupe pour accéder au serveur est intégré au programme (gp_id), mais comme nous avons été informés de la possibilité que le token puisse changer, nous avons intégré la demande de confirmation du token actuel, avec la possibilité de rentrer le nouveau token à utiliser (celui-ci ne sera pas conservé dans le programme par la suite cependant).

Après toutes ces confirmations, le programme débute :

La première étape consiste en la création de la base (locations_data, meteo_data, calendrier_data) qui servira pour l’écriture des 3 fichiers csv obtenus en sortis, c’est à dire l’ajout des en-tête pour chacun d’entre eux dans leur propre variable (met_line, cal_line, loc_line).
Ensuite vient la première série de boucle, pour le port 8100, correspondant aux données sur le jour. Le serveur est accédé en rentrant son adresse qui comprend l’id et le token, un minuteur est intégré dans cette section pour ne pas dépasser le nombre de demandes par secondes du serveur et empêcher qu’une extraction échoue.

Un print est employé pour indiquer à l’opérateur si le serveur est accédé avec succès (code 200) ou non, si la connexion a été établie alors on passe à l’extraction elle-même :
chaque ligne de données est récupérée et placée dans sa liste dédiée grâce à l’utilisation de splitlines et strip.
Afin d’avoir un premier nettoyage des données les en-têtes des données sont ignorées et les « NA » correspondant ) des données absentes sont remplacées par une valeur vide.

La boucle se répète jusqu’à ce que tous les id demandés à être traités le sont.

Le début de la deuxième étape est la conversion de x et y pour les ports 8080 et 8090, contrairement au port 8100 ces données correspondent à 1 identifiant = 1 heure d’une journée. Cela correspond à une multiplication par 24 du nombre de serveurs à consulter pour ces deux ports.

Après cela on rentre dans la deuxième boucle dédiée aux ports 8080 et 8090 qui suit les mêmes étapes que pour la première boucle.

La dernière étape de traitement consiste en l’écriture des 3 fichiers csv grâce aux listes dédiés, par le biais des commande open et write.

L’opérateur est informé de la fin du processus et du nombre d’échec d’exportation, si ce nombre est supérieur à 1 une petite aide apparaît pour indiquer les erreurs les plus communes.
