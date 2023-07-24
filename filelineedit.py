# This Python file uses the following encoding: utf-8
from PySide6.QtWidgets import QLineEdit
#custom lineedit which can be used for drag and drop input
class FileLineEdit(QLineEdit):
    allowAllSuffixes = True
    def __init__(self, parent):
        super().__init__(parent)

    def setAcceptableSuffix(self, suffix):
        self.acceptableSuffix = suffix
        self.allowAllSuffixes = False
    def dragEnterEvent(self, event):
        mimeData = event.mimeData()
        if mimeData.hasUrls() and len(mimeData.urls()) == 1:
            if self.allowAllSuffixes or mimeData.urls()[0].toLocalFile().endswith(self.acceptableSuffix):
                event.acceptProposedAction()
            else:
                event.ignore()
        else:
            event.ignore()

    def dropEvent(self, event):
        mimeData = event.mimeData()
        if mimeData.hasUrls() and len(mimeData.urls()) == 1:
            if self.allowAllSuffixes or mimeData.urls()[0].toLocalFile().endswith(self.acceptableSuffix):
                self.setText(mimeData.urls()[0].toLocalFile())
                event.acceptProposedAction()
            else:
                event.ignore()
        else:
            event.ignore()



