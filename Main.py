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
			if counter == 3:											# Author part
				isTitle, isAuthor, isAbstract, isIntro, isBody, isConclusion, isDiscussion, isBiblio = False, True, False, False, False, False, False, False
			if "Abstract" in line or "ABSTRACT" in line:				# Abstract part
				isTitle, isAuthor, isAbstract, isIntro, isBody, isConclusion, isDiscussion, isBiblio = False, False, True, False, False, False, False, False
			if "Introduction\n" in line or "INTRODUCTION\n" in line:	# Introduction part
				isTitle, isAuthor, isAbstract, isIntro, isBody, isConclusion, isDiscussion, isBiblio = False, False, False, True, False, False, False, False
			if line == "2\n":											# Body part
				isTitle, isAuthor, isAbstract, isIntro, isBody, isConclusion, isDiscussion, isBiblio = False, False, False, False, True, False, False, False
			if "Conclusion\n" in line or "CONCLUSION\n" in line:		# Conclusion part
				isTitle, isAuthor, isAbstract, isIntro, isBody, isConclusion, isDiscussion, isBiblio = False, False, False, False, False, True, False, False
			if "Discussion\n" in line or "DISCUSSION\n" in line:		# Discussion part
				isTitle, isAuthor, isAbstract, isIntro, isBody, isConclusion, isDiscussion, isBiblio = False, False, False, False, False, False, True, False
			if "References\n" in line or "REFERENCES\n" in line:		# Biblio part
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
def WriteToFiles(outputType, pathToInputDir, pathToOutputDir):
	for fileName in os.listdir(pathToInputDir):
		if fileName.endswith(".pdf"):
			fileNameModified = fileName.replace(" ", "\ ")
			print(fileName)

			# Use pdftotext to extract the content of the pdf file to a temp.txt file
			os.system("pdftotext " + pathToInputDir + "/" + fileNameModified + " " + pathToOutputDir + "/temp.txt")

			# Split the text into 8 different parts
			title, author, abstract, intro, body, conclusion, discussion, biblio = SplitFile(pathToOutputDir)

			if outputType == "txt":
				WriteToTxt(pathToOutputDir, fileName, title, author, abstract, intro, body, conclusion, discussion, biblio)

			elif outputType == "xml":
				WriteToXml(pathToOutputDir, fileName, title, author, abstract, biblio)

	# Delete temp.txt
	os.remove(pathToOutputDir + "/temp.txt")


if __name__ == "__main__":
	pathToInputDir = sys.argv[1]

	outputType = sys.argv[2]
	if outputType == "-t":			# Txt generation chosen
		pathToOutputDir = pathToInputDir + "/Txt"
		ResetOutputDir(pathToOutputDir)
		WriteToFiles("txt", pathToInputDir, pathToOutputDir)

	elif outputType == "-x":		# Xml generation chosen
		pathToOutputDir = pathToInputDir + "/Xml"
		ResetOutputDir(pathToOutputDir)
		WriteToFiles("xml", pathToInputDir, pathToOutputDir)