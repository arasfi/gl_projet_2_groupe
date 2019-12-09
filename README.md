# Explications
	- L'exécutable Main.py reçoit le chemin du dossier qui contient les fichiers .pdf ainsi que le mode de sortie (-t ou -x).  
	- Le main est constitué de fonctions : 
		- ResetOutputDir(pathToOutputDir) : supprimer et/ou créer le répertoire
		- SplitFile(pathToOutputDir) : on découpe le document en plusieurs parties (isTitle, isAuthor, isAbstract, isIntro, isBody, isConclusion, isDiscussion, isBiblio), ensuite en récupère chaque parties que l'on va stocké dans les variables adéquates (respectivement : title, author, abstract, intro, body, conclusion, discussion, biblio). Dès qu'on a stocké la ligne dans la variable on passe à la ligne suivante. Ensuite on return chaque variables.
		- WriteToTxt(pathToOutputDir, fileName, title, author, abstract, intro, body, conclusion, discussion, biblio) : convertie le fichier .pdf en fichier .txt
		- WriteToXml() : convertie le fichier .pdf en fichier .xml
		- WriteToFiles(outputType, pathToInputDir, pathToOutputDir, listOfFilesToConvert) : cette fonction va appeler WriteToTxt ou WriteToXml en fonction de la sortie qu'on lui donne.
		- ListMenu(pathToInputDir) : liste les pdf dans le directoire passé en argument.
		- GetListOfFilesToConvert(numberOfFiles) : 
			- Si on saisit '*', on convertira tous les fichiers
			- Sinon on saisit les numéros (donnés grâce a ListMenu) des pdf à convertir
	
	- Tout d'abord nous récupérons le répertoire qui contient les pdf, il devra être passé en argument
	- Ensuite on créer le répertoire /Txt ou seront les fichiers .txt et le répertoire /Xml ou seront les fichiers .xml
	- Enfin on récupère le type de sortie, il devra aussi être passé en argument
		- si le deuxième argument est -t, on crée le répertoire /Txt, on convertie les fichiers pdf en fichier texte et on stocke dans le répertoire /Txt
		- si le deuxième argument est -x, on crée le répertoire /Xml, on convertie les fichiers pdf en fichier xml et on stocke dans le répertoire /Xml
	

### Pour lancer le programme : 
	Commande : python Main.py chemin_du_dossier_contenant_les_pdf -t|-x
