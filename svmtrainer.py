# This Python file uses the following encoding: utf-8
from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QMessageBox
import os
import json
from pprint import pprint
import tensorflow as tf
import numpy as np
import math
from sklearn.svm import SVC, NuSVC, OneClassSVM
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.metrics import f1_score
from skl2onnx import __max_supported_opset__
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from matplotlib import pyplot as plt
#trains the SVM model
class SvmTrainer:
    class Args():
        pass

    def __init__(self, mainWindow):
        self.args = SvmTrainer.Args()
        self.setDefaultHyperparams()
        self.logger = mainWindow.ui.svmConsoleTextBrowser


    def log(self,text):
        self.logger.append(text)

    def setDefaultHyperparams(self):
        self.args.display = True
        self.args.dataSplit = {"training" : 0.8, "test" : 0.2, "validation" : 0.}
        self.args.kernel = "rbf"
        self.args.gamma = "auto"

    #display the confusion matrix
    def show_cm(self, y_true, y_pred, name):
        cm_display = ConfusionMatrixDisplay(confusion_matrix(y_true, y_pred, normalize = "true"), display_labels= ["no_trigger", "trigger"])
        cm_display.plot()
        plt.title(name)
        plt.show()
    #set values of hyperparams from the file
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

    #preserve the class distribution for all datasets
    def trainTestValSplitEqual(self, dataset):
        pTrain = self.args.dataSplit["training"]
        pTest = self.args.dataSplit["test"]
        pVal = self.args.dataSplit["validation"]
        return dataset.trainTestValSplitEqual(pTrain, pTest, pVal)

    def train(self, dataset, triggerClasses, model = None):
        npData, npLabels, npClassSizes = dataset.toNumpy(triggerClasses)
        (trainIndices, testIndices, valIndices) = self.trainTestValSplitEqual(dataset)

        #use normalization by Standard deviation as the part of the model
        model =  make_pipeline(StandardScaler(), SVC(kernel = self.args.kernel, gamma = self.args.gamma))
        self.model = model.fit(npData[trainIndices], npLabels[trainIndices])
        train_y = model.predict(npData[trainIndices])
        test_y = model.predict(npData[testIndices])



        self.show_cm(npLabels[trainIndices], train_y, "Training")
        self.show_cm(npLabels[testIndices], test_y, "Test")
        #self.show_cm(npLabels[valIndices], val_y, "Validation")
        self.log(f"Fitting model: {self.model}")
        self.log(f"Train accuracy {model.score(npData[trainIndices], npLabels[trainIndices])}")
        self.log(f"Test accuracy {model.score(npData[testIndices], npLabels[testIndices])}")
        #self.log(f"Test F1 score{f1_score(npLabels[testIndices], y_pred)}")
        return model
