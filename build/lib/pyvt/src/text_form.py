# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'text_form.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal

class popup_widget_4TX(QDialog): 
    
    text_input = 'none'
    text_signal = _signal = pyqtSignal(int) 
    
    def __init__(self, parent):
        super().__init__()
        self.setupUi(self, parent)
    
    def setupUi(self, Dialog, parent):
        Dialog.setObjectName("Dialog")
        Dialog.resize(361, 211)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 170, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(Dialog)
        self.plainTextEdit.setGeometry(QtCore.QRect(20, 60, 321, 91))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 30, 81, 21))
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        
        #self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.accepted.connect(self.confirm)
        self.text_signal.connect(lambda val: parent.text_signal.emit(val))
        
        #self.buttonBox.rejected.connect(Dialog.reject)
        self.buttonBox.rejected.connect(self.cancel)
        
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Input text:"))

    def confirm(self):

        self.text_input = self.plainTextEdit.toPlainText()
        self.text_signal.emit(1)
        
        self.close()

    def cancel(self):

        self.text_signal.emit(0)
        
        self.close()
