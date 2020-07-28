# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'vectorfield_form.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal

class popup_widget_4VF(QDialog): 
    def __init__(self, parent):
        super().__init__()
        self.setupUi(self, parent)

    vectorfield_signal = pyqtSignal(int) 
    scaling_factor = 1 
    skip_factor = 1    
    link_opt = 0 

    def setupUi(self, Dialog, parent):
        Dialog.setObjectName("Dialog")
        Dialog.resize(366, 219)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(12, 180, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.Apply)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setText("View")
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).setText("Close")
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Apply).setText("Export")
        
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(85, 77, 111, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(85, 30, 81, 21))
        self.label_2.setObjectName("label_2")
        self.lineEdit_skip = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_skip.setGeometry(QtCore.QRect(190, 31, 71, 21))
        self.lineEdit_skip.setObjectName("lineEdit_skip")
        self.lineEdit_scale = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_scale.setGeometry(QtCore.QRect(190, 77, 71, 21))
        self.lineEdit_scale.setObjectName("lineEdit_scale")

     #   self.radioButton = QtWidgets.QRadioButton(Dialog)
     #   self.radioButton.setGeometry(QtCore.QRect(240, 72, 100, 20))
     #   self.radioButton.setObjectName("radioButton")
     #   self.radioButton.toggled.connect(self.clicked_Rbutton)

     #   self.radioButton_2 = QtWidgets.QRadioButton(Dialog)
     #   self.radioButton_2.setGeometry(QtCore.QRect(240, 102, 100, 20))
     #   self.radioButton_2.setObjectName("radioButton_2")
     #   self.radioButton_2.toggled.connect(self.clicked_Rbutton)

     #   self.radioButton_3 = QtWidgets.QRadioButton(Dialog)
     #   self.radioButton_3.setGeometry(QtCore.QRect(240, 132, 100, 20))
     #   self.radioButton_3.setObjectName("radioButton_3")
     #   self.radioButton_3.toggled.connect(self.clicked_Rbutton)
        
        self.textBrowser = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser.setGeometry(QtCore.QRect(60, 124, 251, 41))
        self.textBrowser.setObjectName("textBrowser")
        self.frame_2 = QtWidgets.QFrame(Dialog)
        self.frame_2.setGeometry(QtCore.QRect(55, 119, 261, 51))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
       # self.line = QtWidgets.QFrame(Dialog)
       # self.line.setGeometry(QtCore.QRect(223, 20, 121, 20))
       # self.line.setFrameShape(QtWidgets.QFrame.HLine)
       # self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
       # self.line.setObjectName("line")
       # self.label_3 = QtWidgets.QLabel(Dialog)
       # self.label_3.setGeometry(QtCore.QRect(230, 40, 111, 16))
       # self.label_3.setObjectName("label_3")
       # self.line_2 = QtWidgets.QFrame(Dialog)
       # self.line_2.setGeometry(QtCore.QRect(223, 161, 121, 20))
       # self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
       # self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
       # self.line_2.setObjectName("line_2")
       # self.line_3 = QtWidgets.QFrame(Dialog)
       # self.line_3.setGeometry(QtCore.QRect(214, 29, 20, 141))
       # self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
       # self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
       # self.line_3.setObjectName("line_3")
       # self.line_4 = QtWidgets.QFrame(Dialog)
       # self.line_4.setGeometry(QtCore.QRect(334, 29, 20, 141))
       # self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
       # self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
       # self.line_4.setObjectName("line_4")

        self.retranslateUi(Dialog)
        ##self.buttonBox.accepted.connect(Dialog.accept)

        self.buttonBox.accepted.connect(self.click_view)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Apply).clicked.connect(self.click_confirm)
        self.vectorfield_signal.connect(lambda val: parent.vectorfield_signal.emit(val))
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Scaling factor:"))
        self.label_2.setText(_translate("Dialog", "Skip factor:"))
     #   self.radioButton.setText(_translate("Dialog", "cutplane"))
     #   self.radioButton_2.setText(_translate("Dialog", "isosurface"))
     #   self.radioButton_3.setText(_translate("Dialog", "streamline"))
     #   self.label_3.setText(_translate("Dialog", "Linkage option:"))
        self.textBrowser.setPlainText('linkage to the geometries specified in the main window')

    def clicked_Rbutton(self):
        if self.radioButton.isChecked():
            self.textBrowser.setPlainText('linkage to the specified cutplane')
        elif self.radioButton_2.isChecked():
            self.textBrowser.setPlainText('linkage to the specified isosurface')
        elif self.radioButton_3.isChecked(): 
            self.textBrowser.setPlainText('linkage to the specified streamline')

    def set_message(self, opt):
        
        if opt==1:   # for linkage to cutplane
            self.textBrowser.setPlainText('established linkage to cutplane')
            self.link_opt = 1
        elif opt==2: # for linkage to isosurface
            self.textBrowser.setPlainText('established linkage to isosurface')
            self.link_opt = 2 
        elif opt==3: # for linkage to streamline
            self.textBrowser.setPlainText('established linkage to streamline')
            self.link_opt = 3 
        else: 
            self.textBrowser.setPlainText('no scene unit specified; linkage to the 3D data')
            self.link_opt = 4 

    def click_view(self):

        lstr = self.lineEdit_scale.text().encode('utf-8')
        lstr_split = [float(s) for s in lstr.split()]

        self.scaling_factor = lstr_split[0]
        
        lstr = self.lineEdit_skip.text().encode('utf-8')
        lstr_split = [int(s) for s in lstr.split()]

        self.skip_factor = lstr_split[0]

        self.vectorfield_signal.emit(0)

    def click_confirm(self):
        
        lstr = self.lineEdit_scale.text().encode('utf-8')
        lstr_split = [float(s) for s in lstr.split()]

        self.scaling_factor = lstr_split[0]
        
        lstr = self.lineEdit_skip.text().encode('utf-8')
        lstr_split = [int(s) for s in lstr.split()]

        self.skip_factor = lstr_split[0]

        self.vectorfield_signal.emit(1)

