#!/usr/bin/env python3

# import glob
# import io
import os
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET

# A function to create the xml file with the right structure
def CreateXmlFile(preambleString, titreString, auteurString, abstractString, biblioString):
	# create the file structure
	article = ET.Element('article')
	preamble = ET.SubElement(article, 'preamble')
	titre = ET.SubElement(article, 'titre')
	auteur = ET.SubElement(article, 'auteur')
	abstract = ET.SubElement(article, 'abstract')
	biblio = ET.SubElement(article, 'biblio')

	# put informations in Xml elements
	preamble.text = preambleString
	titre.text = titreString
	auteur.text = auteurString
	abstract.text = abstractString
	biblio.text = biblioString

	# create a new XML file with the results
	mydata = ET.tostring(article)
	myfile = open("article.xml", "wb")
	myfile.write(mydata)








# VARIABLES
pathToDir = sys.argv[1]
pathToTxtOutput = pathToDir + "/Txt"

# Delete output dir if exists
if os.path.exists(pathToTxtOutput):
	shutil.rmtree(pathToTxtOutput)

# Make a new output dir
os.mkdir(pathToTxtOutput)

# Print all pdf files in <pathToDir>
for fileName in os.listdir(pathToDir):
	if fileName.endswith(".pdf"):
		fileNameModified = fileName.replace(" ", "\ ")
		print(fileName)

		# Use pdftotext to extract the content of the pdf file to a temp.txt file
		txtFileName = fileName.replace(".pdf", ".txt")
		os.system("pdftotext -raw " + pathToDir + "/" + fileNameModified + " " + pathToTxtOutput + "/temp.txt")

		# Get file name
		text = "Fichier d'origine : " + fileName + "\n"

		# Get title
		text += "Titre : "
		counter = 0
		with open(pathToTxtOutput + "/temp.txt", "r") as file:
			for line in file:
				line = line.replace("\n", " ")
				line = line.replace("\r", " ")
				text += line
				counter += 1
				if counter == 2:
					break

		# Get abstract
		text += "\nAbstract : "
		isAbstract = False
		with open(pathToTxtOutput + "/temp.txt", "r") as file:
			for line in file:
				if ("Introduction\n" in line or "INTRODUCTION\n" in line):
					isAbstract = False
					break
				if isAbstract:
					line = line.replace("-\n", "")
					line = line.replace("-\r", "")
					line = line.replace("\n", " ")
					line = line.replace("\r", " ")
					text += line
				if ("Abstract" in line or "ABSTRACT" in line):
					isAbstract = True

		# Write the result to the file
		file = open(pathToTxtOutput + "/" + txtFileName, "w")
		file.write(text)
		file.close()

# Delete temp.txt
os.remove(pathToTxtOutput + "/temp.txt")