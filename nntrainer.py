# This Python file uses the following encoding: utf-8
#import tensorflow as tf
#import numpy as np
from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import QThread
import os
import json
from pprint import pprint
import tensorflow as tf
import numpy as np
import math
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from matplotlib import pyplot as plt
#import tensorflow_addons as tfa

class NnTrainer():
    class Args():
        pass

    def __init__(self, mainWindow):
        self.args = NnTrainer.Args()
        self.setDefaultHyperparams()
        self.mainWindow = mainWindow
        self.logger = mainWindow.ui.nnConsoleTextBrowser
        pass

    def log(self,text):
        self.logger.append(text)

    def setDefaultHyperparams(self):
        self.args.learningRate = 0.001
        self.args.hiddenLayerSizes = [20,20]
        self.args.epochCount = 30
        self.args.learningRateDecay = None#{"name" : "cosine", "initialLearnRate" : 0.001, "decayRate" : 0.96}
        self.args.optimizer = "adam"
        self.args.dataSplit = {"training" : 0.7, "validation" : 0.15, "test" : 0.15}
        self.args.dropout = 0
        self.args.batchSize = 5
        self.args.untriggerWeight = 1
        self.args.triggerWeight = 100


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
        pprint(vars(self.args))

    def trainTestValSplitEqual(self, dataset):
        pTrain = self.args.dataSplit["training"]
        pTest = self.args.dataSplit["test"]
        pVal = self.args.dataSplit["validation"]
        return dataset.trainTestValSplitEqual(pTrain, pTest, pVal)

    def show_cm(self, y_true, y_pred, name):
        cm_display = ConfusionMatrixDisplay(confusion_matrix(y_true, y_pred), display_labels= ["no_trigger", "trigger"],)
        plt.rcParams['font.size'] = 16
        cm_display.plot()
        plt.title(name + " confusion matrix")
        plt.show()

    def train(self, dataset, triggerClasses, model = None):
        SHUFFLE_BUFFER_SIZE = 1024
        def extract_labels(example, label):
            return label
        def augment(example):
            noise = 0.0 * np.random.normal(np.zeros(stds.shape), stds, stds.shape)
            return example + noise;

        npData, npLabels, npClassSizes = dataset.toNumpy(triggerClasses)
        #npData = (npData - npData.mean(axis = 0))/np.nan_to_num(npData.std(axis = 0))

        (trainIndices, testIndices, valIndices) = self.trainTestValSplitEqual(dataset)
        means = npData[trainIndices, :].mean(axis = 0)
        stds = npData[trainIndices, :].std(axis = 0)
        EPSILON = 0.0000001
        stds[np.abs(stds) < EPSILON] = 1
        print(trainIndices.shape, testIndices.shape, valIndices.shape)
        print("MEANS")
        print(means)
        print(stds)
        train_sample_weights = np.ones(shape = len(trainIndices))
        train_sample_weights[train_sample_weights == 1] = self.args.triggerWeight
        train_sample_weights[train_sample_weights == 0] = self.args.untriggerWeight

        tf.random.set_seed(42)
        trainDataset = (self.ballance_dataset(tf.data.Dataset.from_tensor_slices(
            (npData[trainIndices, :], npLabels[trainIndices], train_sample_weights)))
            .map(lambda x,y,weight: (augment(x), y, weight))
            .shuffle(SHUFFLE_BUFFER_SIZE)
            .batch(self.args.batchSize, drop_remainder = True))
        testDataset = tf.data.Dataset.from_tensor_slices(
            (npData[testIndices, :], npLabels[testIndices])).shuffle(SHUFFLE_BUFFER_SIZE).batch(self.args.batchSize, drop_remainder = True)
        valDataset = tf.data.Dataset.from_tensor_slices(
        (npData[valIndices, :], npLabels[valIndices])).shuffle(SHUFFLE_BUFFER_SIZE).batch(self.args.batchSize, drop_remainder = True)
        #TODO create model based on args

        #if model == None:
        model = Model(self.args, trainDataset, means, stds)



        model.compile(optimizer = model.optimizer,
            loss = tf.keras.losses.BinaryFocalCrossentropy(),#tf.keras.losses.BinaryCrossentropy(),
            metrics = [tf.keras.metrics.BinaryAccuracy(), tf.keras.metrics.Precision(), tf.keras.metrics.Recall()])
        model.fit(trainDataset, validation_data = valDataset, epochs= self.args.epochCount,
            callbacks = [PrintLossCallback(self)]) #class_weight = {0 : self.args.untriggerWeight, 1 : self.args.triggerWeight})
        model._set_inputs(npData)
        positive_offset = 0
        test_y = (model.predict(npData[testIndices]) + positive_offset).round().ravel()
        train_y = (model.predict(npData[trainIndices])+ positive_offset).round().ravel()
        val_y = (model.predict(npData[valIndices])+ positive_offset).round().ravel()


        self.show_cm(npLabels[trainIndices], train_y, "Training")
        self.show_cm(npLabels[testIndices], test_y, "Test")
        self.show_cm(npLabels[valIndices], val_y, "Validation")
        #print("RESULT DTYPE ", result.dtype)
        return model

    def ballance_dataset(self, dataset):
        ds_untrigger = dataset.filter(lambda x, y, weight: tf.math.equal(y,0))
        ds_trigger = dataset.filter(lambda x, y, weight: tf.math.equal(y,1))
        n_0 = tf.data.experimental.cardinality(ds_untrigger)
        n_1 = tf.data.experimental.cardinality(ds_trigger)
        if(n_0 < n_1):
            ds_untrigger = ds_untrigger.repeat(int(np.ceil(n_1/n_0))).take(n_1)
        else:
            ds_trigger = ds_trigger.repeat(int(np.ceil(n_0/n_1))).take(n_0)
        return ds_untrigger.concatenate(ds_trigger)



class PrintLossCallback(tf.keras.callbacks.Callback):
    def __init__(self, logger):
        super(PrintLossCallback, self).__init__()
        self.logger = logger
    def on_train_batch_end(self, batch, logs = None):
        self.logger.log(f"{logs}")

    def on_epoch_end(self, epoch, logs=None):
        #valLoss=logs.get('val_loss')  # get the validation loss for this epoch
        self.logger.log(f"Validation after epoch {epoch}: {logs}")


class ZScoreNormalizationLayer(tf.keras.layers.Layer):
    def __init__(self, mean, std):
        super(ZScoreNormalizationLayer, self).__init__()
        self.mean = mean
        self.std = std
    def __call__(self, inputs):
        return (inputs - self.mean)/self.std
    def get_config(self):
        config = super(ZScoreNormalizationLayer, self).get_config()
        config["mean"] = self.mean
        config["std"] = self.std
        return config
    @classmethod
    def from_config(cls, config):
        return cls(mean = config["mean"], std = config["std"])

class Model(tf.keras.Model):
    def __init__(self, args, trainDataset, mean, std):
        super().__init__()
        self.hiddenLayers = [ZScoreNormalizationLayer(mean, std)]
        for hiddenLayerSize in args.hiddenLayerSizes:
            self.hiddenLayers.append(tf.keras.layers.Dropout(args.dropout))
            self.hiddenLayers.append(tf.keras.layers.Dense(hiddenLayerSize, activation = "relu"))
        self.classificationHead = tf.keras.layers.Dense(1, activation = "sigmoid")
        learningSchedule = args.learningRate

        if args.learningRateDecay != None and args.learningRateDecay != "None":
            if not hasattr(args.learningRateDecay, "decaySteps"):
                decayStepCount = tf.math.ceil(tf.data.experimental.cardinality(trainDataset).numpy() * args.epochCount / args.batchSize)
            else:
                decayStepCount = args.learningRateDecay.decaySteps

            learningSchedules = {
                "exponential":
                    tf.keras.optimizers.schedules.ExponentialDecay(
                    args.learningRateDecay.initialLearnRate,
                    decayStepCount,
                    args.learningRateDecay.decayRate),
                "cosine":
                    tf.keras.optimizers.schedules.CosineDecay(
                    args.learningRateDecay.initialLearnRate,
                    decayStepCount
                    )
                }
            if "name" in learningSchedules.keys():
                learningSchedule = learningSchedules[args.learningRateDecay.name]
            else:
                print("Learning rate was not identified")

        optimizers = {
            "adam":
                tf.keras.optimizers.Adam(learning_rate = learningSchedule)
            }
        if args.optimizer in optimizers.keys():
            self.optimizer = optimizers[args.optimizer]
        else:
            self.optimizer = tf.keras.optimizers.Adam(learning_rate = learningSchedule)

    @tf.function
    def __call__(self, inputs, training = True):
        #TODO create model
        output = inputs
        for hiddenLayer in self.hiddenLayers:
            output = hiddenLayer(output)
        return self.classificationHead(output)


    @tf.function
    def call(self, inputs, training = True):
        #TODO create model
        output = inputs
        for hiddenLayer in self.hiddenLayers:
            output = hiddenLayer(output)
        return self.classificationHead(output)




