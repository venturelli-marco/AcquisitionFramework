# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui\saveWidget.ui'
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

class Ui_saveWidget(object):
    def setupUi(self, saveWidget):
        saveWidget.setObjectName(_fromUtf8("saveWidget"))
        saveWidget.resize(920, 790)
        self.frame = QtGui.QFrame(saveWidget)
        self.frame.setGeometry(QtCore.QRect(40, 20, 851, 681))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayoutWidget = QtGui.QWidget(self.frame)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(60, 60, 701, 151))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_6 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_6.setText(_fromUtf8(""))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 4, 2, 1, 1)
        self.textFilename = QtGui.QLineEdit(self.gridLayoutWidget)
        self.textFilename.setObjectName(_fromUtf8("textFilename"))
        self.gridLayout.addWidget(self.textFilename, 3, 1, 1, 1)
        self.label = QtGui.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)
        self.label_save = QtGui.QLabel(self.gridLayoutWidget)
        self.label_save.setText(_fromUtf8(""))
        self.label_save.setObjectName(_fromUtf8("label_save"))
        self.gridLayout.addWidget(self.label_save, 5, 2, 1, 1)
        self.label_5 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_5.setText(_fromUtf8(""))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)
        self.progressBar = QtGui.QProgressBar(self.gridLayoutWidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout.addWidget(self.progressBar, 5, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_2.setText(_fromUtf8(""))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 5, 0, 1, 1)
        self.label_8 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_8.setText(_fromUtf8(""))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout.addWidget(self.label_8, 2, 2, 1, 1)
        self.label_7 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_7.setText(_fromUtf8(""))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 2, 3, 1, 2)
        self.label_4 = QtGui.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS Shell Dlg 2"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 2)
        self.buttonStart = QtGui.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonStart.sizePolicy().hasHeightForWidth())
        self.buttonStart.setSizePolicy(sizePolicy)
        self.buttonStart.setObjectName(_fromUtf8("buttonStart"))
        self.gridLayout.addWidget(self.buttonStart, 3, 3, 1, 1)
        self.buttonStop = QtGui.QPushButton(self.gridLayoutWidget)
        self.buttonStop.setObjectName(_fromUtf8("buttonStop"))
        self.gridLayout.addWidget(self.buttonStop, 3, 4, 1, 1)
        self.calibButton = QtGui.QPushButton(self.gridLayoutWidget)
        self.calibButton.setObjectName(_fromUtf8("calibButton"))
        self.gridLayout.addWidget(self.calibButton, 4, 3, 1, 1)
        self.saveMethodCheck = QtGui.QCheckBox(self.gridLayoutWidget)
        self.saveMethodCheck.setChecked(True)
        self.saveMethodCheck.setObjectName(_fromUtf8("saveMethodCheck"))
        self.gridLayout.addWidget(self.saveMethodCheck, 4, 1, 1, 1)
        self.getBackgroundButton = QtGui.QPushButton(self.gridLayoutWidget)
        self.getBackgroundButton.setObjectName(_fromUtf8("getBackgroundButton"))
        self.gridLayout.addWidget(self.getBackgroundButton, 5, 3, 1, 1)
        self.gridLayoutWidget_2 = QtGui.QWidget(self.frame)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(60, 300, 701, 336))
        self.gridLayoutWidget_2.setObjectName(_fromUtf8("gridLayoutWidget_2"))
        self.gridLayout_2 = QtGui.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_17 = QtGui.QLabel(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_17.setFont(font)
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.gridLayout_2.addWidget(self.label_17, 5, 0, 1, 1)
        self.previewLabel = QtGui.QLabel(self.gridLayoutWidget_2)
        self.previewLabel.setMinimumSize(QtCore.QSize(100, 100))
        self.previewLabel.setText(_fromUtf8(""))
        self.previewLabel.setObjectName(_fromUtf8("previewLabel"))
        self.gridLayout_2.addWidget(self.previewLabel, 10, 0, 1, 1)
        self.label_18 = QtGui.QLabel(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_18.setFont(font)
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.gridLayout_2.addWidget(self.label_18, 6, 0, 1, 1)
        self.thresholdSlider = QtGui.QSlider(self.gridLayoutWidget_2)
        self.thresholdSlider.setMaximum(255)
        self.thresholdSlider.setProperty("value", 110)
        self.thresholdSlider.setTracking(True)
        self.thresholdSlider.setOrientation(QtCore.Qt.Horizontal)
        self.thresholdSlider.setTickPosition(QtGui.QSlider.NoTicks)
        self.thresholdSlider.setObjectName(_fromUtf8("thresholdSlider"))
        self.gridLayout_2.addWidget(self.thresholdSlider, 4, 1, 1, 1)
        self.label_19 = QtGui.QLabel(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_19.setFont(font)
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.gridLayout_2.addWidget(self.label_19, 7, 0, 1, 1)
        self.thLabel = QtGui.QLabel(self.gridLayoutWidget_2)
        self.thLabel.setObjectName(_fromUtf8("thLabel"))
        self.gridLayout_2.addWidget(self.thLabel, 4, 3, 1, 1)
        self.label_9 = QtGui.QLabel(self.gridLayoutWidget_2)
        self.label_9.setText(_fromUtf8(""))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout_2.addWidget(self.label_9, 4, 2, 1, 1)
        self.textFilename_2 = QtGui.QLineEdit(self.gridLayoutWidget_2)
        self.textFilename_2.setObjectName(_fromUtf8("textFilename_2"))
        self.gridLayout_2.addWidget(self.textFilename_2, 3, 1, 1, 1)
        self.label_10 = QtGui.QLabel(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_10.setFont(font)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout_2.addWidget(self.label_10, 3, 0, 1, 1)
        self.label_11 = QtGui.QLabel(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_11.setFont(font)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout_2.addWidget(self.label_11, 4, 0, 1, 1)
        self.label_save_2 = QtGui.QLabel(self.gridLayoutWidget_2)
        self.label_save_2.setText(_fromUtf8(""))
        self.label_save_2.setObjectName(_fromUtf8("label_save_2"))
        self.gridLayout_2.addWidget(self.label_save_2, 9, 2, 1, 1)
        self.progressBar_2 = QtGui.QProgressBar(self.gridLayoutWidget_2)
        self.progressBar_2.setProperty("value", 0)
        self.progressBar_2.setObjectName(_fromUtf8("progressBar_2"))
        self.gridLayout_2.addWidget(self.progressBar_2, 9, 1, 1, 1)
        self.label_12 = QtGui.QLabel(self.gridLayoutWidget_2)
        self.label_12.setText(_fromUtf8(""))
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.gridLayout_2.addWidget(self.label_12, 2, 0, 1, 1)
        self.label_13 = QtGui.QLabel(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_13.setFont(font)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.gridLayout_2.addWidget(self.label_13, 9, 0, 1, 1)
        self.label_14 = QtGui.QLabel(self.gridLayoutWidget_2)
        self.label_14.setText(_fromUtf8(""))
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.gridLayout_2.addWidget(self.label_14, 2, 2, 1, 1)
        self.label_15 = QtGui.QLabel(self.gridLayoutWidget_2)
        self.label_15.setText(_fromUtf8(""))
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.gridLayout_2.addWidget(self.label_15, 2, 3, 1, 2)
        self.buttonStop_2 = QtGui.QPushButton(self.gridLayoutWidget_2)
        self.buttonStop_2.setObjectName(_fromUtf8("buttonStop_2"))
        self.gridLayout_2.addWidget(self.buttonStop_2, 3, 4, 1, 1)
        self.label_16 = QtGui.QLabel(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS Shell Dlg 2"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_16.setFont(font)
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.gridLayout_2.addWidget(self.label_16, 0, 0, 1, 2)
        self.buttonStart_2 = QtGui.QPushButton(self.gridLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonStart_2.sizePolicy().hasHeightForWidth())
        self.buttonStart_2.setSizePolicy(sizePolicy)
        self.buttonStart_2.setObjectName(_fromUtf8("buttonStart_2"))
        self.gridLayout_2.addWidget(self.buttonStart_2, 3, 3, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.faceLabel = QtGui.QLabel(self.gridLayoutWidget_2)
        self.faceLabel.setMinimumSize(QtCore.QSize(100, 100))
        self.faceLabel.setText(_fromUtf8(""))
        self.faceLabel.setObjectName(_fromUtf8("faceLabel"))
        self.horizontalLayout.addWidget(self.faceLabel)
        self.faceBSLabel = QtGui.QLabel(self.gridLayoutWidget_2)
        self.faceBSLabel.setText(_fromUtf8(""))
        self.faceBSLabel.setObjectName(_fromUtf8("faceBSLabel"))
        self.horizontalLayout.addWidget(self.faceBSLabel)
        self.faceNormLabel = QtGui.QLabel(self.gridLayoutWidget_2)
        self.faceNormLabel.setText(_fromUtf8(""))
        self.faceNormLabel.setObjectName(_fromUtf8("faceNormLabel"))
        self.horizontalLayout.addWidget(self.faceNormLabel)
        self.faceEqLabel = QtGui.QLabel(self.gridLayoutWidget_2)
        self.faceEqLabel.setText(_fromUtf8(""))
        self.faceEqLabel.setObjectName(_fromUtf8("faceEqLabel"))
        self.horizontalLayout.addWidget(self.faceEqLabel)
        self.gridLayout_2.addLayout(self.horizontalLayout, 10, 1, 1, 1)
        self.label_20 = QtGui.QLabel(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_20.setFont(font)
        self.label_20.setObjectName(_fromUtf8("label_20"))
        self.gridLayout_2.addWidget(self.label_20, 8, 0, 1, 1)
        self.xBox = QtGui.QSpinBox(self.gridLayoutWidget_2)
        self.xBox.setMaximum(1000)
        self.xBox.setObjectName(_fromUtf8("xBox"))
        self.gridLayout_2.addWidget(self.xBox, 5, 1, 1, 1)
        self.yBox = QtGui.QSpinBox(self.gridLayoutWidget_2)
        self.yBox.setMaximum(1000)
        self.yBox.setObjectName(_fromUtf8("yBox"))
        self.gridLayout_2.addWidget(self.yBox, 6, 1, 1, 1)
        self.wBox = QtGui.QSpinBox(self.gridLayoutWidget_2)
        self.wBox.setMaximum(1000)
        self.wBox.setObjectName(_fromUtf8("wBox"))
        self.gridLayout_2.addWidget(self.wBox, 7, 1, 1, 1)
        self.hBox = QtGui.QSpinBox(self.gridLayoutWidget_2)
        self.hBox.setMaximum(1000)
        self.hBox.setObjectName(_fromUtf8("hBox"))
        self.gridLayout_2.addWidget(self.hBox, 8, 1, 1, 1)

        self.retranslateUi(saveWidget)
        QtCore.QMetaObject.connectSlotsByName(saveWidget)

    def retranslateUi(self, saveWidget):
        self.textFilename.setText(_translate("saveWidget", "acquisition", None))
        self.label.setText(_translate("saveWidget", "File Name:", None))
        self.label_3.setText(_translate("saveWidget", "Progress", None))
        self.label_4.setText(_translate("saveWidget", "Save Orientation", None))
        self.buttonStart.setText(_translate("saveWidget", "Start", None))
        self.buttonStop.setText(_translate("saveWidget", "Stop", None))
        self.calibButton.setText(_translate("saveWidget", "Calibrate IMU", None))
        self.saveMethodCheck.setText(_translate("saveWidget", "Save during acquisition", None))
        self.getBackgroundButton.setText(_translate("saveWidget", "getBackground", None))
        self.label_17.setText(_translate("saveWidget", "x:", None))
        self.label_18.setText(_translate("saveWidget", "y:", None))
        self.label_19.setText(_translate("saveWidget", "w:", None))
        self.thLabel.setText(_translate("saveWidget", "110", None))
        self.textFilename_2.setText(_translate("saveWidget", "acquisition", None))
        self.label_10.setText(_translate("saveWidget", "File Name:", None))
        self.label_11.setText(_translate("saveWidget", "Threshold:", None))
        self.label_13.setText(_translate("saveWidget", "Progress", None))
        self.buttonStop_2.setText(_translate("saveWidget", "Stop", None))
        self.label_16.setText(_translate("saveWidget", "Extract Faces ", None))
        self.buttonStart_2.setText(_translate("saveWidget", "Start", None))
        self.label_20.setText(_translate("saveWidget", "h:", None))

