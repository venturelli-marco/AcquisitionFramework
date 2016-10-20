from PyQt4 import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot

from gui.testWidget import Ui_testWidget
from model.frameSet import frameSet

MAX_PLOT_WINDOW = 1000

class testForm(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_testWidget()
        self.ui.setupUi(self)

        self.data = np.array([0, 0.0, 0.0, 0.0])
        self.shoulder_data = np.array([0, 0.0, 0.0, 0.0])
        self.nn = 0

        self.pltW = pg.PlotWidget(self.ui.rot_chart)
        self.pltW.showMaximized()
        self.pltW.setMinimumSize(QtCore.QSize(800,175))
        self.pltW.setYRange(-180,180)
        self.pltW.setXRange(0,MAX_PLOT_WINDOW)
        self.pltW.plotItem.showGrid(True, True)
        self.pltW.plotItem.addLegend()
        self.pltW.plotItem.plot(x=[self.data[0]], y=[self.data[1]], pen=(0,3), name="roll")
        self.pltW.plotItem.plot(x=[self.data[0]], y=[self.data[2]], pen=(1,3), name="pitch")
        self.pltW.plotItem.plot(x=[self.data[0]], y=[self.data[3]], pen=(2,3), name="yaw")

        self.pltW_shoulder = pg.PlotWidget(self.ui.rot_chart_2)
        self.pltW_shoulder.showMaximized()
        self.pltW_shoulder.setMinimumSize(QtCore.QSize(800, 175))
        self.pltW_shoulder.setYRange(-180, 180)
        self.pltW_shoulder.setXRange(0, MAX_PLOT_WINDOW)
        self.pltW_shoulder.plotItem.showGrid(True, True)
        self.pltW_shoulder.plotItem.addLegend()
        self.pltW_shoulder.plotItem.plot(x=[self.data[0]], y=[self.data[1]], pen=(0, 3), name="roll")
        self.pltW_shoulder.plotItem.plot(x=[self.data[0]], y=[self.data[2]], pen=(1, 3), name="pitch")
        self.pltW_shoulder.plotItem.plot(x=[self.data[0]], y=[self.data[3]], pen=(2, 3), name="yaw")


        # self.view = gl.GLViewWidget(self.ui.frame_GL)
        # self.view = gl.GLViewWidget()
        # self.view.setMinimumSize(QtCore.QSize(400, 300))
        # self.view.setMaximumSize(QtCore.QSize(400, 300))
        # self.view.show()
        #
        # ## create three grids, add each to the view
        # # self.xgrid = gl.GLGridItem()
        # # self.view.addItem(self.xgrid)
        #
        # vertex,_ = self.loadOBJ("resources/face.obj")
        # vertex = np.array(vertex)
        # self.face = gl.GLScatterPlotItem(pos=vertex, color=pg.glColor('w'), size=2)
        # self.view.addItem(self.face)

        ## rotate x and y grids to face the correct direction
        # self.face.rotate(60, 0, 0, 1)
        # self.face.rotate(45, 1, 0, 0)
        # self.face.rotate(-90, 0, 1, 0)
        # self.face.rotate(-25, 0, 1, 0)
        # ## scale each grid differently
        # self.face.scale(0.03, 0.03, 0.03)

        self.lastFrameYaw = None
        self.lastFrameRoll = None
        self.lastFramePitch = None

        self.ui.calibButton.clicked.connect(self.startCalibration)

    def startCalibration(self):
        self.emit(QtCore.SIGNAL('calibrationRequest()'))

    def showFrame(self, frame):
        if not isinstance(frame, frameSet):
            raise TypeError("Given argument is not a frameSet")

        self.nn += 1
        if self.nn % 3 == 0:
            return

        if self.data.shape[0] >= MAX_PLOT_WINDOW:
            self.pltW.plotItem.clear()
            self.data = self.data[-1,:]
            self.data[0] = 0
            self.pltW_shoulder.plotItem.clear()
            self.shoulder_data = self.shoulder_data[-1, :]
            self.shoulder_data[0] = 0

        self.data = np.vstack((self.data, np.array([self.data.shape[0], frame.orientation_euler["roll"], frame.orientation_euler["pitch"], frame.orientation_euler["yaw"]])))
        self.pltW.plotItem.plot(self.data[:,0], self.data[:,1], pen=(0,3))
        self.pltW.plotItem.plot(self.data[:,0], self.data[:,2], pen=(1,3))
        self.pltW.plotItem.plot(self.data[:,0], self.data[:,3], pen=(2,3))

        self.shoulder_data = np.vstack((self.shoulder_data, np.array(
            [self.shoulder_data.shape[0], frame.shoulder_orientation_euler["roll"], frame.shoulder_orientation_euler["pitch"],
             frame.shoulder_orientation_euler["yaw"]])))
        self.pltW_shoulder.plotItem.plot(self.shoulder_data[:, 0], self.shoulder_data[:, 1], pen=(0, 3))
        self.pltW_shoulder.plotItem.plot(self.shoulder_data[:, 0], self.shoulder_data[:, 2], pen=(1, 3))
        self.pltW_shoulder.plotItem.plot(self.shoulder_data[:, 0], self.shoulder_data[:, 3], pen=(2, 3))

        # if self.lastFramePitch is not None:
        #     self.face.rotate(frame.orientation_euler["roll"]-self.lastFrameRoll, 0, 0, 1) # OK
        #     self.face.rotate(frame.orientation_euler["pitch"]-self.lastFramePitch, 0, 1, 0)
        #     self.face.rotate(frame.orientation_euler["yaw"]-self.lastFrameYaw, 1, 0, 0)
        #
        # self.lastFrameRoll = frame.orientation_euler["roll"]
        # self.lastFramePitch = frame.orientation_euler["pitch"]
        # self.lastFrameYaw = frame.orientation_euler["yaw"]

        if frame.frameSkeleton is not None:
            image = frame.frameSkeleton
        else:
            image = np.zeros((self.ui.labelSkeleton.size().width(),self.ui.labelSkeleton.size().height()))
        image = QtGui.QImage(image, image.shape[1],image.shape[0], image.shape[1], QtGui.QImage.Format_Indexed8)
        pix = QtGui.QPixmap(image).scaled(self.ui.labelSkeleton.size())
        self.ui.labelSkeleton.setPixmap(pix)

    def loadOBJ(self,filename):
        numVerts = 0
        verts = []
        norms = []
        vertsOut = []
        normsOut = []
        for line in open(filename, "r"):
            vals = line.split()
            if vals[0] == "v":
                v = map(float, vals[1:4])
                verts.append(v)
            if vals[0] == "vn":
                n = map(float, vals[1:4])
                norms.append(n)
            if vals[0] == "f":
                for f in vals[1:]:
                    w = f.split("/")
                    # OBJ Files are 1-indexed so we must subtract 1 below
                    vertsOut.append(list(verts[int(w[0])-1]))
                    normsOut.append(list(norms[int(w[2])-1]))
                    numVerts += 1
        return vertsOut, normsOut

