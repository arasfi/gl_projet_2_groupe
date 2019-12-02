#!/usr/bin/env python3

# import glob
# import io
import os
import shutil
import subprocess
import sys

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
		print(fileName)
		txtFileName = fileName.replace(".pdf", ".txt")
		subprocess.run(["pdftotext", "-raw", pathToDir + "/" + fileName, pathToTxtOutput + "/temp.txt"])
		shutil.copyfile(pathToTxtOutput + "/temp.txt", pathToTxtOutput + "/" + txtFileName)


# for i in range(1):
# 	file = io.open("Lin_2004_Rouge.txt", 'r', encoding='utf8')
# 	lineNumber = 0
# 	for line in file:
# 		print(line)
# 		lineNumber += 1
# 		if lineNumber > 10:
# 			break
# 	file.close()
