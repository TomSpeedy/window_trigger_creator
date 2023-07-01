# This Python file uses the following encoding: utf-8
from sklearn_lvq import GlvqModel
from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QMessageBox
import os
import json
from pprint import pprint
import tensorflow as tf
import numpy as np
import math

class LvqTrainer:
    class Args():
        pass

    def __init__(self, mainWindow):
        self.args = LvqTrainer.Args()
        self.setDefaultHyperparams()
        self.logger = mainWindow.ui.lvqConsoleTextBrowser


    def log(self,text):
        self.logger.append(text)

    def setDefaultHyperparams(self):
        self.args.display = True
        self.args.prototypesPerClass = 1
        self.args.dataSplit = {"training" : 0.8, "test" : 0.2, "validation" : 0.0}
        self.args.maxIter = 2500
        self.args.beta = 2

    def loadHyperparams(self, paramFile):
        if(paramFile == ""):
            return
        if not os.path.isfile(paramFile):
            messageBox = QMessageBox(self.mainWindow)
            messageBox.setText("Selected hyperparameter file does not exist")
            messageBox.show()
            return
        with open(paramFile, "r") as paramStream:
            params = paramStream.read()
        paramDict = json.loads(params)
        for hyperparamName, hyperparamValue in paramDict.items():
            if(hasattr(self.args, hyperparamName)):
                setattr(self.args, hyperparamName, hyperparamValue)
            else:
                messageBox = QMessageBox(self.mainWindow)
                messageBox.setText(f"Hyperparameter name {hyperparamName} is not valid for this model. Skipping.")
                messageBox.show()

    def trainTestValSplitEqual(self, dataset):
        pTrain = self.args.dataSplit["training"]
        pTest = self.args.dataSplit["test"]
        pVal = self.args.dataSplit["validation"]
        return dataset.trainTestValSplitEqual(pTrain, pTest, pVal)

    def train(self, dataset, triggerClasses, model = None):
        npData, npLabels, npClassSizes = dataset.toNumpy(triggerClasses)
        npData = (npData - npData.mean(axis = 0))/npData.std(axis = 0)
        (trainIndices, testIndices, valIndices) = self.trainTestValSplitEqual(dataset)
        if model == None:
            model = GlvqModel(display=self.args.display, prototypes_per_class= npClassSizes.shape[0])
        self.model = model.fit(npData[trainIndices], npLabels[trainIndices])
        self.log(f"Reached test accuracy {model.score(npData[testIndices], npLabels[testIndices])}")
        return model


