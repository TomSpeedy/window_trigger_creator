# This Python file uses the following encoding: utf-8
from pprint import pprint
import numpy as np
import math
class DataModel:
    IGNORE_FEATURE = "start_toa[ms]"
    def __init__(self, reader, fileName):
        self.reader = reader
        self.attributeNames, self.data = self.reader.readWfFile(fileName)

    def scalarAttributes(self):
        scalarAttributes = []
        vectorMarker = "[["
        for attributeName in self.attributeNames:
            if vectorMarker not in attributeName:
                scalarAttributes.append(attributeName)
        return scalarAttributes

    def classes(self):
        return self.data.keys()

    def flattenWindows(self):
        windows2d = []
        for windowClass in self.classes():
            for window in self.data[windowClass]:
                flattenedWindow = []
                for index, feature in enumerate(window):
                    if hasattr(feature, "__iter__"):
                        flattenedWindow.extend(feature)
                    else:
                        flattenedWindow.append(feature)
                windows2d.append(flattenedWindow)
        return windows2d


    def classSizes(self):
        windowCounts = []
        for classIndex, windowClass in enumerate(self.classes()):
            windowCount = len(self.data[windowClass])
            windowCounts.append(windowCount)
        return np.array(windowCounts)

    def toNumpy(self, triggerClasses):
        npLabels = np.array([], dtype = np.int64)
        npData = np.array([])
        self.data = self.data
        windowCounts = []
        for classIndex, windowClass in enumerate(self.classes()):
            windowCount = len(self.data[windowClass])
            if windowClass in triggerClasses:
                npLabels = np.concatenate([npLabels, np.repeat(1, windowCount)], axis = 0)
            else:
                npLabels = np.concatenate([npLabels, np.repeat(0, windowCount)], axis = 0)
            windowCounts.append(windowCount)
        npData = np.nan_to_num(np.array(self.flattenWindows(), dtype = np.float32))[:, 1:] #ignore the zero-th feature
        #print("****************contains nan ", np.any(np.isnan(npData)))
        self.shape = npData.shape
        #print("SHAPE", npData.shape)
        #print(npData[0,:])
        return npData, npLabels, np.array(windowCounts)

    def trainTestValSplitEqual(self, pTrain, pTest, pVal):
        assert(math.isclose(pTrain + pTest + pVal, 1.) and pTrain >= 0 and pTest >= 0 and pVal >= 0)
        #we need to compute offsets of each class to compute absolute indices of elements of each class
        classesSizes = self.classSizes()
        classSizesCum = classesSizes.cumsum()
        classOffsets = np.insert(classSizesCum, 0, 0)
        trainIndices = np.array([], dtype = np.int64)
        testIndices = np.array([], dtype = np.int64)
        valIndices = np.array([], dtype = np.int64)

        for classIndex, classSize in enumerate(classesSizes):
            shuffledIndices = np.arange(classSize, dtype = np.int64)
            np.random.shuffle(shuffledIndices)
            shuffledIndices += classOffsets[classIndex]
            trainIndices = np.append(trainIndices, shuffledIndices[:int(pTrain * classSize)])
            valIndices = np.append(valIndices, shuffledIndices[int(pTrain * classSize): int((pTrain + pVal) * classSize)])
            testIndices = np.append(testIndices, shuffledIndices[int((pTrain + pVal) * classSize) : ])

        return (trainIndices, testIndices, valIndices)
