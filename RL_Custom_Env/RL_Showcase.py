from Q_learning import qTrain
from mazeEscapeGame import mazeEscape, generateEmptyMap
import random
import time
import os
import pickle as pkl
import numpy as np

def main():
    file_setup()
    pretrainedEmptyData = None
    pretrainedRandomData0 = None

    fieldSize = 15
    windowsWidth = 1280
    windowsHeight = 720
    textAreaHeight = 80

    emptyMap = generateEmptyMap(fieldSize, windowsWidth, windowsHeight)
    emptyMapEscape = mazeEscape(fieldSize, windowsWidth, windowsHeight, textAreaHeight, emptyMap)
    randomMapEscape = mazeEscape(fieldSize, windowsWidth, windowsHeight, textAreaHeight)

    qTableEmptyMap = qTrain(emptyMapEscape, 15000, True)
    qTableRandomMap = qTrain(randomMapEscape, 30000, True)

    emptyMapEscape.reset()
    randomMapEscape.reset()
    packageEmptyMap = {"windowsData":(fieldSize, windowsWidth, windowsHeight), "map":(emptyMapEscape.environment.getMap()), "qTable":qTableEmptyMap}
    packageRandomMap = {"windowsData":(fieldSize, windowsWidth, windowsHeight), "map":(randomMapEscape.environment.getMap()), "qTable":qTableRandomMap}

    pretrainedPath = pretrainDataDirectory()
    fileDirectoryEmptyMap = pretrainedPath + "/emptyMapPreTrained.pkl"
    fileDirectoryRandomMap = pretrainedPath + "/randomMapPreTrained0.pkl"

    saveToFile(pretrainedPath, "emptyMapPreTrained", packageEmptyMap)
    saveToFile(pretrainedPath, "randomMapPreTrained0", packageRandomMap)


    # with open(fileDirectoryEmptyMap, "rb") as f:
    #     pretrainedEmptyData = pkl.load(f)
    # with open(fileDirectoryRandomMap, "rb") as f:
    #     pretrainedRandomData0 = pkl.load(f)
    # eMapWindowsData = pretrainedEmptyData["windowsData"]
    # eMap = pretrainedEmptyData["map"]
    # eMapQTable = pretrainedEmptyData["qTable"]
    # rMapWindowsData = pretrainedRandomData0["windowsData"]
    # rMap = pretrainedRandomData0["map"]
    # rMapQTable = pretrainedRandomData0["qTable"]
    # pretrainedRandomMap = mazeEscape(rMapWindowsData[0], rMapWindowsData[1], rMapWindowsData[2], textAreaHeight, rMap)
    # pretrainedRandomMap.close()
    # pretrainedEmptyMap = mazeEscape(eMapWindowsData[0], eMapWindowsData[1], eMapWindowsData[2], textAreaHeight, eMap)

    # print("Pretrained Q-tables applied to their respective maps")
    # testingQTable(eMapQTable, pretrainedEmptyMap, "pretrainedEmptyQTable")


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

def testingQTable(qTable, environment:mazeEscape, qTableName):
    state = environment.reset()
    done = False
    score = 0
    while (not done):
        environment.render(qTableName)
        action = np.argmax(qTable[state])
        state, reward, done = environment.step(action)
        score += reward
    environment.close()


if __name__ == "__main__":
    main()
