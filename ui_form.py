# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.2.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGroupBox, QLabel, QLineEdit,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QTabWidget, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1029, 709)
        self.triggerTypeTabs = QTabWidget(MainWindow)
        self.triggerTypeTabs.setObjectName(u"triggerTypeTabs")
        self.triggerTypeTabs.setGeometry(QRect(20, 110, 881, 651))
        self.manual_tab = QWidget()
        self.manual_tab.setObjectName(u"manual_tab")
        self.manualAttributeGroupBox = QGroupBox(self.manual_tab)
        self.manualAttributeGroupBox.setObjectName(u"manualAttributeGroupBox")
        self.manualAttributeGroupBox.setGeometry(QRect(10, 30, 801, 501))
        self.triggerTypeTabs.addTab(self.manual_tab, "")
        self.nn_tab = QWidget()
        self.nn_tab.setObjectName(u"nn_tab")
        self.nnHyperparamGroupBox = QGroupBox(self.nn_tab)
        self.nnHyperparamGroupBox.setObjectName(u"nnHyperparamGroupBox")
        self.nnHyperparamGroupBox.setGeometry(QRect(10, 10, 791, 71))
        self.nnHyperparamLineEdit = QLineEdit(self.nnHyperparamGroupBox)
        self.nnHyperparamLineEdit.setObjectName(u"nnHyperparamLineEdit")
        self.nnHyperparamLineEdit.setGeometry(QRect(20, 30, 361, 22))
        self.nnBrowseHyperparamButton = QPushButton(self.nnHyperparamGroupBox)
        self.nnBrowseHyperparamButton.setObjectName(u"nnBrowseHyperparamButton")
        self.nnBrowseHyperparamButton.setGeometry(QRect(420, 30, 80, 23))
        self.nnClassesGroupBox = QGroupBox(self.nn_tab)
        self.nnClassesGroupBox.setObjectName(u"nnClassesGroupBox")
        self.nnClassesGroupBox.setGeometry(QRect(10, 90, 611, 301))
        self.nnClassListWidget = QListWidget(self.nnClassesGroupBox)
        self.nnClassListWidget.setObjectName(u"nnClassListWidget")
        self.nnClassListWidget.setGeometry(QRect(10, 30, 281, 171))
        self.nnStartTrainingButton = QPushButton(self.nnClassesGroupBox)
        self.nnStartTrainingButton.setObjectName(u"nnStartTrainingButton")
        self.nnStartTrainingButton.setGeometry(QRect(20, 220, 151, 23))
        self.nnSaveModelButton = QPushButton(self.nnClassesGroupBox)
        self.nnSaveModelButton.setObjectName(u"nnSaveModelButton")
        self.nnSaveModelButton.setGeometry(QRect(20, 260, 161, 23))
        self.triggerTypeTabs.addTab(self.nn_tab, "")
        self.lvq_tab = QWidget()
        self.lvq_tab.setObjectName(u"lvq_tab")
        self.triggerTypeTabs.addTab(self.lvq_tab, "")
        self.browseInputButton = QPushButton(MainWindow)
        self.browseInputButton.setObjectName(u"browseInputButton")
        self.browseInputButton.setGeometry(QRect(480, 20, 80, 23))
        self.inputFileLineEdit = QLineEdit(MainWindow)
        self.inputFileLineEdit.setObjectName(u"inputFileLineEdit")
        self.inputFileLineEdit.setGeometry(QRect(140, 20, 321, 22))
        self.inputLabel = QLabel(MainWindow)
        self.inputLabel.setObjectName(u"inputLabel")
        self.inputLabel.setGeometry(QRect(30, 20, 121, 16))
        self.loadInputButton = QPushButton(MainWindow)
        self.loadInputButton.setObjectName(u"loadInputButton")
        self.loadInputButton.setGeometry(QRect(30, 60, 131, 31))

        self.retranslateUi(MainWindow)

        self.triggerTypeTabs.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.manualAttributeGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Feature Intervals", None))
        self.triggerTypeTabs.setTabText(self.triggerTypeTabs.indexOf(self.manual_tab), QCoreApplication.translate("MainWindow", u"Manual interval trigger", None))
        self.nnHyperparamGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Import hyperparameter file:", None))
        self.nnBrowseHyperparamButton.setText(QCoreApplication.translate("MainWindow", u"Browse...", None))
        self.nnClassesGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Select Classes For Trigger", None))
        self.nnStartTrainingButton.setText(QCoreApplication.translate("MainWindow", u"Start Training", None))
        self.nnSaveModelButton.setText(QCoreApplication.translate("MainWindow", u"Save Trained Model", None))
        self.triggerTypeTabs.setTabText(self.triggerTypeTabs.indexOf(self.nn_tab), QCoreApplication.translate("MainWindow", u"NN trigger", None))
        self.triggerTypeTabs.setTabText(self.triggerTypeTabs.indexOf(self.lvq_tab), QCoreApplication.translate("MainWindow", u"LVQ trigger", None))
        self.browseInputButton.setText(QCoreApplication.translate("MainWindow", u"Browse...", None))
        self.inputFileLineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"<existing \".wf\" file>", None))
        self.inputLabel.setText(QCoreApplication.translate("MainWindow", u"Select input file:", None))
        self.loadInputButton.setText(QCoreApplication.translate("MainWindow", u"Load selected file", None))
    # retranslateUi

