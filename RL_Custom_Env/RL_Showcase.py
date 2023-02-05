from Q_learning import qTrain
from mazeEscapeGame import mazeEscape, generateEmptyMap
import random
import time
import os
import pickle as pkl
import numpy as np

def main():
    file_setup()
    pretrainedRandomData0 = None

    fieldSize = 15
    windowsWidth = 1280
    windowsHeight = 720
    textAreaHeight = 80

    pretrainedPath = pretrainDataDirectory()
    fileDirectoryRandomMap = pretrainedPath + "/randomMapPreTrained0.pkl"
    with open(fileDirectoryRandomMap, "rb") as f:
        pretrainedRandomData0 = pkl.load(f)
    rMapWindowsData = pretrainedRandomData0["windowsData"]
    rMap = pretrainedRandomData0["map"]
    rMapQTable = pretrainedRandomData0["qTable"]

    print("Pretrained Q-table applied to its map:")
    pretrainedRandomMap = mazeEscape(rMapWindowsData[0], rMapWindowsData[1], rMapWindowsData[2], textAreaHeight, rMap)
    testingQTable(rMapQTable, pretrainedRandomMap, "pretrainedRandomQTable")

    newMap1 = mazeEscape(fieldSize, windowsWidth, windowsHeight, textAreaHeight)
    testQTable = qTrain(newMap1, 30000, True)

    print("Training a Q-table on a random map with rendering:")
    newMap = mazeEscape(fieldSize, windowsWidth, windowsHeight, textAreaHeight)
    newQTable = qTrain(newMap, 30000, True)
    testingQTable(newQTable, newMap, "TrainedQTable")
    testingQTable(testQTable, newMap1, "Testing123")

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
        time.sleep(0.15)
        score += reward

if __name__ == "__main__":
    main()
