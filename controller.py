# This Python file uses the following encoding: utf-8
from PySide6.QtWidgets import QGridLayout, QLabel, QLineEdit, QCheckBox, QPushButton, QFileDialog
from PySide6.QtGui import QDoubleValidator
from PySide6.QtCore import Qt
from wfreader import WfReader
from datamodel import DataModel
import os
from nntrainer import NnTrainer
class Controller:
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow
        self.reader = WfReader()
        self.nnTrainer = NnTrainer()
        mainWindow.ui.nnStartTrainingButton.clicked.connect(self.nnStartTraining)

    def saveManualTriggerClicked(self):
        EMPTY_FIELD_STR = ""
        ANY_VALUE_STR = "*"
        START_INTERVAL_STR = "["
        END_INTERVAL_STR = "]"
        VALUE_SEPARATOR_STR = " "
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
            for lowerBoundEdit, upperBoundEdit in zip(groupBox.fromEdits, groupBox.toEdits):
                outputStream.write(START_INTERVAL_STR)
                if(lowerBoundEdit.text() == EMPTY_FIELD_STR):
                    outputStream.write(ANY_VALUE_STR)
                else:
                    outputStream.write(lowerBoundEdit.text())
                outputStream.write(VALUE_SEPARATOR_STR)
                if(upperBoundEdit.text() == EMPTY_FIELD_STR):
                    outputStream.write(ANY_VALUE_STR)
                else:
                    outputStream.write(upperBoundEdit.text())
                outputStream.write(END_INTERVAL_STR)
            outputStream.write(VECTOR_SEPARATOR_STR)
        outputStream.close()


    def loadManualUi(self):
        groupBox = self.mainWindow.ui.manualAttributeGroupBox
        groupBox.fromEdits = []
        groupBox.toEdits = []
        layout = QGridLayout(groupBox)
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
        for windowClass in self.dataModel.classes():
            ui.nnClassListWidget.addItem(windowClass)

        for classItemIndex in range(ui.nnClassListWidget.count()):
            classItem = ui.nnClassListWidget.item(classItemIndex)
            classItem.setFlags(classItem.flags() | Qt.ItemIsUserCheckable)
            classItem.setCheckState(Qt.Unchecked)


    def loadInputClicked(self):

        self.dataModel = DataModel(self.reader, self.mainWindow.ui.inputFileLineEdit.text())

        self.loadManualUi()
        self.loadNnUi()

    def nnStartTraining(self):
        self.nnTrainer.loadHyperparams(self.mainWindow.ui.nnHyperparamLineEdit.text())
