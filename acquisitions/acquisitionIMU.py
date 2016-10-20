from acquisition import Acquisition
import Queue
from IMU import CupidThread, calibration
import numpy as np
from matplotlib import pyplot as plt, animation
import time

class real_time_plot():

    def __init__(self,q):
        self.ax = np.array([])
        self.q = q

    def update(self, frameNum, a0, a1, a2):
        try:
            line = self.q.get()
            # data = [float(val) for val in line.split()]
            data = line

            if len(self.ax)==0:
                self.ax = data
            else:
                self.ax = np.vstack((self.ax, data))

            # print data
            a0.set_data(self.ax[:,0], self.ax[:,15])
            a1.set_data(self.ax[:,0], self.ax[:,16])
            a2.set_data(self.ax[:,0], self.ax[:,17])

        except KeyboardInterrupt:
            print('exiting')

        return a0,

class AcquisitionIMU(Acquisition):

    def __init__(self, port="COM7", save_conf=False, auto_calib = True,
                 accelerometer="4g", gyro="500dps", algo="kalman", sample_rate="100hz", frameType=0): # HEAD frameType = 0
                                                                                                      # SHOULDER frameType = 1
        self.q = Queue.LifoQueue()

        # vt = VideoThread.VideoThread(q)
        self.ct = CupidThread.CupidThread(self.q, port, save_conf, auto_calib, accelerometer, gyro, algo, sample_rate)

        self.calib_obj = None
        self.isCalibrate = False
        self.frameType = frameType

    def run(self):
        self.ct.start()
        print "Started cupid thread, waiting a bit"

    def close(self):
        self.ct.stop()

    def _get_frame(self, frame):
        line = self.q.get()
        # if not self.isCalibrate:
        #     frame.orientation_euler = {
        #         "roll": line[0,14],
        #         "pitch": line[0,15],
        #         "yaw": line[0,16]
        #     }
        #     frame.orientation_quat = line[0,10:14]
        # else:
        #     frame.orientation_quat = self.calib_obj.calibrate(line[0,10:14])
        #     roll, pitch, yaw = calibration.IMU_calibration.quaternion_to_euler(
        #         frame.orientation_quat[0],
        #         frame.orientation_quat[1],
        #         frame.orientation_quat[2],
        #         frame.orientation_quat[3])
        #     frame.orientation_euler = {
        #         "roll": roll,
        #         "pitch": pitch,
        #         "yaw": yaw
        #     }
        if not self.isCalibrate:
            frame_eul = {
                "roll": line[0,14],
                "pitch": line[0,15],
                "yaw": line[0,16]
            }
            frame_quat = line[0,10:14]
        else:
            frame_quat = self.calib_obj.calibrate(line[0,10:14])
            roll, pitch, yaw = calibration.IMU_calibration.quaternion_to_euler(
                frame_quat[0],
                frame_quat[1],
                frame_quat[2],
                frame_quat[3])
            frame_eul = {
                "roll": roll,
                "pitch": pitch,
                "yaw": yaw
            }

        if self.frameType == 0:
            frame.orientation_euler = frame_eul
            frame.orientation_quat = frame_quat
        elif self.frameType == 1:
            frame.shoulder_orientation_euler = frame_eul
            frame.shoulder_orientation_quat = frame_quat


    def calibrate(self, frame):
        if self.calib_obj is None:
            self.calib_obj = calibration.IMU_calibration()
        # line = self.q.get()
        # orientation_quat = line[0,10:14]
        # orientation_quat = frame.orientation_quat

        if self.frameType == 0:
            orientation_quat = frame.orientation_quat
        elif self.frameType == 1:
            orientation_quat = frame.shoulder_orientation_quat

        res = self.calib_obj.calibrate(orientation_quat)
        if res is not None:
            self.isCalibrate = True

        return self.isCalibrate



def test():
    imu = AcquisitionIMU()
    imu.run()

    # print('plotting data...')
    # rp = real_time_plot(imu.q)
    #
    #
    # # set up animation
    # fig = plt.figure()
    # ax = plt.axes(xlim=(0, 10000), ylim=(-180, 180))
    # a0, = ax.plot([], [])
    # a1, = ax.plot([], [])
    # a2, = ax.plot([], [])
    #
    # anim = animation.FuncAnimation(fig, rp.update,
    #                              fargs=(a0, a1, a2),
    #                              interval=50)
    # # show plot
    # plt.show()
    #
    # # wait for the end of the world
    # while True:
    #     time.sleep(0.05)

