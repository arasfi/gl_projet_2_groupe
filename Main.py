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


def ConvertToTxt(pathToOutputDir):
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


def ConvertToXml:
	# Delete output dir if exists
	if os.path.exists(pathToXmlOutput):
		shutil.rmtree(pathToXmlOutput)

	# Make a new output dir
	os.mkdir(pathToXmlOutput)

	# Print all pdf files in <pathToDir>
	for fileName in os.listdir(pathToDir):
		if fileName.endswith(".pdf"):
			fileNameModified = fileName.replace(" ", "\ ")
			print(fileName)

			# Use pdftotext to extract the content of the pdf file to a temp.txt file
			XmlFileName = fileName.replace(".pdf", ".xml")
			os.system("pdftotext -raw " + pathToDir + "/" + fileNameModified + " " + pathToXmlOutput + "/temp.txt")

			# Get file name
			preamble = fileName

			# Get title and author(s)
			titre = ""
			auteur = ""
			counter = 0
			with open(pathToTxtOutput + "/temp.txt", "r") as file:
				for line in file:
					line = line.replace("\n", " ")
					line = line.replace("\r", " ")
					if counter < 2:		# Title
						titre += line
					else:				# Author
						auteur += line
					if ("Abstract" in line or "ABSTRACT" in line):
						break
					counter += 1

			# Get abstract
			abstract = ""
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
						abstract += line
					if ("Abstract" in line or "ABSTRACT" in line):
						isAbstract = True

			# Write the result to the file
			# TODO

	# Delete temp.txt
	os.remove(pathToXmlOutput + "/temp.txt")



if __name__ == "__main__":
	pathToDir = sys.argv[1]
	pathToTxtOutput = pathToDir + "/Txt"
	pathToXmlOutput = pathToDir + "/Xml"

	outputType = sys.argv[2]
	if outputType == "-t":			# Txt generation chosen
		ResetOutputDir(pathToTxtOutput)
		ConvertToTxt()

	else if outputType == "-x":		# Xml generation chosen
		ResetOutputDir(pathToXmlOutput)
		ConvertToXml()