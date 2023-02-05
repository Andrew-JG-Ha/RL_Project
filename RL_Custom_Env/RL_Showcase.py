from Q_learning import qTrain
from mazeEscapeGame import mazeEscape, generateEmptyMap
import random
import time
import os
import pickle as pkl

def main():
    file_setup()

    fieldSize = 20
    windowsWidth = 1280
    windowsHeight = 720
    textAreaHeight = 80

    emptyMap = generateEmptyMap(fieldSize, windowsWidth, windowsHeight)
    emptyMapEscape = mazeEscape(fieldSize, windowsWidth, windowsHeight, textAreaHeight, emptyMap)
    randomMapEscape = mazeEscape(fieldSize, windowsWidth, windowsHeight, textAreaHeight)

    qTableEmptyMap = qTrain(emptyMapEscape, 20000)
    qTableRandomMap = qTrain(randomMapEscape, 20000)

def file_setup():
    """
    Instantiation of the required folders
    """
    qFolder = "QTables"
    pretrainedFolder = "pretrainedQTables"
    newTablesFolder = "newQTables"
    currentPath = os.path.abspath(os.path.dirname(__file__))
    parentPath = os.path.normpath(os.path.join(currentPath, qFolder))
    pretrainedPath = os.path.normpath(os.path.join(parentPath, pretrainedFolder))
    newTablesPath = os.path.normpath(os.path.join(parentPath, newTablesFolder))
    if (not os.path.exists(parentPath)):
        os.mkdir(parentPath)
        if (not os.path.exists(pretrainedPath)):
            os.mkdir(pretrainedPath)
        if (not os.path.exists(newTablesPath)):
            os.mkdir(newTablesPath)

def saveToFile(fileDirectory, filename, object):
    """
    Creates and saves the object to the given filename within the given fileDirectory
    """
    pickleFileName = fileDirectory + "/" + filename + '.pkl'
    with open(pickleFileName, 'wb') as f:
        pkl.dump(object, f)

if __name__ == "__main__":
    main()
