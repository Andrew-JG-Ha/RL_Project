from Q_learning import qTrain
from mazeEscapeGame import mazeEscape
import os
import pickle as pkl
import numpy as np

def main():
    file_setup()
    pretrainedRandomData0 = None
    savePackage = False

    fieldSize = 14
    windowsWidth = 1280
    windowsHeight = 720
    textAreaHeight = 80

    pretrainedPath = pretrainDataDirectory()
    filesInPath = os.listdir(pretrainedPath)

    for file in filesInPath:
        fileDirectoryRandomMap = pretrainedPath + "/" + file
        with open(fileDirectoryRandomMap, "rb") as f:
            pretrainedRandomData0 = pkl.load(f)
        rMapWindowsData = pretrainedRandomData0["windowsData"]
        rMap = pretrainedRandomData0["map"]
        rMapQTable = pretrainedRandomData0["qTable"]
        print("Showcasing: {}'s Q-Table".format(file))
        pretrainedRandomMap = mazeEscape(rMapWindowsData[0], rMapWindowsData[1], rMapWindowsData[2], textAreaHeight, rMap)
        testingQTable(rMapQTable, pretrainedRandomMap, file)

    print("Training a Q-table with 150000 episodes on a random map with rendering on:")
    newMap = mazeEscape(fieldSize, windowsWidth, windowsHeight, textAreaHeight)
    newQTable = qTrain(newMap, 150000, True)
    testingQTable(newQTable, newMap, "TrainedQTable")

    if savePackage == True:
        package = createPackage(fieldSize, windowsWidth, windowsHeight, newMap, newQTable)
        saveToFile(pretrainedPath, "randomMapPreTrained" + str(len(filesInPath)), package)

def file_setup():
    """
    Instantiation of the required folders
    """
    qFolder = "QTables"
    pretrainedFolder = "pretrainedQTables"
    currentPath = os.path.abspath(os.path.dirname(__file__))
    parentPath = os.path.normpath(os.path.join(currentPath, qFolder))
    pretrainedPath = os.path.normpath(os.path.join(parentPath, pretrainedFolder))
    if (not os.path.exists(parentPath)):
        os.mkdir(parentPath)
        if (not os.path.exists(pretrainedPath)):
            os.mkdir(pretrainedPath)

def saveToFile(fileDirectory, filename, object):
    """
    Creates and saves the object to the given filename within the given fileDirectory
    """
    pickleFileName = fileDirectory + "/" + filename + '.pkl'
    with open(pickleFileName, 'wb') as f:
        pkl.dump(object, f)

def createPackage(fieldSize, windowsWidth, windowsHeight, mazeGameinstance:mazeEscape, qTable):
    mazeGameinstance.reset()
    package = {"windowsData":(fieldSize, windowsWidth, windowsHeight), "map":mazeGameinstance.environment.getMap(), "qTable":qTable}
    return package

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
        environment.updateClock()
        score += reward

if __name__ == "__main__":
    main()
