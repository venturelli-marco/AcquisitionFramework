import os
import json
import glob
import time

from PyQt4 import QtGui, QtCore
from subprocess import Popen

import numpy as np
import cv2

from gui.saveWidget import Ui_saveWidget
from model.frameSet import frameSet, BASE_DIR
from utility.plot import plot_orientation
from saveThread import SaveThread
import Queue

MAX_SAVE_WINDOW = 2500
SEMAPHORE_PATH = 'AlignmentSemaphore/TestKinectFace.exe'

class saveForm(QtGui.QWidget):
    def __init__(self, parent=None, IMU=False):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_saveWidget()
        self.ui.setupUi(self)

        self.acquisition = False

        self.frame_num = 0

        self.frame = None
        self.frames = []

        self.save_dir = ""

        self.f_json = None
        self.f_txt = None
        self.l_json = {}

        self.saveThread = None
        self.saveQueue = Queue.Queue(MAX_SAVE_WINDOW)

        self.stopExtract = False

        # self.ui.calibButton.setVisible(False)
        self.ui.calibButton.clicked.connect(self.startCalibration)

        self.ui.buttonStart.clicked.connect(self.startAcquisition)
        self.ui.buttonStop.clicked.connect(self.stopAcquisition)
        self.ui.getBackgroundButton.clicked.connect(self.getBackround)

        self.connect(self, QtCore.SIGNAL('frameAcquired()'), self.updateProgressBar)
        self.connect(self, QtCore.SIGNAL('stopAcquisition()'), self.stopSaving)
        self.connect(self, QtCore.SIGNAL('saving()'), self.updateSaveProgressBar)

        # self.connect(self, QtCore.SIGNAL('stopCalibration()'), self.stopCalibration)

        self.ui.thresholdSlider.valueChanged.connect(self.updatePreview)
        self.ui.buttonStart_2.clicked.connect(self.updateFaceROI)
        self.ui.buttonStop_2.clicked.connect(self.stopExtractRoi)

        self.ui.calibButton.setEnabled(IMU)

        self.process = Popen([SEMAPHORE_PATH])

    def startCalibration(self):
        self.emit(QtCore.SIGNAL('calibrationRequest()'))

    def startAcquisition(self):
        if self.process is not None:
            self.process.kill()
            self.process = None

        if len(self.ui.textFilename.text()) > 0:
            self.acquisition = True
            self.frame_num = 0
        else:
            msg = QtGui.QMessageBox()
            msg.setIcon(QtGui.QMessageBox.Critical)
            msg.setText("Please insert a name for destination directory")
            msg.setInformativeText("In order to save acquired frames, you have to type a name for destination folder")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QtGui.QMessageBox.Ok)
            msg.exec_()
        self.ui.buttonStart.setDisabled(True)

    def stopAcquisition(self):
        self.acquisition = False
        if len(self.frames) > 0:
            self.save_frames(self.frames, self.ui.textFilename.text())
            self.frames = []
        if len(self.l_json) > 0:
            json.dump(self.l_json, self.f_json, indent=2,sort_keys=True)
            self.l_json = {}
            try:
                self.f_json.close()
                self.f_txt.close()
            except:
                pass
        if self.saveThread is not None:
            self.saveThread.stop()
            # self.saveQueue.queue.clear()
            self.saveThread = None
        self.resetProgressBar()
        self.emit(QtCore.SIGNAL('stopAcquisition()'))
        try:
            plot_orientation(self.save_dir+"/data.txt")
        except:
            pass

        self.ui.buttonStart.setDisabled(False)

        self.process = Popen([SEMAPHORE_PATH])

    def stopExtractRoi(self):
        self.stopExtract = True

    def saveFrame(self, frame):
        if not isinstance(frame, frameSet):
            raise TypeError("Given argument is not a frameSet")

        self.frame = frame

        if self.acquisition:
            if max(len(self.frames), self.frame_num) < MAX_SAVE_WINDOW:
                if self.ui.saveMethodCheck.isChecked():
                    # save during acquisition
                    # self.save_frame(frame,self.ui.textFilename.text())
                    self.save_frameThread(frame, self.ui.textFilename.text())
                else:
                    # save after stop
                    self.frames.append(frame)
                self.emit(QtCore.SIGNAL('frameAcquired()'))
            else:
                # reached max frame number
                self.stopAcquisition()

    def resetProgressBar(self):
        self.ui.progressBar.reset()
        self.ui.label_save.setText("Saving...")

    def stopSaving(self):
        # self.updateProgressBar()
        self.ui.progressBar.reset()
        self.ui.label_save.setText("Completed...")

    def updateProgressBar(self):
        self.ui.progressBar.setValue(max(len(self.frames), self.frame_num)*100/MAX_SAVE_WINDOW)
        self.ui.label_save.setText("")

    def updateSaveProgressBar(self):
        n = self.ui.progressBar.value()+1
        self.ui.progressBar.setValue(n*100/len(self.frames))

    def create_directories(self, dir_name):
        dir_name = BASE_DIR+"/"+str(dir_name)
        if os.path.isdir(dir_name):
            # raise OSError("Directory already exists")
            print "Directory already exists"
            try:
                for i in range(1,100):
                    if not os.path.isdir(dir_name+"({})".format(i)):
                        dir_name += "({})".format(i)
                        break
            except:
                raise OSError("Directory already exists")

        self.save_dir = dir_name
        os.mkdir(self.save_dir)
        os.mkdir(self.save_dir+"/RGB")
        os.mkdir(self.save_dir+"/DEPTH")
        # os.mkdir(self.save_dir+"/Skeleton")

    def save_frames(self, frames, dir_name):
        self.create_directories(dir_name)

        with open(self.save_dir+"/data.txt", "w") as f_txt, open(self.save_dir+"/data.json", "w") as f_json:
            l_json = {}
            # f_txt.write("\n")
            for i,f in enumerate(frames):
                f.frame_num = i
                l_json["%06d" % i] = f.to_json()
                f_txt.write(f.to_str()+"\n")
                f.save_img(self.save_dir)
                self.emit(QtCore.SIGNAL('saving()'))
            json.dump(l_json, f_json, indent=2, sort_keys=True)

    def save_frameReopenFile(self, frame, dir_name):
        if self.frame_num == 0:
            self.create_directories(dir_name)

        with open(self.save_dir+"/data.txt", "a") as f_txt:
            try:
                with open(self.save_dir+"/data.json", "r") as fr_json:
                    l_json = json.load(fr_json)
            except:
                l_json = {}
            # f_txt.write("\n")

            frame.frame_num = self.frame_num
            l_json["%06d" % self.frame_num] = frame.to_json()
            f_txt.write(frame.to_str()+"\n")
            frame.save_img(self.save_dir)

        with open(self.save_dir+"/data.json", "w") as f_json:
            json.dump(l_json, f_json, indent=2,sort_keys=True)

        self.frame_num += 1

    def save_frame(self, frame, dir_name):
        # TODO: fare versione con file mantenuti aperti
        if self.frame_num == 0:
            self.create_directories(dir_name)

        if self.f_txt is None:
            self.f_txt = open(self.save_dir+"/data.txt", "w")
        if self.f_json is None:
            self.f_json = open(self.save_dir+"/data.json", "w")

        frame.frame_num = self.frame_num
        self.l_json["%06d" % self.frame_num] = frame.to_json()
        self.f_txt.write(frame.to_str()+"\n")
        frame.save_img(self.save_dir)

        self.frame_num += 1

    def save_frameThread(self, frame, dir_name):
        if self.frame_num == 0:
            self.create_directories(dir_name)

        if self.saveThread is None:
            self.saveThread = SaveThread(self.saveQueue, self.save_dir)
            # self.saveThread.setDaemon()
            self.saveThread.start()

        frame.frame_num = self.frame_num

        # frame.save_img(self.save_dir)
        self.saveQueue.put(frame)

        self.frame_num += 1

    def updatePreview(self):
        self.ui.thLabel.setText("%d" % self.ui.thresholdSlider.value())
        try:
            files = glob.glob("data/" + str(self.ui.textFilename_2.text()) + "/DEPTH/" + "*.png")
        except:
            files = []
        if len(files) <= 0:
            return

        image = cv2.imread(files[0],0)
        h,w = image.shape
        x1 = self.ui.xBox.value()
        y1 = self.ui.yBox.value()
        x2 = x1 + self.ui.wBox.value()
        y2 = y1 + self.ui.hBox.value()

        if x1 == 0: x1 = int(w/2 - w/10);
        if y1 == 0: y1 = int(h/2 - h/7);
        if x2 == 0: x2 = int(w/2 + w/10);
        if y2 == 0: y2 = int(h/2 + h/8)

        face = image[y1:y2,x1:x2]

        th,mask = cv2.threshold(face,self.ui.thresholdSlider.value(),255, cv2.THRESH_BINARY_INV)
        face = cv2.bitwise_and(face,mask)

        face = QtGui.QImage(face, face.shape[1],face.shape[0], face.shape[1], QtGui.QImage.Format_Indexed8)
        pix = QtGui.QPixmap(face).scaled(self.ui.previewLabel.size())
        self.ui.previewLabel.setPixmap(pix)

    def getBackround(self):
        path = "data/" + str(self.ui.textFilename.text()) + "_background"
        cv2.imwrite(path+"RGB.png", self.frame.frameRGB)
        cv2.imwrite(path+"Depth.png", self.frame.frameDepth)


    def updateFaceROI(self):
        self.stopExtract = False
        try:
            files = glob.glob("data/" + str(self.ui.textFilename_2.text()) + "/DEPTH/" + "*.png")
        except:
            files = []
        if len(files) <= 0:
            return

        for f in files:
            if self.stopExtract:
                return
            image = cv2.imread(f,0)
            h,w = image.shape

            x1 = self.ui.xBox.value()
            y1 = self.ui.yBox.value()
            x2 = x1 + self.ui.wBox.value()
            y2 = y1 + self.ui.hBox.value()

            if x1 == 0: x1 = int(w/2 - w/10);
            if y1 == 0: y1 = int(h/2 - h/7);
            if x2 == 0: x2 = int(w/2 + w/10);
            if y2 == 0: y2 = int(h/2 + h/8)

            face = image[y1:y2,x1:x2]

            th,mask = cv2.threshold(face,self.ui.thresholdSlider.value(),255, cv2.THRESH_BINARY_INV)
            face_supp = cv2.bitwise_and(face,mask)

            face_norm = cv2.normalize(face_supp, None, 0, 255, cv2.NORM_MINMAX)
            face_eq = cv2.equalizeHist(face_supp)

            cv2.imshow("face", face)
            cv2.imshow("face background sup", face_supp)
            cv2.imshow("face norm", face_norm)
            cv2.imshow("face eq", face_eq)
            cv2.waitKey(1)

            face = QtGui.QImage(cv2.bitwise_and(face,np.ones_like(face)*255), face.shape[1],face.shape[0], face.shape[1], QtGui.QImage.Format_Indexed8)
            pix = QtGui.QPixmap(face).scaled(self.ui.faceLabel.size())
            self.ui.faceLabel.setPixmap(pix)

            face_supp = QtGui.QImage(face_supp, face_supp.shape[1],face_supp.shape[0], face_supp.shape[1], QtGui.QImage.Format_Indexed8)
            pix = QtGui.QPixmap(face_supp).scaled(self.ui.faceBSLabel.size())
            self.ui.faceBSLabel.setPixmap(pix)

            face_norm = QtGui.QImage(face_norm, face_norm.shape[1],face_norm.shape[0], face_norm.shape[1], QtGui.QImage.Format_Indexed8)
            pix = QtGui.QPixmap(face_norm).scaled(self.ui.faceNormLabel.size())
            self.ui.faceNormLabel.setPixmap(pix)

            face_eq = QtGui.QImage(face_eq, face_eq.shape[1],face_eq.shape[0], face_eq.shape[1], QtGui.QImage.Format_Indexed8)
            pix = QtGui.QPixmap(face_eq).scaled(self.ui.faceEqLabel.size())
            self.ui.faceEqLabel.setPixmap(pix)

