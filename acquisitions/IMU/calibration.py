import numpy as np
from math import asin, atan2, pi

CALIBRATION_FRAMES = 100

class IMU_calibration():
    def __init__(self, calibration_sample=CALIBRATION_FRAMES):
        self.calibration_sample = calibration_sample
        self.calib_step = 0

        self.first_rot = np.array([0.0, 0.0, 0.0, 0.0])
        self.average = np.array([0.0, 0.0, 0.0, 0.0])
        self.cumulative = np.array([0.0, 0.0, 0.0, 0.0])

    def quat_product(self, q1, q2):
        x = q1[0] * q2[1] + q1[1] * q2[0] + q1[2] * q2[3] - q1[3] * q2[2]
        y = q1[0] * q2[2] - q1[1] * q2[3] + q1[2] * q2[0] + q1[3] * q2[1]
        z = q1[0] * q2[3] + q1[1] * q2[2] - q1[2] * q2[1] + q1[3] * q2[0]
        w = q1[0] * q2[0] - q1[1] * q2[1] - q1[2] * q2[2] - q1[3] * q2[3]

        return np.array([w,x,y,z])

    def calibrate(self, quat_read):
        self.calib_step += 1
        if (self.calib_step == 1):
            self.first_rot = quat_read
        elif self.calib_step < self.calibration_sample:
            self.AverageQuaternion(quat_read)
        else:
            if self.calib_step >= self.calibration_sample:
                # return self.average
                return self.get_quat_calibrated(quat_read)
        return None

    def get_quat_calibrated(self, quat_read):
        # quat_read = np.array([Q0,Q1,Q2,Q3])
        quat = self.average * np.array([1.0, -1.0, -1.0, -1.0]) # coniugate
        quat = quat / np.linalg.norm(quat)
        quat = self.quat_product(quat,quat_read)
        Q0, Q1, Q2, Q3 = quat[0], quat[1], quat[2], quat[3]
        return np.array([Q0,Q1,Q2,Q3])

    def AverageQuaternion(self, newRotation):

        new_rot = newRotation

        if not self.AreQuaternionsClose(newRotation, self.first_rot):
            new_rot = new_rot * -1.0

        addDet = 1.0 / self.calib_step

        self.cumulative = self.cumulative + new_rot
        self.average = self.cumulative * addDet

        self.average = self.average / np.linalg.norm(self.average)

    def AreQuaternionsClose(self, q1, q2):
        dot = q1[0] * q2[0] + q1[1] * q2[1] + q1[2] * q2[2] + q1[3] * q2[3]

        if dot < 0.0:
            return False
        else:
            return True

    @staticmethod
    def quaternion_to_euler(qw, qx, qy, qz):
        test = qx * qy + qz * qw
        if test > 0.499:
            roll = 2.0 * atan2(qx, qw)
            pitch = pi / 2.0
            yaw = 0.0
        elif test < -0.499:
            roll = -2.0 * atan2(qx, qw)
            pitch = - pi / 2.0
            yaw = 0.0
        else:
            roll = atan2(2 * qy * qw - 2 * qx * qz, 1 - 2 * (qy ** 2) - 2 * (qz ** 2))
            pitch = asin(2 * qx * qy + 2 * qz * qw)
            yaw = atan2(2 * qx * qw - 2 * qy * qz, 1 - 2 * (qx ** 2) - 2 * (qz ** 2))

        roll *= 180 / pi
        pitch *= 180 / pi
        yaw *= 180 / pi

        return roll, pitch, yaw