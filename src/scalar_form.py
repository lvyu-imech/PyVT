# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'variable_form.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal

class popup_widget_4SC(QDialog):

    scalar_signal = pyqtSignal()
    
    varlist = []
    formula = ''
    new_var_name = ''

    def __init__(self, parent):
        super().__init__()
        self.setupUi(self, parent)

    def setupUi(self, Dialog, parent):
        Dialog.setObjectName("Dialog")
        Dialog.resize(386, 234)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(20, 190, 351, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.toolButton = QtWidgets.QToolButton(Dialog)
        self.toolButton.setGeometry(QtCore.QRect(290, 33, 31, 31))
        self.toolButton.setObjectName("toolButton")
        self.toolButton.clicked.connect(self.add_scalar2formula)
        self.toolButton.setIcon(QtGui.QIcon('./icons/add_stuff.png'))

        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 90, 61, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(30, 140, 101, 21))
        self.label_2.setObjectName("label_2")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(91, 91, 261, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(127, 140, 151, 21))
        self.lineEdit_2.setObjectName("lineEdit_2")
        
        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(90, 38, 181, 26))
        self.comboBox.setObjectName("comboBox")

        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(30, 40, 61, 21))
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(287, 136, 71, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.add_scalar_variable)  
        self.scalar_signal.connect(parent.scalar_signal.emit)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.toolButton.setText(_translate("Dialog", "+"))
        self.label.setText(_translate("Dialog", "Formula:"))
        self.label_2.setText(_translate("Dialog", "Enter a name:"))
        self.label_3.setText(_translate("Dialog", "Variable:"))
        self.pushButton.setText(_translate("Dialog", "Add"))

    def reinitialize(self):
        self.comboBox.clear()
        for item in self.varlist:
            self.comboBox.addItem(item)
        self.lineEdit_2.clear()
        self.lineEdit.clear()

    def add_scalar2formula(self):
        
        index = self.comboBox.currentIndex()
        name  = 'scalar_' + str(index+1)
        self.lineEdit.setText(self.lineEdit.text() + name) 

    def add_scalar_variable(self):
        self.new_var_name = self.lineEdit_2.text()
        self.comboBox.addItem(self.new_var_name)
        self.varlist.append(self.new_var_name)
        self.formula = self.lineEdit.text()

        self.scalar_signal.emit() 
