# Execution
	- L'exécutable Main.py reçoit le chemin du dossier qui contient les fichiers .pdf. 
	- Ensuite il parcourt ce dossier et traite chaque fichier afin de récupérer des données de la forme : 
		- Nom du fichier d’origine;
		- Titre du papier;
		- Résumé ou abstract de l’auteur.
	- Une fois que les données sont traitées, elles sont placées dans un fichier .txt.
	- Tous les fichiers .txt obtenus sont placés dans un dossier nommé "Txt" que l'exécutable crée lui-même dans le dossier contant les fichiers pdf.

### Pour lancer le programme : 
	Commande : ./Main.py chemin_du_dossier_contenant_les_pdf
