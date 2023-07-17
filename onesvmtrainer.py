# This Python file uses the following encoding: utf-8
from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QMessageBox
import os
import json
from pprint import pprint
import tensorflow as tf
import numpy as np
import math
from sklearn.svm import SVC, OneClassSVM
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from skl2onnx import __max_supported_opset__

class OneSvmTrainer:
    class Args():
        pass

    def __init__(self, mainWindow):
        self.args = OneSvmTrainer.Args()
        self.setDefaultHyperparams()
        self.logger = mainWindow.ui.oneSvmConsoleTextBrowser

    def log(self,text):
        self.logger.append(text)

    def setDefaultHyperparams(self):
        self.args.display = True
        self.args.dataSplit = {"training" : 1, "test" : 0., "validation" : 0.}
        self.args.nu = 0.1
        self.args.kernel = "rbf"
        self.args.gamma = "auto"

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
        self.log("Starting training")
        npData, npLabels, npClassSizes = dataset.toNumpy(triggerClasses)

        (trainIndices, testIndices, valIndices) = self.trainTestValSplitEqual(dataset)
        model = make_pipeline(StandardScaler(), OneClassSVM(nu = 0.1))
        self.model = model.fit(npData[trainIndices])
        self.log("Model fitted")

        return model
