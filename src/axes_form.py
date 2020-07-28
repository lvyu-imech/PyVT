# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'axes.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal

class popup_widget_4AX(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.setupUi(self, parent)
    
    axes_signal = pyqtSignal()

    factor_min = 1.0/4.0
    factor_max = 2.0

    show_x  = True
    show_y  = True
    show_z  = True

    title_x = 'X'
    title_y = 'Y'
    title_z = 'Z'

    bounds_x = (0, 1) 
    bounds_y = (0, 1)
    bounds_z = (0, 1) 
    
    noflabel_x = 4
    noflabel_y = 4
    noflabel_z = 4

    grid_on = False
    font_factor = 1
    label_factor = 1
    offset = 16
    
    exponent_x = 0
    exponent_y = 0
    exponent_z = 0
    
    def setupUi(self, Dialog, parent):
        Dialog.setObjectName("Dialog")
        Dialog.resize(455, 492)
        Dialog.setAutoFillBackground(True)
        self.checkBox_x = QtWidgets.QCheckBox(Dialog)
        self.checkBox_x.setGeometry(QtCore.QRect(140, 20, 31, 20))
        self.checkBox_x.setObjectName("checkBox_x")
        self.checkBox_y = QtWidgets.QCheckBox(Dialog)
        self.checkBox_y.setGeometry(QtCore.QRect(220, 20, 31, 20))
        self.checkBox_y.setObjectName("checkBox_y")
        self.checkBox_z = QtWidgets.QCheckBox(Dialog)
        self.checkBox_z.setGeometry(QtCore.QRect(300, 20, 31, 20))
        self.checkBox_z.setObjectName("checkBox_z")
        self.show_axes = QtWidgets.QLabel(Dialog)
        self.show_axes.setGeometry(QtCore.QRect(30, 20, 81, 16))
        self.show_axes.setObjectName("show_axes")
        self.title = QtWidgets.QLabel(Dialog)
        self.title.setGeometry(QtCore.QRect(33, 70, 51, 16))
        self.title.setObjectName("title")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(100, 70, 21, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(100, 110, 21, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(100, 150, 21, 16))
        self.label_5.setObjectName("label_5")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 200, 60, 16))
        self.label.setObjectName("label")
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setGeometry(QtCore.QRect(-30, 42, 501, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(Dialog)
        self.line_2.setGeometry(QtCore.QRect(-40, 180, 491, 20))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(40, 234, 21, 16))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(Dialog)
        self.label_8.setGeometry(QtCore.QRect(40, 274, 21, 16))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(Dialog)
        self.label_9.setGeometry(QtCore.QRect(40, 314, 21, 16))
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(Dialog)
        self.label_10.setGeometry(QtCore.QRect(130, 204, 51, 16))
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(Dialog)
        self.label_11.setGeometry(QtCore.QRect(330, 203, 81, 20))
        self.label_11.setObjectName("label_11")
        self.font_size_label = QtWidgets.QLabel(Dialog)
        self.font_size_label.setGeometry(QtCore.QRect(20, 366, 71, 20))
        self.font_size_label.setObjectName("font_size_label")
        self.line_3 = QtWidgets.QFrame(Dialog)
        self.line_3.setGeometry(QtCore.QRect(-10, 340, 501, 20))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.offset_label = QtWidgets.QLabel(Dialog)
        self.offset_label.setGeometry(QtCore.QRect(290, 406, 51, 16))
        self.offset_label.setObjectName("offset_label")
        self.line_4 = QtWidgets.QFrame(Dialog)
        self.line_4.setGeometry(QtCore.QRect(-10, 430, 501, 20))
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.apply_button = QtWidgets.QDialogButtonBox(Dialog)
        self.apply_button.setGeometry(QtCore.QRect(190, 450, 261, 32))
        self.apply_button.setOrientation(QtCore.Qt.Horizontal)
        self.apply_button.setStandardButtons(QtWidgets.QDialogButtonBox.Apply|QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.apply_button.setCenterButtons(True)
        self.apply_button.setObjectName("apply_button")
        
        self.apply_button.rejected.connect(Dialog.reject)
        self.apply_button.accepted.connect(Dialog.accept)
        self.apply_button.button(QtWidgets.QDialogButtonBox.Apply).clicked.connect(self.click_confirm)
        self.axes_signal.connect(parent.axes_signal.emit)

        self.titleIn_x = QtWidgets.QLineEdit(Dialog)
        self.titleIn_x.setGeometry(QtCore.QRect(140, 70, 141, 21))
        self.titleIn_x.setObjectName("title_x")
        self.titleIn_y = QtWidgets.QLineEdit(Dialog)
        self.titleIn_y.setGeometry(QtCore.QRect(140, 110, 141, 21))
        self.titleIn_y.setObjectName("title_y")
        self.titleIn_z = QtWidgets.QLineEdit(Dialog)
        self.titleIn_z.setGeometry(QtCore.QRect(140, 150, 141, 21))
        self.titleIn_z.setObjectName("title_z")
        self.intv_x = QtWidgets.QLineEdit(Dialog)
        self.intv_x.setGeometry(QtCore.QRect(330, 234, 71, 21))
        self.intv_x.setObjectName("intv_x")
        self.intv_y = QtWidgets.QLineEdit(Dialog)
        self.intv_y.setGeometry(QtCore.QRect(330, 274, 71, 21))
        self.intv_y.setObjectName("intv_y")
        self.intv_z = QtWidgets.QLineEdit(Dialog)
        self.intv_z.setGeometry(QtCore.QRect(330, 314, 71, 21))
        self.intv_z.setObjectName("intv_z")
        self.spinBox = QtWidgets.QSpinBox(Dialog)
        self.spinBox.setGeometry(QtCore.QRect(360, 402, 48, 24))
        self.spinBox.setObjectName("spinBox")
        self.axis_x_min = QtWidgets.QLineEdit(Dialog)
        self.axis_x_min.setGeometry(QtCore.QRect(110, 234, 71, 21))
        self.axis_x_min.setObjectName("lineEdit")
        self.axis_x_max = QtWidgets.QLineEdit(Dialog)
        self.axis_x_max.setGeometry(QtCore.QRect(210, 234, 71, 21))
        self.axis_x_max.setObjectName("lineEdit_2")
        self.label_12 = QtWidgets.QLabel(Dialog)
        self.label_12.setGeometry(QtCore.QRect(230, 204, 51, 16))
        self.label_12.setObjectName("label_12")
        self.axis_y_min = QtWidgets.QLineEdit(Dialog)
        self.axis_y_min.setGeometry(QtCore.QRect(110, 274, 71, 21))
        self.axis_y_min.setObjectName("lineEdit_3")
        self.axis_y_max = QtWidgets.QLineEdit(Dialog)
        self.axis_y_max.setGeometry(QtCore.QRect(210, 274, 71, 21))
        self.axis_y_max.setObjectName("lineEdit_4")
        self.axis_z_min = QtWidgets.QLineEdit(Dialog)
        self.axis_z_min.setGeometry(QtCore.QRect(110, 314, 71, 21))
        self.axis_z_min.setObjectName("lineEdit_5")
        self.axis_z_max = QtWidgets.QLineEdit(Dialog)
        self.axis_z_max.setGeometry(QtCore.QRect(210, 314, 71, 21))
        self.axis_z_max.setObjectName("lineEdit_6")
        self.checkBox = QtWidgets.QCheckBox(Dialog)
        self.checkBox.setGeometry(QtCore.QRect(360, 364, 71, 20))
        self.checkBox.setText("")
        self.checkBox.setObjectName("checkBox")
        self.offset_label_2 = QtWidgets.QLabel(Dialog)
        self.offset_label_2.setGeometry(QtCore.QRect(290, 367, 51, 16))
        self.offset_label_2.setObjectName("offset_label_2")
        self.title_2 = QtWidgets.QLabel(Dialog)
        self.title_2.setGeometry(QtCore.QRect(290, 54, 71, 16))
        self.title_2.setObjectName("title_2")
        self.slider_font = QtWidgets.QSlider(Dialog)
        self.slider_font.setGeometry(QtCore.QRect(130, 365, 111, 22))
        self.slider_font.setOrientation(QtCore.Qt.Horizontal)
        self.slider_font.setObjectName("horizontalSlider")
        self.font_size_label_2 = QtWidgets.QLabel(Dialog)
        self.font_size_label_2.setGeometry(QtCore.QRect(20, 402, 71, 20))
        self.font_size_label_2.setObjectName("font_size_label_2")
        self.slider_label = QtWidgets.QSlider(Dialog)
        self.slider_label.setGeometry(QtCore.QRect(130, 402, 111, 22))
        self.slider_label.setOrientation(QtCore.Qt.Horizontal)
        self.slider_label.setObjectName("horizontalSlider_2")
        self.title_3 = QtWidgets.QLabel(Dialog)
        self.title_3.setGeometry(QtCore.QRect(120, 387, 31, 16))
        self.title_3.setObjectName("title_3")
        self.title_4 = QtWidgets.QLabel(Dialog)
        self.title_4.setGeometry(QtCore.QRect(240, 386, 31, 16))
        self.title_4.setObjectName("title_4")
        self.spinBox_x = QtWidgets.QSpinBox(Dialog)
        self.spinBox_x.setGeometry(QtCore.QRect(340, 70, 48, 24))
        self.spinBox_x.setObjectName("spinBox_2")
        self.spinBox_y = QtWidgets.QSpinBox(Dialog)
        self.spinBox_y.setGeometry(QtCore.QRect(340, 110, 48, 24))
        self.spinBox_y.setObjectName("spinBox_3")
        self.spinBox_z = QtWidgets.QSpinBox(Dialog)
        self.spinBox_z.setGeometry(QtCore.QRect(340, 150, 48, 24))
        self.spinBox_z.setObjectName("spinBox_4")

        self.retranslateUi(Dialog)
        
        self.set_initial_status()
        
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.checkBox_x.setText(_translate("Dialog", "X "))
        self.checkBox_y.setText(_translate("Dialog", "Y"))
        self.checkBox_z.setText(_translate("Dialog", "Z"))
        self.show_axes.setText(_translate("Dialog", "Show axes"))
        self.title.setText(_translate("Dialog", "Titles"))
        self.label_3.setText(_translate("Dialog", "X"))
        self.label_4.setText(_translate("Dialog", "Y"))
        self.label_5.setText(_translate("Dialog", "Z"))
        self.label.setText(_translate("Dialog", "Labels"))
        self.label_7.setText(_translate("Dialog", "X"))
        self.label_8.setText(_translate("Dialog", "Y"))
        self.label_9.setText(_translate("Dialog", "Z"))
        self.label_10.setText(_translate("Dialog", "min."))
        self.label_11.setText(_translate("Dialog", "no. of labels"))
        self.font_size_label.setText(_translate("Dialog", "Font factor"))
        self.offset_label.setText(_translate("Dialog", "Offset"))
        self.label_12.setText(_translate("Dialog", "max."))
        self.offset_label_2.setText(_translate("Dialog", "Grid on"))
        self.title_2.setText(_translate("Dialog", "x 10^??"))
        self.font_size_label_2.setText(_translate("Dialog", "Label factor"))
        self.title_3.setText(_translate("Dialog", "1/4"))
        self.title_4.setText(_translate("Dialog", "2"))
     
    def click_confirm(self):
        
        self.record_status() 
        self.axes_signal.emit()

        pass

    def find_slider_value(self, factor_value):
        
        if factor_value >= self.factor_max:
            value = 99
        elif factor_value <= self.factor_min:
            value = 0
        else:
            value = 0.0 + 99.0*(factor_value - self.factor_min)/(self.factor_max - self.factor_min) 
            value = int(value)

        return value

    def find_factor_value(self, slider_value):

        value = float(slider_value)/99.0 * (self.factor_max - self.factor_min) + self.factor_min

        return value

    def record_status(self):

        if self.checkBox_x.isChecked():
            self.show_x = True
        else:
            self.show_x = False
        
        if self.checkBox_y.isChecked():
            self.show_y = True
        else:
            self.show_y = False

        if self.checkBox_z.isChecked():
            self.show_z = True
        else:
            self.show_z = False

        self.title_x = self.titleIn_x.text()
        self.title_y = self.titleIn_y.text()
        self.title_z = self.titleIn_z.text()

        self.noflabel_x = int(self.intv_x.text().encode('utf-8'))
        if self.noflabel_x<2:
            self.noflabel_x = 2
        self.noflabel_y = int(self.intv_y.text().encode('utf-8'))
        if self.noflabel_y<2:
            self.noflabel_y = 2
        self.noflabel_z = int(self.intv_z.text().encode('utf-8'))
        if self.noflabel_z<2:
            self.noflabel_z = 2

        min_val = float(self.axis_x_min.text().encode('utf-8'))
        max_val = float(self.axis_x_max.text().encode('utf-8'))
        self.bounds_x = (min_val, max_val)

        min_val = float(self.axis_y_min.text().encode('utf-8'))
        max_val = float(self.axis_y_max.text().encode('utf-8'))
        self.bounds_y = (min_val, max_val)

        min_val = float(self.axis_z_min.text().encode('utf-8'))
        max_val = float(self.axis_z_max.text().encode('utf-8'))
        self.bounds_z = (min_val, max_val)

        self.offset = self.spinBox.value()
        
        if self.checkBox.isChecked():
            self.grid_on = True
        else:
            self.grid_on = False
        
        self.font_factor  = self.find_factor_value(self.slider_font.value())
        self.label_factor = self.find_factor_value(self.slider_label.value()) 
        
        self.exponent_x = self.spinBox_x.value() 
        self.exponent_y = self.spinBox_y.value() 
        self.exponent_z = self.spinBox_z.value() 

    def set_initial_status(self):
        
        if self.show_x:
           self.checkBox_x.setChecked(True)
        else:
           self.checkBox_x.setChecked(False)
        
        if self.show_y:
           self.checkBox_y.setChecked(True)
        else:
           self.checkBox_y.setChecked(False)
        
        if self.show_z:
           self.checkBox_z.setChecked(True)
        else:
           self.checkBox_z.setChecked(False)

        self.titleIn_x.setText(self.title_x)
        self.titleIn_y.setText(self.title_y)
        self.titleIn_z.setText(self.title_z)
        
        self.intv_x.setText(str(self.noflabel_x))
        self.intv_y.setText(str(self.noflabel_y))
        self.intv_z.setText(str(self.noflabel_z))

        self.axis_x_min.setText(str(self.bounds_x[0]))
        self.axis_x_max.setText(str(self.bounds_x[1]))
        self.axis_y_min.setText(str(self.bounds_y[0]))
        self.axis_y_max.setText(str(self.bounds_y[1]))
        self.axis_z_min.setText(str(self.bounds_z[0]))
        self.axis_z_max.setText(str(self.bounds_z[1]))

        self.spinBox.setValue(self.offset)

        if self.grid_on:
            self.checkBox.setChecked(True)
        else:
            self.checkBox.setChecked(False)

        #print(self.font_factor)
        #print(self.find_slider_value(self.font_factor))
        self.slider_font.setValue(self.find_slider_value(self.font_factor))
        self.slider_label.setValue(self.find_slider_value(self.label_factor))

        self.spinBox_x.setValue(self.exponent_x)
        self.spinBox_y.setValue(self.exponent_y)
        self.spinBox_z.setValue(self.exponent_z)
        
