# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cutplane_form.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal

class popup_widget_4CP(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.setupUi(self, parent)

    cutplane_signal = pyqtSignal(int)
   
    def_type = 'x'
    x_factor = 0
    y_factor = 0
    z_factor = 0
    udf_org  = (0, 0, 0)
    udf_nml  = (1, 0, 0) 
    offset   = 0.0
    numcut   = 1

    def setupUi(self, Dialog, parent):
        Dialog.setObjectName("Dialog")
        Dialog.resize(347, 333)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(20, 297, 311, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.Apply)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setText("View")
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).setText("Close")
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Apply).setText("Import")

        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(27, 22, 81, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(27, 72, 81, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(27, 122, 81, 16))
        self.label_3.setObjectName("label_3")
        self.horizontalSlider = QtWidgets.QSlider(Dialog)
        self.horizontalSlider.setGeometry(QtCore.QRect(114, 18, 201, 22))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalSlider.valueChanged.connect(lambda val: self.slider1_action(val))

        self.horizontalSlider_2 = QtWidgets.QSlider(Dialog)
        self.horizontalSlider_2.setGeometry(QtCore.QRect(114, 70, 201, 22))
        self.horizontalSlider_2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_2.setObjectName("horizontalSlider_2")
        self.horizontalSlider_2.valueChanged.connect(lambda val: self.slider2_action(val))
        
        self.horizontalSlider_3 = QtWidgets.QSlider(Dialog)
        self.horizontalSlider_3.setGeometry(QtCore.QRect(114, 120, 201, 22))
        self.horizontalSlider_3.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_3.setObjectName("horizontalSlider_3")
        self.horizontalSlider_3.valueChanged.connect(lambda val: self.slider3_action(val))
        
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(180, 174, 111, 21))
        self.lineEdit.setObjectName("lineEdit")
        #self.lineEdit.textChanged.connect(self.add1_input)
        self.lineEdit.editingFinished.connect(self.add1_input)
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setGeometry(QtCore.QRect(-3, 147, 401, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(180, 213, 111, 21))
        self.lineEdit_2.setObjectName("lineEdit_2")
        #self.lineEdit_2.textChanged.connect(self.add2_input)
        self.lineEdit_2.editingFinished.connect(self.add2_input)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(60, 176, 81, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(60, 216, 101, 16))
        self.label_5.setObjectName("label_5")
        self.line_2 = QtWidgets.QFrame(Dialog)
        self.line_2.setGeometry(QtCore.QRect(-20, 240, 401, 20))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")


        self.checkBox = QtWidgets.QCheckBox(Dialog)
        self.checkBox.setGeometry(QtCore.QRect(20, 160, 31, 41))
        self.checkBox.setText("")
        self.checkBox.setObjectName("checkBox")
        self.checkBox.clicked.connect(self.set_type)
       
        self.spinBox = QtWidgets.QSpinBox(Dialog)
        self.spinBox.setGeometry(QtCore.QRect(86, 260, 48, 24))
        self.spinBox.setObjectName("spinBox")
        self.spinBox.setMinimum(1)
        self.spinBox.editingFinished.connect(self.cutplane_num_change)
        
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(10, 264, 81, 16))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(157, 264, 91, 16))
        self.label_7.setObjectName("label_7")
        self.lineEdit_3 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_3.setGeometry(QtCore.QRect(253, 261, 51, 21))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_3.setText('0')
        #self.lineEdit_3.textChanged.connect(self.cutplane_offset_change)
        self.lineEdit_3.editingFinished.connect(self.cutplane_offset_change)

        self.retranslateUi(Dialog)
        #self.buttonBox.accepted.connect(Dialog.accept)
       
        self.buttonBox.accepted.connect(self.click_view)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Apply).clicked.connect(self.click_confirm)
        self.cutplane_signal.connect(lambda val: parent.cutplane_signal.emit(val))

        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Define Cutplane"))
        self.label.setText(_translate("Dialog", "x-direction"))
        self.label_2.setText(_translate("Dialog", "y-direction"))
        self.label_3.setText(_translate("Dialog", "z-direction"))
        self.label_4.setText(_translate("Dialog", "define orgin:"))
        self.label_5.setText(_translate("Dialog", "define normal:"))
        self.label_6.setText(_translate("Dialog", "No. of cuts"))
        self.label_7.setText(_translate("Dialog", "Signed offset"))

    def slider1_action(self, value):
       
        self.x_factor = value
        self.def_type = 'x'
    
    def slider2_action(self, value):
       
        self.y_factor = value
        self.def_type = 'y'

    def slider3_action(self, value):
       
        self.z_factor = value
        self.def_type = 'z'

    def add1_input(self):
        lstr = self.lineEdit.text().encode('utf-8')
        lstr_split = [float(s) for s in lstr.split()] 
        
        self.udf_org = tuple(lstr_split[0:3])

    def add2_input(self):
        lstr = self.lineEdit_2.text().encode('utf-8')
        lstr_split = [float(s) for s in lstr.split()] 
        
        self.udf_nml = tuple(lstr_split[0:3]) 

    def cutplane_num_change(self):
        self.numcut = self.spinBox.value() 

    def cutplane_offset_change(self):
        lstr = self.lineEdit_3.text().encode('utf-8')
        self.offset = float(lstr) 
    
    def set_type(self):
        self.def_type = 'other'
      
    def click_view(self):
        if self.def_type == 'other':
            self.add1_input()
            self.add2_input()
       
        self.cutplane_num_change()
        self.cutplane_signal.emit(0)

    def click_confirm(self):
        if self.def_type == 'other':
            self.add1_input()
            self.add2_input()
        
        self.cutplane_num_change()
        self.cutplane_signal.emit(1)
