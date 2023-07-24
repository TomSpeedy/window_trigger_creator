# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow
from controller import Controller

# Represents the View in MVC model
# handles GUI operation
class MainWindow(QWidget):
    def __init__(self, app, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.app = app
        self.controller = Controller(self, app)
        #connect all signals with slots
        self.ui.browseInputButton.clicked.connect(self.browseInputClicked)
        self.ui.nnBrowseHyperparamButton.clicked.connect(self.browseNnHyperparamClicked)
        self.ui.lvqBrowseHyperparamButton.clicked.connect(self.browseLvqHyperparamClicked)
        self.ui.svmBrowseHyperparamButton.clicked.connect(self.browseSvmHyperparamClicked)
        self.ui.oneSvmBrowseHyperparamButton.clicked.connect(self.browseOneSvmHyperparamClicked)
        self.ui.loadInputButton.clicked.connect(self.controller.loadInputClicked)
        self.ui.nnSaveModelButton.clicked.connect(self.controller.saveNnTriggerClicked)
        self.ui.lvqSaveModelButton.clicked.connect(self.controller.saveLvqTriggerClicked)
        self.ui.svmSaveModelButton.clicked.connect(self.controller.saveSvmTriggerClicked)
        self.ui.oneSvmSaveModelButton.clicked.connect(self.controller.saveOneSvmTriggerClicked)

        #self.ui.inputFileLineEdit.setText("/home/tomas/MFF/DT/window_processor/build/output/beam_data.wf")
        self.ui.inputFileLineEdit.setAcceptableSuffix(".wf")
        self.ui.svmHyperparamLineEdit.setAcceptableSuffix(".json")
        self.ui.lvqHyperparamLineEdit.setAcceptableSuffix(".json")
        self.ui.oneSvmHyperparamLineEdit.setAcceptableSuffix(".json")
        self.ui.nnHyperparamLineEdit.setAcceptableSuffix(".json")

        self.ui.triggerTypeTabs.setVisible(False);

    def browseInputClicked(self):
        self.browseClicked("Window features (*.wf)", self.ui.inputFileLineEdit)

    def browseNnHyperparamClicked(self):
        self.browseClicked("Json hyperparameters (*.json)", self.ui.nnHyperparamLineEdit)

    def browseLvqHyperparamClicked(self):
        self.browseClicked("Json hyperparameters (*.json)", self.ui.lvqHyperparamLineEdit)

    def browseSvmHyperparamClicked(self):
        self.browseClicked("Json hyperparameters (*.json)", self.ui.svmHyperparamLineEdit)

    def browseOneSvmHyperparamClicked(self):
        self.browseClicked("Json hyperparameters (*.json)", self.ui.oneSvmHyperparamLineEdit)


    def saveAsClicked(self):
        selectedFile = QFileDialog.getSaveFileName( parent = self, caption = "Save as...")[0]
        return selectedFile

    def browseClicked(self, filter, textBox):
        selectedFile = QFileDialog.getOpenFileName( parent = self, caption = "Open file", filter = filter)[0]
        if selectedFile != "":
            textBox.setText(selectedFile)

    def showMessage(self, text):
        messageBox = QMessageBox(self)
        messageBox.setText(text)
        messageBox.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow(app)
    widget.show()
    sys.exit(app.exec())
