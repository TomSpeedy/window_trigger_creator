# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication, QWidget, QFileDialog

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow
from controller import Controller


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.controller = Controller(self)
        self.ui.browseInputButton.clicked.connect(self.browseInputClicked)
        self.ui.nnBrowseHyperparamButton.clicked.connect(self.browseHyperparamClicked)
        self.ui.loadInputButton.clicked.connect(self.controller.loadInputClicked)
        self.ui.inputFileLineEdit.setText("/home/tomas/MFF/DT/build-window_processor-Desktop_Qt_6_4_2_GCC_64bit-Debug/output/test_b.wf")

    def browseInputClicked(self):
        self.browseClicked("Window features (*.wf)", self.ui.inputFileLineEdit)

    def browseHyperparamClicked(self):
        self.browseClicked("Json hyperparameters (*.json)", self.ui.nnHyperparamLineEdit)

    def browseClicked(self, filter, textBox):
        selectedFile = QFileDialog.getOpenFileName( parent = self, caption = "Open file", filter = filter)[0]
        if selectedFile != "":
            textBox.setText(selectedFile)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
