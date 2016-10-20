# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui\testWidget.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_testWidget(object):
    def setupUi(self, testWidget):
        testWidget.setObjectName(_fromUtf8("testWidget"))
        testWidget.resize(920, 825)
        self.frame = QtGui.QFrame(testWidget)
        self.frame.setGeometry(QtCore.QRect(10, 10, 901, 811))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QtCore.QSize(830, 750))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayoutWidget = QtGui.QWidget(self.frame)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 10, 591, 61))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_4 = QtGui.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS Shell Dlg 2"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 2)
        self.rot_chart = QtGui.QWidget(self.frame)
        self.rot_chart.setGeometry(QtCore.QRect(10, 90, 881, 175))
        self.rot_chart.setMinimumSize(QtCore.QSize(800, 175))
        self.rot_chart.setObjectName(_fromUtf8("rot_chart"))
        self.calibButton = QtGui.QPushButton(self.frame)
        self.calibButton.setGeometry(QtCore.QRect(370, 770, 141, 31))
        self.calibButton.setObjectName(_fromUtf8("calibButton"))
        self.labelSkeleton = QtGui.QLabel(self.frame)
        self.labelSkeleton.setGeometry(QtCore.QRect(10, 470, 421, 291))
        self.labelSkeleton.setText(_fromUtf8(""))
        self.labelSkeleton.setObjectName(_fromUtf8("labelSkeleton"))
        self.frame_GL = QtGui.QFrame(self.frame)
        self.frame_GL.setGeometry(QtCore.QRect(450, 470, 441, 291))
        self.frame_GL.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_GL.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_GL.setObjectName(_fromUtf8("frame_GL"))
        self.rot_chart_2 = QtGui.QWidget(self.frame)
        self.rot_chart_2.setGeometry(QtCore.QRect(10, 280, 881, 175))
        self.rot_chart_2.setMinimumSize(QtCore.QSize(800, 175))
        self.rot_chart_2.setObjectName(_fromUtf8("rot_chart_2"))
        self.frame.raise_()
        self.frame_GL.raise_()
        self.labelSkeleton.raise_()
        self.frame_GL.raise_()

        self.retranslateUi(testWidget)
        QtCore.QMetaObject.connectSlotsByName(testWidget)

    def retranslateUi(self, testWidget):
        self.label_4.setText(_translate("testWidget", "Test Orientation", None))
        self.calibButton.setText(_translate("testWidget", "Calibrate IMU", None))

