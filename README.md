L'exécutable main.py recoit le nom dossier qui contient les fichiers .pdf . 
Ensuite il parcourt ce dossier pour récupérer fichier par fichier afin de récupérer des données de la forme : 
	- Le nom du fichier d’origine.
	- Le titre du papier.
	- Le résumé ou abstract de l’auteur.
Une fois les données sont traitées, elles sont placées dans un fichier .txt.
Tous les fichiers .txt obtenus sont placés dans un dossier que l'exécutable crée par lui meme.

Pour lancer le programme : 
	commande : ./main.py chemin_du_dossier
