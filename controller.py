# This Python file uses the following encoding: utf-8
from PySide6.QtWidgets import QGridLayout, QLabel, QLineEdit, QCheckBox, QPushButton, QFileDialog
from PySide6.QtGui import QDoubleValidator
from PySide6.QtCore import Qt, QThread

from wfreader import WfReader
from datamodel import DataModel
import os
from nntrainer import NnTrainer
from lvqtrainer import LvqTrainer
from svmtrainer import SvmTrainer
from onesvmtrainer import OneSvmTrainer
from skl2onnx import convert_sklearn, to_onnx
from skl2onnx.common.data_types import FloatTensorType
from lvq_converter import lvqModelConverter, lvqModelShape
from skl2onnx import update_registered_converter
from skl2onnx.algebra.onnx_ops import OnnxMatMul, OnnxSub
from onnx.defs import onnx_opset_version
import sklearn_lvq
import subprocess

class Controller:
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow
        self.reader = WfReader()
        self.nnTrainer = NnTrainer(mainWindow)
        self.lvqTrainer = LvqTrainer(mainWindow)
        self.svmTrainer = SvmTrainer(mainWindow)
        self.oneSvmTrainer = OneSvmTrainer(mainWindow)
        mainWindow.ui.nnStartTrainingButton.clicked.connect(self.nnStartTraining)
        mainWindow.ui.lvqStartTrainingButton.clicked.connect(self.lvqStartTraining)
        mainWindow.ui.svmStartTrainingButton.clicked.connect(self.svmStartTraining)
        mainWindow.ui.oneSvmStartTrainingButton.clicked.connect(self.oneSvmStartTraining)

    def saveManualTriggerClicked(self):
        EMPTY_FIELD_STR = ""
        ANY_VALUE_STR = "*"
        START_INTERVAL_STR = "["
        END_INTERVAL_STR = "]"
        VALUE_SEPARATOR_STR = " "
        BOUND_SEPARATOR_STR = ":"
        VECTOR_SEPARATOR_STR = "\n"
        MANUAL_SUFFIX = ".ift"
        saveFile = QFileDialog.getSaveFileName(parent = self.mainWindow, caption = "Save as/Append to", filter = "Interval features trigger (*.ift)")[0]
        if saveFile == EMPTY_FIELD_STR:
            return
        if not saveFile.endswith(MANUAL_SUFFIX):
            saveFile += MANUAL_SUFFIX
        with open(saveFile, "a") as outputStream:

            if not os.path.isfile(saveFile) or os.stat(saveFile).st_size == 0:
                for scalarAtribute in self.dataModel.scalarAttributes():
                    outputStream.write(scalarAtribute)
                    outputStream.write(VALUE_SEPARATOR_STR)
                outputStream.write(VECTOR_SEPARATOR_STR)
            groupBox = self.mainWindow.ui.manualAttributeGroupBox
            for index, (lowerBoundEdit, upperBoundEdit) in enumerate(zip(groupBox.fromEdits, groupBox.toEdits)):
                if index != 0:
                    outputStream.write(VALUE_SEPARATOR_STR);
                outputStream.write(START_INTERVAL_STR)
                if(lowerBoundEdit.text() == EMPTY_FIELD_STR):
                    outputStream.write(ANY_VALUE_STR)
                else:
                    outputStream.write(lowerBoundEdit.text())
                outputStream.write(BOUND_SEPARATOR_STR)
                if(upperBoundEdit.text() == EMPTY_FIELD_STR):
                    outputStream.write(ANY_VALUE_STR)
                else:
                    outputStream.write(upperBoundEdit.text())
                outputStream.write(END_INTERVAL_STR)
            outputStream.write(VECTOR_SEPARATOR_STR)
        outputStream.close()

    def saveNnTriggerClicked(self):
        NN_TRIGGER_SUFFIX = ".nnt"
        SAVE_TF_MODEL_NAME = "./temp/tfModel"
        if self.nnModel == None:
            self.mainWindow.showMessage("Model cannot be saved because no model was trained")
            return
        saveFileName = self.mainWindow.saveAsClicked()
        if(saveFileName == ""):
            self.mainWindow.showMessage("Model was not saved because no save destination was not chosen")
            return
        if(not saveFileName.endswith(NN_TRIGGER_SUFFIX)):
            saveFileName += NN_TRIGGER_SUFFIX
        print(self.nnModel)
        self.nnModel.save(SAVE_TF_MODEL_NAME)

        convertCmd = ["python3", "-m" "tf2onnx.convert", "--saved-model", SAVE_TF_MODEL_NAME, "--output", saveFileName]
        subprocess.run(convertCmd)

    def saveLvqTriggerClicked(self):
        LVQ_TRIGGER_SUFFIX = ".lvqt"
        SAVE_LVQ_MODEL_NAME = "./temp/lvqModel"
        if not hasattr(self, "lvqModel"):
            self.mainWindow.showMessage("Model cannot be saved because no model was trained")
            return
        saveFileName = self.mainWindow.saveAsClicked()
        if(saveFileName == ""):
            self.mainWindow.showMessage("Model was not saved because no save destination was not chosen")
            return
        if(not saveFileName.endswith(LVQ_TRIGGER_SUFFIX)):
            saveFileName += LVQ_TRIGGER_SUFFIX
        print(self.dataModel.shape)
        initial_type = [("input", FloatTensorType([None, 26]))]
        lvq_onnx = convert_sklearn(self.lvqModel, initial_types=initial_type)
        with open(saveFileName, "wb") as file:
            file.write(lvq_onnx.SerializeToString())
        #convertCmd = ["python3", "-m" "tf2onnx.convert", "--saved-model", SAVE_TF_MODEL_NAME, "--output", saveFileName]
        #subprocess.run(convertCmd)

    def saveSvmTriggerClicked(self):
        SVM_TRIGGER_SUFFIX = ".svmt"
        if not hasattr(self, "svmModel"):
            self.mainWindow.showMessage("Model cannot be saved because no model was trained")
            return
        saveFileName = self.mainWindow.saveAsClicked()
        if(saveFileName == ""):
            self.mainWindow.showMessage("Model was not saved because no save destination was not chosen")
            return
        if(not saveFileName.endswith(SVM_TRIGGER_SUFFIX)):
            saveFileName += SVM_TRIGGER_SUFFIX
        print(self.dataModel.shape)
        initial_type = [("input", FloatTensorType([None, 26]))]
        allClassesList = self.mainWindow.ui.nnClassListWidget
        triggerClasses = [allClassesList.item(itemIndex).text() for itemIndex in range(allClassesList.count())
            if allClassesList.item(itemIndex).checkState() == Qt.Checked]
        npData, npLabels, npClassSizes = self.dataModel.toNumpy(triggerClasses)
        npData = (npData - npData.mean(axis = 0))/npData.std(axis = 0)
        svm_onnx = convert_sklearn(self.svmModel, initial_types = initial_type, verbose = 2, target_opset={'':18, 'ai.onnx.ml':2} )
        with open(saveFileName, "wb") as file:
            file.write(svm_onnx.SerializeToString())

    def saveOneSvmTriggerClicked(self):
        ONE_SVM_TRIGGER_SUFFIX = ".osvmt"
        if not hasattr(self, "oneSvmModel"):
            self.mainWindow.showMessage("Model cannot be saved because no model was trained")
            return
        saveFileName = self.mainWindow.saveAsClicked()
        if(saveFileName == ""):
            self.mainWindow.showMessage("Model was not saved because no save destination was not chosen")
            return
        if(not saveFileName.endswith(ONE_SVM_TRIGGER_SUFFIX)):
            saveFileName += ONE_SVM_TRIGGER_SUFFIX
        print(self.dataModel.shape)
        initial_type = [("input", FloatTensorType([None, 26]))]
        oneSvmOnnx = convert_sklearn(self.oneSvmModel, initial_types = initial_type, verbose = 2, target_opset={'':18, 'ai.onnx.ml':2} )
        with open(saveFileName, "wb") as file:
            file.write(oneSvmOnnx.SerializeToString())

    def clearManualLayout(self, layout):
        if layout == None:
            return
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)


    def loadManualUi(self):
        groupBox = self.mainWindow.ui.manualAttributeGroupBox
        groupBox.fromEdits = []
        groupBox.toEdits = []
        self.clearManualLayout(self.mainWindow.ui.manualAttributeGroupBox.layout())
        if(self.mainWindow.ui.manualAttributeGroupBox.layout() == None):
            layout = QGridLayout(self.mainWindow.ui.manualAttributeGroupBox)
        else:
            layout = self.mainWindow.ui.manualAttributeGroupBox.layout()
        doubleValidator = QDoubleValidator()
        for attributeIndex, scalarAttribute in enumerate(self.dataModel.scalarAttributes()):
            layout.addWidget(QLabel(scalarAttribute, groupBox), attributeIndex, 0)
            layout.addWidget(QLabel("from", groupBox), attributeIndex, 1)
            fromLineEdit = QLineEdit(groupBox)
            fromLineEdit.setValidator(doubleValidator)
            groupBox.fromEdits.append(fromLineEdit)
            layout.addWidget(fromLineEdit, attributeIndex, 2)
            layout.addWidget(QLabel("to", groupBox), attributeIndex, 3)
            toLineEdit = QLineEdit(groupBox)
            toLineEdit.setValidator(doubleValidator)
            groupBox.toEdits.append(toLineEdit)
            layout.addWidget(toLineEdit, attributeIndex, 4)

        scalarCount = len(self.dataModel.scalarAttributes())
        groupBox.saveTriggerButton = QPushButton("Save trigger", groupBox)
        layout.addWidget(groupBox.saveTriggerButton, scalarCount, 0)
        groupBox.saveTriggerButton.clicked.connect(self.saveManualTriggerClicked)

        self.mainWindow.ui.manualAttributeGroupBox.setLayout(layout)

    def loadNnUi(self):
        ui = self.mainWindow.ui
        ui.nnClassListWidget.clear()
        for windowClass in self.dataModel.classes():
            ui.nnClassListWidget.addItem(windowClass)

        for classItemIndex in range(ui.nnClassListWidget.count()):
            classItem = ui.nnClassListWidget.item(classItemIndex)
            classItem.setFlags(classItem.flags() | Qt.ItemIsUserCheckable)
            classItem.setCheckState(Qt.Unchecked)

    def loadSvmUi(self):
        ui = self.mainWindow.ui
        ui.svmClassListWidget.clear()
        for windowClass in self.dataModel.classes():
            ui.svmClassListWidget.addItem(windowClass)

        for classItemIndex in range(ui.svmClassListWidget.count()):
            classItem = ui.svmClassListWidget.item(classItemIndex)
            classItem.setFlags(classItem.flags() | Qt.ItemIsUserCheckable)
            classItem.setCheckState(Qt.Unchecked)

    def loadOneSvmUi(self):
        ui = self.mainWindow.ui
        ui.oneSvmClassListWidget.clear()
        for windowClass in self.dataModel.classes():
            ui.oneSvmClassListWidget.addItem(windowClass)

        for classItemIndex in range(ui.svmClassListWidget.count()):
            classItem = ui.svmClassListWidget.item(classItemIndex)
            classItem.setFlags(classItem.flags() | Qt.ItemIsUserCheckable)
            classItem.setCheckState(Qt.Unchecked)

    def loadLvqUi(self):
        ui = self.mainWindow.ui
        ui.lvqClassListWidget.clear()
        for windowClass in self.dataModel.classes():
            ui.lvqClassListWidget.addItem(windowClass)

        for classItemIndex in range(ui.lvqClassListWidget.count()):
            classItem = ui.lvqClassListWidget.item(classItemIndex)
            classItem.setFlags(classItem.flags() | Qt.ItemIsUserCheckable)
            classItem.setCheckState(Qt.Unchecked)





    def loadInputClicked(self):

        self.dataModel = DataModel(self.reader, self.mainWindow.ui.inputFileLineEdit.text())

        self.loadManualUi()
        self.loadNnUi()
        self.loadLvqUi()
        self.loadSvmUi()
        self.loadOneSvmUi()
        self.mainWindow.ui.triggerTypeTabs.setVisible(True);

    def nnStartTraining(self):
        self.nnTrainer.loadHyperparams(self.mainWindow.ui.nnHyperparamLineEdit.text())
        allClassesList = self.mainWindow.ui.nnClassListWidget
        selectedClassesStr = [allClassesList.item(itemIndex).text() for itemIndex in range(allClassesList.count())
            if allClassesList.item(itemIndex).checkState() == Qt.Checked]
        #thread = QThread()
        #self.nnTrainer.moveToThread(thread)
        #thread.started.connect(lambda : self.nnTrainer.train(self.dataModel, selectedClassesStr))

        #thread = Thread(target = self.nnTrainer.train, args = (self.dataModel, selectedClassesStr))
        #thread.start()
        self.nnModel = self.nnTrainer.train(self.dataModel, selectedClassesStr)

    def lvqStartTraining(self):
        self.lvqTrainer.loadHyperparams(self.mainWindow.ui.lvqHyperparamLineEdit.text())
        allClassesList = self.mainWindow.ui.lvqClassListWidget
        selectedClassesStr = [allClassesList.item(itemIndex).text() for itemIndex in range(allClassesList.count())
            if allClassesList.item(itemIndex).checkState() == Qt.Checked]
        self.lvqModel = self.lvqTrainer.train(self.dataModel, selectedClassesStr)

    def svmStartTraining(self):
        self.svmTrainer.loadHyperparams(self.mainWindow.ui.svmHyperparamLineEdit.text())
        allClassesList = self.mainWindow.ui.svmClassListWidget
        selectedClassesStr = [allClassesList.item(itemIndex).text() for itemIndex in range(allClassesList.count())
            if allClassesList.item(itemIndex).checkState() == Qt.Checked]
        self.svmModel = self.svmTrainer.train(self.dataModel, selectedClassesStr)

    def oneSvmStartTraining(self):
        self.oneSvmTrainer.loadHyperparams(self.mainWindow.ui.oneSvmHyperparamLineEdit.text())
        allClassesList = self.mainWindow.ui.oneSvmClassListWidget
        selectedClassesStr = [allClassesList.item(itemIndex).text() for itemIndex in range(allClassesList.count())]
        self.oneSvmModel = self.oneSvmTrainer.train(self.dataModel, selectedClassesStr)
        print("HERE")

