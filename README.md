# Explications
	- L'exécutable Main.py reçoit le chemin du dossier qui contient les fichiers .pdf. 
	- Le main est constitué de fonctions : 
		- ResetOutputDir(pathToOutputDir) : supprimer et/ou créer le répertoire ou les fichiers textes finaux seront stockés
		- GetTitleAndAuthors(pathToOutputDir) : cette fonction récupère les 2 premières lignes du fichier, nous les considèrons comme le titre et le(s) auteur(s). 
		- GetAbstract(pathToOutputDir) : cette fonction récupère l'abstract ou l'introduction de l'article
		- GetBiblio(pathToOutputDir) : cette fonction récupère les références de l'articles
		- ConvertToXml() : convertie le fichier pdf en fichier txt 
	
	- Tout d'abord nous récupérons le répertoire qui contient les pdf, il devra être passé en argument
	- Ensuite on créer le répertoire /Txt ou seront les fichiers .txt et le répertoire /Xml ou seront les fichiers .xml
	- Enfin on récupère le type de sortie, il devra aussi être passé en argument
		- si le deuxième argument est -t, on crée le répertoire /Txt, on convertie les fichiers pdf en fichier texte et on stocke dans le répertoire /Txt
		- si le deuxième argument est -x, on crée le répertoire /Xml, on convertie les fichiers pdf en fichier xml et on stocke dans le répertoire /Xml
	

### Pour lancer le programme : 
	Commande : python Main.py chemin_du_dossier_contenant_les_pdf -t|-x
