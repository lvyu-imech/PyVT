# -*- coding: utf-8 -*-

# Dialog implementation generated from reading ui file 'vector_form.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *

class popup_widget_4VC(QDialog):

    def __init__(self, varlist):
        super().__init__()
        self.setupUi(self, varlist)

    x_comp_var_name = ''
    y_comp_var_name = ''
    z_comp_var_name = ''
    vector_name = "none"
    active_vector = ''

    def setupUi(self, Dialog, varlist):
        Dialog.setObjectName("Dialog")
        Dialog.resize(294, 270)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(88, 230, 113, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.clicked_done)
        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(108, 25, 171, 31))
        self.comboBox.setObjectName("comboBox")
        self.comboBox_2 = QtWidgets.QComboBox(Dialog)
        self.comboBox_2.setGeometry(QtCore.QRect(108, 80, 171, 26))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_3 = QtWidgets.QComboBox(Dialog)
        self.comboBox_3.setGeometry(QtCore.QRect(108, 130, 171, 26))
        self.comboBox_3.setObjectName("comboBox_3")
        
        if varlist != []:
            for i in range(len(varlist)):
                self.comboBox.addItem(varlist[i])
                self.comboBox_2.addItem(varlist[i])
                self.comboBox_3.addItem(varlist[i])

        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(118, 180, 141, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(18, 31, 79, 16))
        self.label.setMaximumSize(QtCore.QSize(16777215, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(18, 83, 81, 16))
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(18, 133, 81, 16))
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(20, 185, 91, 16))
        self.label_4.setMaximumSize(QtCore.QSize(16777215, 16))
        self.label_4.setObjectName("label_4")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Define Vector"))
        self.pushButton.setText(_translate("Dialog", "Done"))
        self.label.setText(_translate("Dialog", "x component"))
        self.label_2.setText(_translate("Dialog", "y component"))
        self.label_3.setText(_translate("Dialog", "z component"))
        self.label_4.setText(_translate("Dialog", "vector name:"))

    def clicked_done(self):
        
        self.x_comp_var_name =  self.comboBox.currentText() 
        self.y_comp_var_name =  self.comboBox_2.currentText() 
        self.z_comp_var_name =  self.comboBox_3.currentText()
        
        self.vector_name = self.lineEdit.text() 
        
        self.close()
