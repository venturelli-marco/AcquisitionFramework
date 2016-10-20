from __future__ import division
from PyQt4 import QtGui, QtCore  # importiamo i moduli necessari
import cv2
import numpy as np

from gui.mainwindow import Ui_MainWindow
from app.saveWidgetCtr import saveForm
from app.testWidgetCrl import testForm
from acquisitions import acquisitionKinect, acquisitionIMU
from model.frameSet import frameSet
from acquisitions.IMU.calibration import CALIBRATION_FRAMES

class applicationForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.saveForm = None
        self.testForm = None

        self.ui.kinect_radio.setIcon(QtGui.QIcon("resources/images/kinect2.png"))
        self.ui.imu_radio.setIcon(QtGui.QIcon("resources/images/IMU.png"))
        self.ui.kinect_imu_radio.setIcon(QtGui.QIcon("resources/images/kinectIMU.png"))

        self.ui.kinect_radio.setIconSize(QtCore.QSize(100,100))
        self.ui.imu_radio.setIconSize(QtCore.QSize(100,100))
        self.ui.kinect_imu_radio.setIconSize(QtCore.QSize(100,100))

        self.ui.start_btn.clicked.connect(self.startAcquisition)
        self.ui.start_btn.clicked.connect(self.resetGUI)

        self.ui.imu_radio.clicked.connect(self.checkChanged)
        self.ui.kinect_imu_radio.clicked.connect(self.checkChanged)
        self.ui.kinect_radio.clicked.connect(self.checkChanged)

        self.ui.save_radio.clicked.connect(self.checkChanged)
        self.ui.test_radio.clicked.connect(self.checkChanged)

        self.ui.default_config.clicked.connect(self.configChecked)

        self.ui.actionHome.triggered.connect(self.resetHome)

        self.frame = frameSet()

        self.kinect = None
        # self.imu = None
        self.imu = []

        self.timer = QtCore.QTimer(self)
        self.t_fps = QtCore.QTimer(self)
        self.fps = 0

        self.calib = [False, False]
        self.calib_step = 0
        self.ui.calibBar.setVisible(False)
        self.ui.calibLabel.setVisible(False)

        self.ui.shoulder_device_box.setEnabled(True)
        self.ui.head_device_box.setEnabled(True)

        self.connect(self.timer, QtCore.SIGNAL('timeout()'), self.acquireFrame)
        self.connect(self.t_fps, QtCore.SIGNAL('timeout()'), self.updateFPS)

        self.connect(self, QtCore.SIGNAL('calibFrameAcquired()'), self.updateCalibBar)
        self.connect(self, QtCore.SIGNAL('calibFrameEnded()'), self.endUpdateCalibBar)

        self.connect(self, QtCore.SIGNAL('triggered()'), self.closeEvent)

    def closeEvent(self, event):
        # if self.imu is not None:
        if len(self.imu) > 0:
            print "Killing IMU thread(s)"
            # self.imu.close()
            for imu in self.imu:
                imu.close()

        self.close()
        self.destroy()

    def calibration(self):
        msg = QtGui.QMessageBox()
        msg.setIcon(QtGui.QMessageBox.Information)
        msg.setText("IMU calibration is going to be performed")
        msg.setInformativeText("Calibration needs a few seconds to complete. \nKeep your head as still as possible")
        msg.setWindowTitle("Calibration")
        msg.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
        ret = msg.exec_()
        if ret == QtGui.QMessageBox.Ok:
            self.calib = [True, True]
            self.calib_step = 0
            self.ui.calibBar.reset()
            self.ui.calibBar.setValue(0)
            self.ui.calibLabel.setText("Calibrating...")
            self.ui.calibBar.setVisible(True)
            self.ui.calibLabel.setVisible(True)

    def endUpdateCalibBar(self):
        self.calib_step = 0
        self.ui.calibLabel.setText("Calibration completed!")

    def updateCalibBar(self):
        self.calib_step += 1
        self.ui.calibBar.setValue((self.calib_step/self.ui.numIMUBox.value())*100/CALIBRATION_FRAMES)

    def startAcquisition(self):
        # if self.ui.test_radio.isChecked():
        #     if self.ui.kinect_radio.isChecked():
        #         acquisitionKinect.test()
        #     if self.ui.imu_radio.isChecked():
        #         acquisitionIMU.test()
        self.ui.sensor_label.setText("Trying to connect to given sensor(s)...")

        if self.ui.kinect_radio.isChecked() or self.ui.kinect_imu_radio.isChecked():
            self.kinect = acquisitionKinect.AcquisitionKinect()
        if self.ui.kinect_imu_radio.isChecked() or self.ui.imu_radio.isChecked():
            numIMU = self.ui.numIMUBox.value()
            for ni in xrange(numIMU):
                if self.ui.default_config.isChecked():
                    auto_calib = False
                    imu = acquisitionIMU.AcquisitionIMU(auto_calib=auto_calib)
                else:
                    # TODO: mettere possibilita load calibration e save calibration
                    auto_calib = str(self.ui.calib_box.currentText())
                    if auto_calib == "Auto":
                        auto_calib = True
                    else:
                        auto_calib = False

                    port = ""
                    if ni == 0:
                        port = str(self.ui.head_device_box.currentText())
                    elif ni == 1:
                        port = str(self.ui.shoulder_device_box.currentText())

                    imu = acquisitionIMU.AcquisitionIMU(
                        port=port,
                        save_conf=str(self.ui.save_box.currentText())=="True",
                        auto_calib=auto_calib,
                        accelerometer=str(self.ui.accel_box.currentText()),
                        gyro=str(self.ui.gyro_box.currentText()),
                        algo=str(self.ui.algo_box.currentText()),
                        sample_rate=str(self.ui.rate_box.currentText()),
                        frameType=ni
                    )
                if auto_calib:
                    msg = QtGui.QMessageBox()
                    msg.setIcon(QtGui.QMessageBox.Information)
                    msg.setText("IMU calibration is going to be performed")
                    msg.setInformativeText("Keep your head as still as possible")
                    msg.setWindowTitle("Calibration")
                    msg.setStandardButtons(QtGui.QMessageBox.Ok)
                    msg.exec_()
                imu.run()
                self.imu.append(imu)
        self.ui.sensor_label.setText("Connection established!")

        if self.ui.save_radio.isChecked():
            self.saveForm = saveForm(IMU=not self.ui.kinect_radio.isChecked())
            self.saveForm.setParent(self.ui.widget)
            self.saveForm.show()
            self.ui.widget.setVisible(True)
            self.connect(self.saveForm, QtCore.SIGNAL('calibrationRequest()'), self.calibration)
        if self.ui.test_radio.isChecked():
            self.testForm = testForm()
            self.testForm.setParent(self.ui.widget)
            self.testForm.show()
            self.ui.widget.setVisible(True)
            self.connect(self.testForm, QtCore.SIGNAL('calibrationRequest()'), self.calibration)

        self.timer.start(40)
        self.t_fps.start(500)

    def updateFPS(self):
        fps = self.fps / 0.500
        self.ui.labelFPS.setText("%.2f" % fps)
        self.fps = 0

    def resetGUI(self):
        image = np.zeros((self.ui.RGB_label.size().width(),self.ui.RGB_label.size().height()))
        image = QtGui.QImage(image, image.shape[1],image.shape[0], image.shape[1], QtGui.QImage.Format_Indexed8)

        pix = QtGui.QPixmap(image).scaled(self.ui.Depth_label.size())
        self.ui.Depth_label.setPixmap(pix)

        pix = QtGui.QPixmap(image).scaled(self.ui.RGB_label.size())
        self.ui.RGB_label.setPixmap(pix)

        self.ui.mainframe.hide()

    def resetHome(self):
        self.frame = frameSet()
        if self.saveForm is not None:
            if self.saveForm.process is not None:
                self.saveForm.process.kill()
                self.saveForm.process = None
            self.saveForm.close()
            self.saveForm = None

        if self.testForm is not None:
            self.testForm.close()
            self.testForm = None

        if self.kinect is not None:
            self.kinect.close()
            self.kinect = None

        # if self.imu is not None:
        #     self.imu.close()
        #     self.imu = None
        if len(self.imu) > 0:
            for imu in self.imu:
                imu.close()
            self.imu = []

        self.resetGUI()
        self.ui.mainframe.show()

    def checkChanged(self):
        if self.ui.kinect_imu_radio.isChecked() or self.ui.imu_radio.isChecked():
            self.ui.imu_settings_box.setEnabled(True)
        elif not self.ui.kinect_imu_radio.isChecked() and not self.ui.imu_radio.isChecked():
            self.ui.imu_settings_box.setEnabled(False)

        if (self.ui.save_radio.isChecked() or self.ui.test_radio.isChecked()) and (self.ui.kinect_imu_radio.isChecked() or self.ui.imu_radio.isChecked() or self.ui.kinect_radio.isChecked()):
            self.ui.start_btn.setEnabled(True)
        else:
            self.ui.start_btn.setEnabled(False)

    def configChecked(self):
        if self.ui.default_config.isChecked():
            self.ui.frame_settings.setEnabled(False)
        else:
            self.ui.frame_settings.setEnabled(True)

    def acquireFrame(self):
        self.frame = frameSet()
        if self.kinect is not None:
            self.kinect.get_frame(self.frame)

        # if self.imu is not None:
        if len(self.imu) > 0:
            for nimu, imu in enumerate(self.imu):
                imu.get_frame(self.frame)
                if self.calib[nimu]:
                    self.emit(QtCore.SIGNAL('calibFrameAcquired()'))
                    if imu.calibrate(self.frame):
                        self.emit(QtCore.SIGNAL('calibFrameEnded()'))
                        self.calib[nimu] = False

        if self.saveForm is not None:
            self.saveForm.saveFrame(self.frame)

        if self.testForm is not None:
            self.testForm.showFrame(self.frame)

        self.updateUI()

    def updateUI(self):
        if self.frame.frameRGB is not None:
            image = cv2.cvtColor(self.frame.frameRGB, cv2.COLOR_BGRA2RGB)
            # image = self.frame.frameRGB
        else:
            image = np.zeros((self.ui.RGB_label.size().width(),self.ui.RGB_label.size().height(),3))
        image = QtGui.QImage(image, image.shape[1],image.shape[0], image.shape[1] * 3, QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap(image).scaled(self.ui.RGB_label.size())
        self.ui.RGB_label.setPixmap(pix)

        if self.frame.frameDepthQuantized is not None:
            image = cv2.cvtColor(self.frame.frameDepthQuantized, cv2.COLOR_GRAY2RGB)
            self.fps += 1
            if self.ui.save_radio.isChecked():
                if self.frame.body_tracked:
                    calibMatrix = np.array([[391.096, 0,  243.892],
                                            [0, 463.098, 208.922],
                                            [0, 0, 1]])
                    headCenter = self.frame.bodyJoints[3]
                    shoulderRightJoint = self.frame.bodyJoints[4]
                    shoulderLeftJoint = self.frame.bodyJoints[8]
                    R = 250.0
                    Z = self.frame.frameDepthQuantized[int(headCenter.y), int(headCenter.x)] * 8 + 500
                    w = int(calibMatrix[0, 0] * R / Z)
                    h = int(calibMatrix[1, 1] * R / Z)
                    x1 = int(headCenter.x - w / 2)
                    y1 = int(headCenter.y - h / 2)
                    x2 = int(headCenter.x + w / 2)
                    y2 = int(headCenter.y + h / 2)
                    cv2.circle(image, (int(headCenter.x), int(headCenter.y)), 7, (0,255,0), -1)
                    cv2.circle(image, (int(shoulderRightJoint.x), int(shoulderRightJoint.y)), 7, (127, 0, 127), -1)
                    cv2.circle(image, (int(shoulderLeftJoint.x), int(shoulderLeftJoint.y)), 7, (127, 0, 127), -1)
                else:
                    h,w = image.shape[0:2]
                    x1 = int(w/2 - w/10)
                    y1 = int(h/2 - h/7)
                    x2 = int(w/2 + w/10)
                    y2 = int(h/2 + h/8)
                cv2.rectangle(image, (x1,y1), (x2,y2), (255,0,0), 2)
        else:
            image = np.zeros((self.ui.Depth_label.size().width(),self.ui.Depth_label.size().height(),3))
        image = QtGui.QImage(image, image.shape[1],image.shape[0], image.shape[1]*3, QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap(image).scaled(self.ui.Depth_label.size())
        self.ui.Depth_label.setPixmap(pix)

        # self.timer.start(30)

