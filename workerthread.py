# This Python file uses the following encoding: utf-8
from PySide6.QtCore import QThread, Signal, Slot, QObject, QMetaObject, Qt


class WorkerThread(QThread):
    def __init__(self, func, *args):
        super().__init__()
        self.func = func
        self.args =  args
    def run(self):
        self.func(*self.args)

class Logger(QObject):
    def __init__(self, textbox, mainWindow):
        super().__init__()
        self.textbox = textbox
        self.mainWindow = mainWindow
        
    @Slot(str)
    def log(self,text):
        self.textbox.append(text)
        self.mainWindow.app.processEvents()
