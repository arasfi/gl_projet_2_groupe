import os


def listMenu(pathToInputDir):
    indexFiles = 1
    for fileName in os.listdir(pathToInputDir):
        if fileName.endswith(".pdf"):
            fileNameModified = fileName.replace(" ", "\ ")
            print(str(indexFiles) + " " + fileName)
            indexFiles = indexFiles + 1
    return indexFiles - 1

numberOfFiles = listMenu('Papers')


filesToConvertInput = input("Veuillez donner les fichiers à convertir (separés par des virgules) : ")

filesToConvertArray = filesToConvertInput.split(',')
for i in range(len(filesToConvertArray)) :
    filesToConvertArray[i] = int(filesToConvertArray[i]) - 1

listOfFilesToConvert = []
for i in range(numberOfFiles):
    if i not in filesToConvertArray:
        listOfFilesToConvert.append(False)
    else:
        listOfFilesToConvert.append(True)

print(listOfFilesToConvert)