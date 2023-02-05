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

    # emptyMap = generateEmptyMap(fieldSize, windowsWidth, windowsHeight)
    # emptyMapEscape = mazeEscape(fieldSize, windowsWidth, windowsHeight, textAreaHeight, emptyMap)
    # randomMapEscape = mazeEscape(fieldSize, windowsWidth, windowsHeight, textAreaHeight)

    # qTableEmptyMap = qTrain(emptyMapEscape, 20000)
    # qTableRandomMap = qTrain(randomMapEscape, 25000)

    # packageEmptyMap = {"windowsData":(fieldSize, windowsWidth, windowsHeight), "map":(emptyMapEscape.environment.getMap()), "qTable":qTableEmptyMap}
    # packageRandomMap = {"windowsData":(fieldSize, windowsWidth, windowsHeight), "map":(randomMapEscape.environment.getMap()), "qTable":qTableRandomMap}


    # saveToFile(pretrainedPath, "emptyMapPreTrained", packageEmptyMap)
    # saveToFile(pretrainedPath, "randomMapPreTrained0", packageRandomMap)

    pretrainedPath = pretrainDataDirectory()
    fileDirectoryEmptyMap = pretrainedPath + "/emptyMapPreTrained.pkl"
    fileDirectoryRandomMap = pretrainedPath + "/randomMapPreTrained0.pkl"

    with open(fileDirectoryEmptyMap, "rb") as f:
        pretrainedEmptyMap = pkl.load(f)

    with open(fileDirectoryRandomMap, "rb") as f:
        pretrainedRandomMap0 = pkl.load(f)

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

def pretrainDataDirectory():
    qFolder = "QTables"
    pretrainedFolder = "pretrainedQTables"
    currentPath = os.path.abspath(os.path.dirname(__file__))
    parentPath = os.path.normpath(os.path.join(currentPath, qFolder))
    pretrainedPath = os.path.normpath(os.path.join(parentPath, pretrainedFolder))
    return pretrainedPath

if __name__ == "__main__":
    main()
