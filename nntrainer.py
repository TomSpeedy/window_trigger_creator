# This Python file uses the following encoding: utf-8
#import tensorflow as tf
#import numpy as np
from PySide6.QtWidgets import QMessageBox
import os
import json
from pprint import pprint
class Args():
    pass
class NnTrainer:
    def __init__(self):
        self.args = Args()
        self.setDefaultHyperparams()
        pass

    def setDefaultHyperparams(self):
        self.args.learningRate = 0.001
        self.args.hiddenLayerSizes = [20, 20]
        self.args.epochCount = 5
        self.args.learningRateDecay = "None"
        self.args.optimizer = "Adam"
        self.args.dataSplit = {"training" : 0.8, "validation" : 0.1, "test" : 0.1}
        self.args.dropout = 0.5

    def loadHyperparams(self, paramFile):

        if not os.path.isfile(paramFile):
            messageBox = QMessageBox()
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
                messageBox = QMessageBox()
                messageBox.setText(f"Hyperparameter name {hyperparamName} is not valid for this model. Skipping.")
                messageBox.show()
        pprint(vars(self.args))



