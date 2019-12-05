#!/usr/bin/env python3

# import glob
# import io
import os
import shutil
import subprocess
import sys


def ResetOutputDir(pathToOutputDir):
	# Delete output dir if exists
	if os.path.exists(pathToOutputDir):
		shutil.rmtree(pathToOutputDir)

	# Make a new output dir
	os.mkdir(pathToOutputDir)


# Write the results to a txt file
def WriteToTxt(pathToOutputDir, fileName, title, author, abstract, biblio):
	txtFileName = fileName.replace(".pdf", ".txt")

	file = open(pathToOutputDir + "/" + txtFileName, "w")
	file.write("Fichier d'origine : " + fileName)
	file.write("Titre : " + title)
	file.write("Auteur(s) : " + author)
	file.write("Résumé : " + abstract)
	file.write("Bibliographie : " + biblio)
	file.close()


# Get title and author(s)
def GetTitleAndAuthors(pathToOutputDir):	
	title = ""
	author = ""
	counter = 0
	with open(pathToOutputDir + "/temp.txt", "r") as file:
		for line in file:
			line = line.replace("-\n", "")
			line = line.replace("-\r", "")
			line = line.replace("\n", " ")
			line = line.replace("\r", " ")
			if counter < 2:		# Title
				title += line
			else:				# Author
				author += line
			if ("Abstract" in line or "ABSTRACT" in line):
				break
			counter += 1
	return title, author


# Get abstract
def GetAbstract(pathToOutputDir):
	abstract = ""
	isAbstract = False
	with open(pathToOutputDir + "/temp.txt", "r") as file:
		for line in file:
			if ("Introduction\n" in line or "INTRODUCTION\n" in line):
				isAbstract = False
				break
			if isAbstract:
				line = line.replace("-\n", "")
				line = line.replace("-\r", "")
				line = line.replace("\n", " ")
				line = line.replace("\r", " ")
				abstract += line
			if ("Abstract" in line or "ABSTRACT" in line):
				isAbstract = True
	return abstract


# Get Biblio/References
def GetBiblio(pathToOutputDir):
	biblio = ""
	isBiblio = False
	with open(pathToOutputDir + "/temp.txt", "r") as file:
		for line in file:
			if isBiblio:
				line = line.replace("-\n", "")
				line = line.replace("-\r", "")
				line = line.replace("\n", " ")
				line = line.replace("\r", " ")
				biblio += line
			if ("References" in line or "REFERENCES" in line):
				isBiblio = True
	return biblio


# Write to (txt or xml) files, using all the prevous Get...() functions
def WriteToFiles(outputType, pathToInputDir, pathToOutputDir):
	for fileName in os.listdir(pathToInputDir):
		if fileName.endswith(".pdf"):
			fileNameModified = fileName.replace(" ", "\ ")
			print(fileName)

			# Use pdftotext to extract the content of the pdf file to a temp.txt file
			os.system("pdftotext -raw " + pathToInputDir + "/" + fileNameModified + " " + pathToOutputDir + "/temp.txt")

			# Get title and author(s)
			title, author = GetTitleAndAuthors(pathToOutputDir)

			# Get abstract
			abstract = GetAbstract(pathToOutputDir)

			# Get Biblio/References
			biblio = GetBiblio(pathToOutputDir)

			if outputType == "txt":
				WriteToTxt(pathToOutputDir, fileName, title, author, abstract, biblio)

			elif outputType == "xml":
				WriteToXml(pathToInputDir, pathToOutputDir)

	# Delete temp.txt
	os.remove(pathToOutputDir + "/temp.txt")


if __name__ == "__main__":
	pathToInputDir = sys.argv[1]

	outputType = sys.argv[2]
	if outputType == "-t":			# Txt generation chosen
		pathToOutputDir = pathToDir + "/Txt"
		ResetOutputDir(pathToOutputDir)
		WriteToFiles("txt", pathToInputDir, pathToOutputDir)

	elif outputType == "-x":		# Xml generation chosen
		pathToOutputDir = pathToDir + "/Xml"
		ResetOutputDir(pathToOutputDir)
		WriteToFiles("xml", pathToInputDir, pathToOutputDir)