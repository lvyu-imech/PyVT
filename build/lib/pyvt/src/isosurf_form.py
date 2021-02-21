# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'isosurf_form.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!

from .qrangeslider import QRangeSlider
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal

class popup_widget_4IS(QDialog):
    def __init__(self, parent, scalar_range):
        super().__init__()
        self.setupUi(self, parent, scalar_range)
    
    isosurf_signal = pyqtSignal(int)
    iso_value = 0
    numiso    = 1
    upperbound = 0.
    lowerbound = 0.
    mod_upperbound = 0.;
    mod_lowerbound = 0.; 

    def setupUi(self, Dialog, parent, scalar_range):
        Dialog.setObjectName("Define Iso-Surface")
        Dialog.resize(290, 189)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(60, 150, 201, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Apply|QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setText("View")
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).setText("Close")
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Apply).setText("Import")

        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 80, 131, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(110, 16, 60, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(190, 16, 60, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(100, 16, 60, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(257, 16, 31, 16))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(180, 16, 31, 16))
        self.label_6.setObjectName("label_6")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(160, 78, 61, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(18, 15, 81, 20))
        self.label_7.setObjectName("label_7")

        #self.horizontalSliderorizontalSlider = QtWidgets.QSlider(Dialog)
        #self.horizontalSlider.setGeometry(QtCore.QRect(19, 46, 231, 31))
        #self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        #self.horizontalSlider.setObjectName("horizontalSlider")
        self.range_slider = QRangeSlider(Dialog)
        self.range_slider.setBackgroundStyle("background-color:white;")
        self.range_slider.handle.setStyleSheet("background-color:white;")
        self.range_slider.setGeometry(QtCore.QRect(19, 46, 241, 23))

        self.spinBox = QtWidgets.QSpinBox(Dialog)
        self.spinBox.setGeometry(QtCore.QRect(158, 114, 51, 24))
        self.spinBox.setObjectName("spinBox")
        self.spinBox.setMinimum(1)
        self.spinBox.valueChanged.connect(self.isosurf_num_change)
        
        self.label_8 = QtWidgets.QLabel(Dialog)
        self.label_8.setGeometry(QtCore.QRect(20, 118, 131, 16))
        self.label_8.setObjectName("label_8")

        self.retranslateUi(Dialog)
        #self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.accepted.connect(self.click_view)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Apply).clicked.connect(self.click_confirm)
        self.isosurf_signal.connect(lambda val: parent.isosurf_signal.emit(val))

        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Define Iso-Surface"))
        self.label.setText(_translate("Dialog", "Enter a single value: "))
        self.label_2.setText(_translate("Dialog", '{:.1e}'.format(self.lowerbound)))
        self.label_3.setText(_translate("Dialog", '{:.1e}'.format(self.upperbound)))
        self.label_4.setText(_translate("Dialog", "("))
        self.label_5.setText(_translate("Dialog", ")"))
        self.label_6.setText(_translate("Dialog", ","))
        self.label_7.setText(_translate("Dialog", "scalar range:"))
        self.label_8.setText(_translate("Dialog", "Enter No. of values: "))

    def set_range(self):
        self.label_2.setText('{:.1e}'.format(self.lowerbound))
        self.label_3.setText('{:.1e}'.format(self.upperbound))

    def get_range(self): 
        mod_upperbound, mod_lowerbound = self.range_slider.getRange()
        
        adj_bounds = (self.lowerbound + float(mod_lowerbound)/99.0 * (self.upperbound - self.lowerbound), \
                      self.lowerbound + float(mod_upperbound)/99.0 * (self.upperbound - self.lowerbound), )

        return adj_bounds

    def isosurf_num_change(self): 
        self.numiso = self.spinBox.value()

    def set_iso_values(self):
 
        if self.numiso == 1: 
            lstr = self.lineEdit.text().encode('utf-8')
            lstr_split = [float(s) for s in lstr.split()]
            
            self.iso_value = [lstr_split[0]]
        else:
            lowerbound, upperbound = self.get_range()
            dist = (upperbound - lowerbound)/float(self.numiso+1)
            self.iso_value = []
            for i in range(self.numiso):
                self.iso_value.append(lowerbound + float(i)*dist)
    
    def click_view(self): 
       
        self.set_iso_values()
        self.isosurf_signal.emit(0)

    def click_confirm(self): 

        self.set_iso_values()
        self.isosurf_signal.emit(1)
    
