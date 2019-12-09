#!/usr/bin/env python3

# import glob
# import io
import os
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET


def ResetOutputDir(pathToOutputDir):
	# Delete output dir if exists
	if os.path.exists(pathToOutputDir):
		shutil.rmtree(pathToOutputDir)

	# Make a new output dir
	os.mkdir(pathToOutputDir)


# Get abstract, introduction, body, conclusion and discussion
def SplitFile(pathToOutputDir):
	title,   author,   abstract,   intro,   body,   conclusion,   discussion,   biblio   = "",   "",    "",    "",    "",    "",    "",    ""
	isTitle, isAuthor, isAbstract, isIntro, isBody, isConclusion, isDiscussion, isBiblio = True, False, False, False, False, False, False, False

	counter = 0
	with open(pathToOutputDir + "/temp.txt", "r") as file:
		for line in file:
			# Author part
			if counter == 3:
				isTitle, isAuthor, isAbstract, isIntro, isBody, isConclusion, isDiscussion, isBiblio = False, True, False, False, False, False, False, False

			# Abstract part
			if "Abstract" in line or "ABSTRACT" in line:
				isTitle, isAuthor, isAbstract, isIntro, isBody, isConclusion, isDiscussion, isBiblio = False, False, True, False, False, False, False, False

			# Introduction part
			if "Introduction\n" in line or "INTRODUCTION\n" in line:
				isTitle, isAuthor, isAbstract, isIntro, isBody, isConclusion, isDiscussion, isBiblio = False, False, False, True, False, False, False, False

			# Body part
			# line.startswith("2\n") or line.startswith("II\n") or 
			if line.startswith("2. ") or line.startswith("II. ") or line.startswith("Corpus") or line == "2\n":
				isTitle, isAuthor, isAbstract, isIntro, isBody, isConclusion, isDiscussion, isBiblio = False, False, False, False, True, False, False, False

			# Conclusion part
			#  or "CONCLUSIONS" in line
			if "Conclusion\n" in line or "CONCLUSION\n" in line or "Conclusions"in line:
				isTitle, isAuthor, isAbstract, isIntro, isBody, isConclusion, isDiscussion, isBiblio = False, False, False, False, False, True, False, False

			# Discussion part
			if "Discussion\n" in line or "DISCUSSION\n" in line:
				isTitle, isAuthor, isAbstract, isIntro, isBody, isConclusion, isDiscussion, isBiblio = False, False, False, False, False, False, True, False

			# Biblio part
			# "References\n" in line or "REFERENCES\n" in line
			if line.startswith("References\n") or line.startswith("REFERENCES\n"):
				isTitle, isAuthor, isAbstract, isIntro, isBody, isConclusion, isDiscussion, isBiblio = False, False, False, False, False, False, False, True

			line = line.replace("-\n", "")
			line = line.replace("-\r", "")
			line = line.replace("\n", " ")
			line = line.replace("\r", " ")

			if isTitle:				# Is title
				title += line
			if isAuthor:			# Is author
				author += line
			if isAbstract:			# Is abstract
				abstract += line
			if isIntro:				# Is introduction
				intro += line
			if isBody:				# Is body
				body += line
			if isConclusion:		# Is conclusion
				conclusion += line
			if isDiscussion:		# Is discussion
				discussion += line
			if isBiblio:				# Is biblio
				biblio += line

			counter += 1

	return title, author, abstract, intro, body, conclusion, discussion, biblio


# Write the results to a txt file
def WriteToTxt(pathToOutputDir, fileName, title, author, abstract, intro, body, conclusion, discussion, biblio):
	txtFileName = fileName.replace(".pdf", ".txt")
	print("Creating \"" + txtFileName + "\"...")

	file = open(pathToOutputDir + "/" + txtFileName, "w")

	file.write("Fichier d'origine :\n" + fileName + "\n\n")
	file.write("Titre :\n" + title + "\n\n")
	file.write("Auteur(s) :\n" + author + "\n\n")
	file.write("Résumé :\n" + abstract + "\n\n")
	file.write("Introduction :\n" + intro + "\n\n")
	file.write("Corps :\n" + body + "\n\n")
	file.write("Conclusion :\n" + conclusion + "\n\n")
	file.write("Discussion :\n" + discussion + "\n\n")
	file.write("Bibliographie :\n" + biblio + "\n\n")

	file.close()


# A function to create the xml file with the right structure
def WriteToXml(pathToOutputDir, fileName, title, author, abstract, biblio):
	xmlFileName = fileName.replace(".pdf", ".xml")
	print("Creating \"" + xmlFileName + "\"...")

	# create the file structure
	articleTag = ET.Element('article')
	preambleTag = ET.SubElement(articleTag, 'preamble')
	titleTag = ET.SubElement(articleTag, 'titre')
	authorTag = ET.SubElement(articleTag, 'auteur')
	abstractTag = ET.SubElement(articleTag, 'abstract')
	biblioTag = ET.SubElement(articleTag, 'biblio')

	# put informations in Xml elements
	preambleTag.text = fileName
	titleTag.text = title
	authorTag.text = author
	abstractTag.text = abstract
	biblioTag.text = biblio

	# create a new XML file with the results
	data = ET.tostring(articleTag)
	file = open(pathToOutputDir + "/" + xmlFileName, "wb")
	file.write(data)
	file.close()


# Write to (txt or xml) files, using all the prevous Get...() functions
def WriteToFiles(outputType, pathToInputDir, pathToOutputDir, listOfFilesToConvert):
	fileIndex = 0
	print()
	for fileName in os.listdir(pathToInputDir):
		if fileName.endswith(".pdf"):
			if listOfFilesToConvert[fileIndex] == True:
				fileNameModified = fileName.replace(" ", "\ ")

				# Use pdftotext to extract the content of the pdf file to a temp.txt file
				os.system("pdftotext " + pathToInputDir + "/" + fileNameModified + " " + pathToOutputDir + "/temp.txt")

				# Split the text into 8 different parts
				title, author, abstract, intro, body, conclusion, discussion, biblio = SplitFile(pathToOutputDir)

				if outputType == "txt":
					WriteToTxt(pathToOutputDir, fileName, title, author, abstract, intro, body, conclusion, discussion, biblio)

				elif outputType == "xml":
					WriteToXml(pathToOutputDir, fileName, title, author, abstract, biblio)

			fileIndex += 1

	# Delete temp.txt
	os.remove(pathToOutputDir + "/temp.txt")


def ListMenu(pathToInputDir):
	fileIndex = 0
	for fileName in os.listdir(pathToInputDir):
		if fileName.endswith(".pdf"):
			fileIndex += 1
			fileNameModified = fileName.replace(" ", "\ ")
			print(str(fileIndex) + " " + fileName)

	return fileIndex


def GetListOfFilesToConvert(numberOfFiles) :
	filesToConvertInput = input("\nVeuillez donner les fichiers à convertir (separés par des virgules) : ")
	
	if filesToConvertInput != "*":
		filesToConvertArray = filesToConvertInput.split(',')
		for i in range(len(filesToConvertArray)):
			filesToConvertArray[i] = int(filesToConvertArray[i]) - 1

	listOfFilesToConvert = []
	for i in range(numberOfFiles):
		if filesToConvertInput == "*":
			listOfFilesToConvert.append(True)
		elif i not in filesToConvertArray:
			listOfFilesToConvert.append(False)
		else:
			listOfFilesToConvert.append(True)

	return listOfFilesToConvert


if __name__ == "__main__":
	pathToInputDir = sys.argv[1]

	numberOfFiles = ListMenu(pathToInputDir)
	listOfFilesToConvert = GetListOfFilesToConvert(numberOfFiles)

	outputType = sys.argv[2]
	if outputType == "-t":			# Txt generation chosen
		pathToOutputDir = pathToInputDir + "/Txt"
		ResetOutputDir(pathToOutputDir)
		WriteToFiles("txt", pathToInputDir, pathToOutputDir, listOfFilesToConvert)

	elif outputType == "-x":		# Xml generation chosen
		pathToOutputDir = pathToInputDir + "/Xml"
		ResetOutputDir(pathToOutputDir)
		WriteToFiles("xml", pathToInputDir, pathToOutputDir, listOfFilesToConvert)