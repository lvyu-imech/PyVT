# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'streamline.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal

class popup_widget_4SL(QWidget):
   
    streamline_signal = pyqtSignal(int)

    #streamline setup parameters
    SL_seed_type = 'other' 
    SL_point_center = (0, 0, 0)
    SL_point_radius = 0.0
    SL_point_numseed = 1 
    SL_line_pointA = (0, 0, 0)
    SL_line_pointB = (1, 0, 0) 
    SL_line_reso   = 10  
    SL_plane_origin = (0, 0, 0) 
    SL_plane_pointA = (1, 0, 0) 
    SL_plane_pointB = (0, 1, 0)
    SL_plane_resoX = 10 
    SL_plane_resoY = 10 

    SL_integ_direct    = 'forward'
    SL_integ_max_step  = 100 
    SL_integ_init_step = 0.1 

    def __init__(self, parent):
        super().__init__()
        self.setupUi(self, parent)

    def setupUi(self, Form, parent):
        Form.setObjectName("Define Streamline")
        Form.resize(452, 314)
        self.Rbutton_point = QtWidgets.QRadioButton(Form)
        self.Rbutton_point.setGeometry(QtCore.QRect(10, 20, 100, 20))
        self.Rbutton_point.setObjectName("Rbutton_point")
        self.Rbutton_point.toggled.connect(self.clicked_Rbutton)

        self.Rbutton_line = QtWidgets.QRadioButton(Form)
        self.Rbutton_line.setGeometry(QtCore.QRect(140, 20, 100, 20))
        self.Rbutton_line.setObjectName("Rbutton_line")
        self.Rbutton_line.toggled.connect(self.clicked_Rbutton)

        self.Rbutton_plane = QtWidgets.QRadioButton(Form)
        self.Rbutton_plane.setGeometry(QtCore.QRect(300, 20, 100, 20))
        self.Rbutton_plane.setObjectName("Rbutton_plane")
        self.Rbutton_plane.toggled.connect(self.clicked_Rbutton)

        self.Ledit_max_step = QtWidgets.QLineEdit(Form)
        self.Ledit_max_step.setGeometry(QtCore.QRect(180, 240, 81, 21))
        self.Ledit_max_step.setText("")
        self.Ledit_max_step.setObjectName("Ledit_max_step")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(180, 220, 91, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(320, 220, 91, 16))
        self.label_2.setObjectName("label_2")
        self.Ledit_init_step = QtWidgets.QLineEdit(Form)
        self.Ledit_init_step.setGeometry(QtCore.QRect(320, 240, 81, 21))
        self.Ledit_init_step.setText("")
        self.Ledit_init_step.setObjectName("Ledit_init_step")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(30, 220, 91, 16))
        self.label_3.setObjectName("label_3")
        self.Ledit_point_center = QtWidgets.QLineEdit(Form)
        self.Ledit_point_center.setGeometry(QtCore.QRect(20, 70, 81, 21))
        self.Ledit_point_center.setText("")
        self.Ledit_point_center.setObjectName("Ledit_point_center")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(20, 50, 101, 16))
        self.label_4.setObjectName("label_4")
        self.Ledit_point_num_seed = QtWidgets.QLineEdit(Form)
        self.Ledit_point_num_seed.setGeometry(QtCore.QRect(20, 120, 81, 21))
        self.Ledit_point_num_seed.setText("")
        self.Ledit_point_num_seed.setObjectName("Ledit_point_num_seed")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(20, 100, 101, 16))
        self.label_5.setObjectName("label_5")
        
        self.label_o1 = QtWidgets.QLabel(Form)
        self.label_o1.setGeometry(QtCore.QRect(20, 150, 101, 16))
        
        self.Ledit_point_radius = QtWidgets.QLineEdit(Form)
        self.Ledit_point_radius.setGeometry(QtCore.QRect(20, 170, 81, 21))
        self.Ledit_point_radius.setText("")

        self.Ledit_line_pointA = QtWidgets.QLineEdit(Form)
        self.Ledit_line_pointA.setGeometry(QtCore.QRect(140, 70, 81, 21))
        self.Ledit_line_pointA.setText("")
        self.Ledit_line_pointA.setObjectName("Ledit_line_pointA")
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(140, 50, 101, 16))
        self.label_6.setObjectName("label_6")
        self.Ledit_line_reso = QtWidgets.QLineEdit(Form)
        self.Ledit_line_reso.setGeometry(QtCore.QRect(140, 170, 81, 21))
        self.Ledit_line_reso.setText("")
        self.Ledit_line_reso.setObjectName("Ledit_line_reso")
        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setGeometry(QtCore.QRect(140, 150, 101, 16))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setGeometry(QtCore.QRect(140, 100, 101, 16))
        self.label_8.setObjectName("label_8")
        self.Ledit_line_pointB = QtWidgets.QLineEdit(Form)
        self.Ledit_line_pointB.setGeometry(QtCore.QRect(140, 120, 81, 21))
        self.Ledit_line_pointB.setText("")
        self.Ledit_line_pointB.setObjectName("Ledit_line_pointB")
        self.label_9 = QtWidgets.QLabel(Form)
        self.label_9.setGeometry(QtCore.QRect(260, 100, 101, 16))
        self.label_9.setObjectName("label_9")
        self.Ledit_plane_pointA = QtWidgets.QLineEdit(Form)
        self.Ledit_plane_pointA.setGeometry(QtCore.QRect(260, 120, 81, 21))
        self.Ledit_plane_pointA.setText("")
        self.Ledit_plane_pointA.setObjectName("Ledit_plane_pointA")
        self.Ledit_plane_pointB = QtWidgets.QLineEdit(Form)
        self.Ledit_plane_pointB.setGeometry(QtCore.QRect(260, 170, 81, 21))
        self.Ledit_plane_pointB.setText("")
        self.Ledit_plane_pointB.setObjectName("Ledit_plane_pointB")
        self.label_10 = QtWidgets.QLabel(Form)
        self.label_10.setGeometry(QtCore.QRect(260, 150, 101, 16))
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(Form)
        self.label_11.setGeometry(QtCore.QRect(360, 80, 81, 20))
        self.label_11.setObjectName("label_11")
        self.Ledit_plane_resoX = QtWidgets.QLineEdit(Form)
        self.Ledit_plane_resoX.setGeometry(QtCore.QRect(370, 100, 41, 21))
        self.Ledit_plane_resoX.setText("")
        self.Ledit_plane_resoX.setObjectName("Ledit_plane_resoX")
        self.label_12 = QtWidgets.QLabel(Form)
        self.label_12.setGeometry(QtCore.QRect(360, 130, 81, 20))
        self.label_12.setObjectName("label_12")
        self.Ledit_plane_resoY = QtWidgets.QLineEdit(Form)
        self.Ledit_plane_resoY.setGeometry(QtCore.QRect(370, 150, 41, 21))
        self.Ledit_plane_resoY.setText("")
        self.Ledit_plane_resoY.setObjectName("Ledit_plane_resoY")
        self.Ledit_plane_origin = QtWidgets.QLineEdit(Form)
        self.Ledit_plane_origin.setGeometry(QtCore.QRect(260, 70, 81, 21))
        self.Ledit_plane_origin.setText("")
        self.Ledit_plane_origin.setObjectName("Ledit_plane_origin")
        self.label_13 = QtWidgets.QLabel(Form)
        self.label_13.setGeometry(QtCore.QRect(260, 50, 101, 16))
        self.label_13.setObjectName("label_13")
        self.line = QtWidgets.QFrame(Form)
        self.line.setGeometry(QtCore.QRect(0, 200, 501, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(Form)
        self.line_2.setGeometry(QtCore.QRect(110, 0, 20, 201))
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(Form)
        self.line_3.setGeometry(QtCore.QRect(230, 0, 20, 201))
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.comboBox = QtWidgets.QComboBox(Form)
        self.comboBox.setGeometry(QtCore.QRect(30, 240, 104, 26))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.activated[str].connect(self.comboChanged)
        
        self.line_4 = QtWidgets.QFrame(Form)
        self.line_4.setGeometry(QtCore.QRect(0, 192, 501, 20))
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")

        self.buttonBox = QtWidgets.QDialogButtonBox(Form)
        self.buttonBox.setGeometry(QtCore.QRect(33, 280, 371, 32))
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.Apply)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setText("View")
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).setText("Close")
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Apply).setText("Export")

        self.buttonBox.accepted.connect(self.click_view)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Apply).clicked.connect(self.click_confirm)
        self.buttonBox.rejected.connect(self.close)
        self.streamline_signal.connect(lambda val: parent.streamline_signal.emit(val))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        Form.setWhatsThis(_translate("Form", "<html><head/><body><p>Streamline</p></body></html>"))
        self.Rbutton_point.setText(_translate("Form", "Point Seed"))
        self.Rbutton_line.setText(_translate("Form", "Line Seed"))
        self.Rbutton_plane.setText(_translate("Form", "Plane Seed"))
        self.label.setText(_translate("Form", "max. step no."))
        self.label_2.setText(_translate("Form", "init. step size"))
        self.label_3.setText(_translate("Form", "integ. direction"))
        self.label_4.setText(_translate("Form", "center"))
        self.label_5.setText(_translate("Form", "no. of seeds"))
        self.label_o1.setText(_translate("Form", "radius"))

        self.label_6.setText(_translate("Form", "point A "))
        self.label_7.setText(_translate("Form", "resolution"))
        self.label_8.setText(_translate("Form", "point B "))
        self.label_9.setText(_translate("Form", "point A "))
        self.label_10.setText(_translate("Form", "point B "))
        self.label_11.setText(_translate("Form", "resolution X"))
        self.label_12.setText(_translate("Form", "resolution Y"))
        self.label_13.setText(_translate("Form", "origin"))
        self.comboBox.setItemText(0, _translate("Form", "forward"))
        self.comboBox.setItemText(1, _translate("Form", "backward"))
        self.comboBox.setItemText(2, _translate("Form", "both"))


    def comboChanged(self, text):
        self.SL_integ_direct = text   #integration direction; default: forward

    def clicked_Rbutton(self):
        if self.Rbutton_point.isChecked():
            self.SL_seed_type = 'point'
        if self.Rbutton_line.isChecked():
            self.SL_seed_type = 'line'
        if self.Rbutton_plane.isChecked():
            self.SL_seed_type = 'plane'

    def read_input(self):

        if self.SL_seed_type == 'point':
            lstr = self.Ledit_point_center.text().encode('utf-8')
            self.SL_point_center = tuple([float(s) for s in lstr.split()])   #only take the first three
            lstr = self.Ledit_point_num_seed.text().encode('utf-8')
            self.SL_point_numseed = int(lstr)
            lstr = self.Ledit_point_radius.text().encode('utf-8')
            self.SL_point_radius = float(lstr)

        if self.SL_seed_type == 'line':
            lstr = self.Ledit_line_pointA.text().encode('utf-8')
            self.SL_line_pointA = tuple([float(s) for s in lstr.split()])   #only take the first three
            lstr = self.Ledit_line_pointB.text().encode('utf-8')
            self.SL_line_pointB = tuple([float(s) for s in lstr.split()])   #only take the first three
            lstr = self.Ledit_line_reso.text().encode('utf-8')
            self.SL_line_reso = int(lstr)

        if self.SL_seed_type == 'plane':
            lstr = self.Ledit_plane_origin.text().encode('utf-8')
            self.SL_plane_origin = tuple([float(s) for s in lstr.split()])
            lstr = self.Ledit_plane_pointA.text().encode('utf-8')
            self.SL_plane_pointA = tuple([float(s) for s in lstr.split()])
            lstr = self.Ledit_plane_pointB.text().encode('utf-8')
            self.SL_plane_pointB = tuple([float(s) for s in lstr.split()])
            lstr = self.Ledit_plane_resoX.text().encode('utf-8')
            self.SL_plane_resoX = int(lstr)
            lstr = self.Ledit_plane_resoY.text().encode('utf-8')
            self.SL_plane_resoY = int(lstr)

        lstr = self.Ledit_max_step.text().encode('utf-8')
        self.SL_integ_max_step = float(lstr)      # !bug to be fixed; int(lstr)
        lstr = self.Ledit_init_step.text().encode('utf-8')
        self.SL_integ_init_step = float(lstr)

        #self.print_param_input()
        #self.close()

    def click_view(self):
        
        self.read_input()
        self.streamline_signal.emit(0)
    
    def click_confirm(self):

        self.read_input()
        self.streamline_signal.emit(1)

    def print_param_input(self):
        
        print(self.SL_seed_type)
        print(self.SL_point_center)
        print(self.SL_point_numseed)
        print(self.SL_line_pointA)
        print(self.SL_line_pointB)
        print(self.SL_line_reso)
        print(self.SL_plane_origin)
        print(self.SL_plane_pointA)
        print(self.SL_plane_pointB)
        print(self.SL_plane_resoX)
        print(self.SL_plane_resoY)

