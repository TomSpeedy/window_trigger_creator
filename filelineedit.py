# This Python file uses the following encoding: utf-8
from PySide6.QtWidgets import QLineEdit

class FileLineEdit(QLineEdit):
    def __init__(self, parent):
        super().__init__(parent)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        mimeData = event.mimeData()
        if mimeData.hasUrls():
            droppedFile = mimeData.urls()[0].toLocalFile()
            self.setText(droppedFile)
            event.acceptProposedAction()



