from __future__ import print_function
import serial
import datetime
import time
from operator import mod
from math import asin, atan2
import numpy as np
from math import pi
import json
import pickle as pkl

JSON_config = "IMU_parameters.json"

class Cupid:
    def twos_comp(self, val, bits):
        """compute the 2's compliment of int value val"""
        if (val & (1 << (bits - 1))) != 0:  # if sign bit is set e.g., 8bit: 128-255
            val = val - (1 << bits)  # compute negative value
        return val

    def start_ser(self):
        cont = 0
        while self.ser.inWaiting() == 0 & cont < 100:
            self.ser.write('=')
            self.ser.write('=')
            cont += 1

        assert self.ser.inWaiting() > 0

    def stop_ser(self):
        self.ser.write(':')
        self.ser.write(':')

    def somma_hex(self, byte):
        s = 0
        for i in range(0, len(byte) - 1, 2):
            s += int(byte[i:i + 2], 16)

    # def sum_hex_byte_mod_256(self, hex_byte):
    #     s = 0
    #     byte = [int(a, 16) for a in hex_byte]
    #     for i in xrange(len(byte)):
    #         s += byte[i]
    #     s = mod(s, 256)
    #     return s

    def calc_checksum(self, hex_byte):
        """

        :param byte: hex encoded data
        :return:
        """
        return self.sum_pkt_mod_256(hex_byte)

    def sum_pkt_mod_256(self, str_pkt):
        s = 0

        for i in range(0, len(str_pkt), 2):
            s += int(str_pkt[i:i + 2], 16)

        return mod(s, 256)

    def xor(self, i1, s2):
        return i1 ^ int(s2, 16)

    def xor_hex(self, str):

        x = int(str[0:2], 16)

        for i in range(2, len(str) - 1, 2):
            x = self.xor(x, str[i:i + 2])

        return hex(x)[2:4]

    def get_pkt(self):
        # ser.flushInput()

        state = 0
        err_count = 0
        byte = 0

        while err_count < 100:

            if state == 0:
                byte = self.ser.read(1)
                err_count += 1
                if hex(ord(byte)) == "0x20":
                    state = 1

            elif state == 1:
                byte = self.ser.read(1)
                if hex(ord(byte)) == "0x9f":
                    state = 2
                elif hex(ord(byte)) != "0x20" and hex(ord(byte)) != "0x9f":
                    state = 0

            elif state == 2:
                byte = self.ser.read(31)  # leggo i restanti 31 byte (dal 2 al 32)

                check = self.calc_checksum('209f' + byte[0:30].encode("hex"))

                if int(byte[-1:].encode("hex"),16) != check:
                    print("Checksum failed, discarding packet")
                    state = 0
                else:
                    return byte

        return -1

    def get_pkt_data(self, data_raw):
        if self.calib_step ==0 and not self.is_calibrate:
            print("Started getting calibration data from pkt")
            print("Keep your head still")
            print("[",end="")
        elif not self.is_calibrate:
            if self.calib_step % 10 == 0:
                print("=", end="")
        elif self.calib_step==500:
            print("Started getting data from pkt")
            self.calib_step += 1
            print("[",end="")
        else:
            if self.calib_step % 100 == 0:
                print("=", end="")
            self.calib_step += 1

        # print data_raw
        data_raw = data_raw.encode('hex')

        pkCount_L = data_raw[0:2]
        pkCount_H = data_raw[2:4]
        pkCount = int(pkCount_H + pkCount_L, 16)  # + is not a sum but a concatenation

        # Accelerometer data
        AccX_L = data_raw[4:6]
        AccX_H = data_raw[6:8]
        AccX = self.twos_comp(int(AccX_H + AccX_L, 16), 16)
        AccX = self.config["conversion"]["acceleration"][self.accel] * AccX / self.config["conversion"]["acceleration"]["k_norm"]

        AccY_L = data_raw[8:10]
        AccY_H = data_raw[10:12]
        AccY = self.twos_comp(int(AccY_H + AccY_L, 16), 16)
        AccY = self.config["conversion"]["acceleration"][self.accel] * AccY / self.config["conversion"]["acceleration"]["k_norm"]

        AccZ_L = data_raw[12:14]
        AccZ_H = data_raw[14:16]
        AccZ = self.twos_comp(int(AccZ_H + AccZ_L, 16), 16)
        AccZ = self.config["conversion"]["acceleration"][self.accel] * AccZ / self.config["conversion"]["acceleration"]["k_norm"]

        # Gyroscope data
        GyrX_L = data_raw[16:18]
        GyrX_H = data_raw[18:20]
        GyrX = self.twos_comp(int(GyrX_H + GyrX_L, 16), 16)
        GyrX = self.config["conversion"]["angular_velocity"][self.gyro] * GyrX / self.config["conversion"]["angular_velocity"]["k_norm"]

        GyrY_L = data_raw[20:22]
        GyrY_H = data_raw[22:24]
        GyrY = self.twos_comp(int(GyrY_H + GyrY_L, 16), 16)
        GyrY = self.config["conversion"]["angular_velocity"][self.gyro] * GyrY / self.config["conversion"]["angular_velocity"]["k_norm"]

        GyrZ_L = data_raw[24:26]
        GyrZ_H = data_raw[26:28]
        GyrZ = self.twos_comp(int(GyrZ_H + GyrZ_L, 16), 16)
        GyrZ = self.config["conversion"]["angular_velocity"][self.gyro] * GyrZ / self.config["conversion"]["angular_velocity"]["k_norm"]

        # Magnetic Field data
        MagX_L = data_raw[28:30]
        MagX_H = data_raw[30:32]
        MagX = self.twos_comp(int(MagX_H + MagX_L, 16), 16) * self.config["conversion"]["magnetic_field"]["k_norm"]

        MagY_L = data_raw[32:34]
        MagY_H = data_raw[34:36]
        MagY = self.twos_comp(int(MagY_H + MagY_L, 16), 16) * self.config["conversion"]["magnetic_field"]["k_norm"]

        MagZ_L = data_raw[36:38]
        MagZ_H = data_raw[38:40]
        MagZ = self.twos_comp(int(MagZ_H + MagZ_L, 16), 16) * self.config["conversion"]["magnetic_field"]["k_norm"]

        # q0q1q2q3 = wxyz

        Q0_L = data_raw[40:42]
        Q0_H = data_raw[42:44]
        Q0 = self.twos_comp(int(Q0_H + Q0_L, 16), 16) / self.config["conversion"]["orientation"]["k_norm"]

        Q1_L = data_raw[44:46]
        Q1_H = data_raw[46:48]
        Q1 = self.twos_comp(int(Q1_H + Q1_L, 16), 16) / self.config["conversion"]["orientation"]["k_norm"]

        Q2_L = data_raw[48:50]
        Q2_H = data_raw[50:52]
        Q2 = self.twos_comp(int(Q2_H + Q2_L, 16), 16) / self.config["conversion"]["orientation"]["k_norm"]

        Q3_L = data_raw[52:54]
        Q3_H = data_raw[54:56]
        Q3 = self.twos_comp(int(Q3_H + Q3_L, 16), 16) / self.config["conversion"]["orientation"]["k_norm"]

        V_BAT_L = data_raw[56:58]
        V_BAT_H = data_raw[58:60]
        V_BAT = int(V_BAT_H + V_BAT_L, 16)

        if not self.is_calibrate:
            self.calibrate(np.array([Q0, Q1, Q2, Q3]))

        if self.is_calibrate and self.auto_calib:
            quat_read = np.array([Q0,Q1,Q2,Q3])
            quat = self.average * np.array([1.0, -1.0, -1.0, -1.0]) # coniugate
            quat = quat / np.linalg.norm(quat)
            quat = self.quat_product(quat,quat_read)
            Q0, Q1, Q2, Q3 = quat[0], quat[1], quat[2], quat[3]

        roll, pitch, yaw = self.quaternion_to_euler(Q0, Q1, Q2, Q3)

        return pkCount, AccX, AccY, AccZ, GyrX, GyrY, GyrZ, MagX, MagY, MagZ, Q0, Q1, Q2, Q3, roll, pitch, yaw, V_BAT

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
        elif self.calib_step < 500:
            self.AverageQuaternion(quat_read)
        else:
            if self.calib_step == 500:
                self.is_calibrate = True
                print("]", end="\n")
                print("End Auto calibration")


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

    def quaternion_to_euler(self, qw, qx, qy, qz):

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

    def pkt_print(self, pkt):

        pkCount, AccX, AccY, AccZ, GyrX, GyrY, GyrZ, MagX, MagY, MagZ, Q0, Q1, Q2, Q3, roll, pitch, yaw, V_BAT = self.get_pkt_data(
            pkt)

        print("pkCount: " + `pkCount` + " Timestamp " + str(datetime.datetime.now()))
        print("\tACCELEROMETER DATA        (x,y,z): " + `AccX` + " " + `AccY` + " " + `AccZ`)
        print("\tGYROSCOPE DATA            (x,y,z): " + `GyrX` + " " + `GyrY` + " " + `GyrZ`)
        print("\tMAGNETOMETER DATA         (x,y,z): " + `MagX` + " " + `MagY` + " " + `MagZ`)
        print("\tORIENTATION DATA    (q0,q1,q2,q3): " + `Q0` + " " + `Q1` + " " + `Q2` + " " + `Q3`)
        print("\tORIENTATION DATA (roll,pitch,yaw): " + `roll` + " " + `pitch` + " " + `yaw`)

        # np_data = np.array(
        #     [pkCount, AccX, AccY, AccZ, GyrX, GyrY, GyrZ, MagX, MagY, MagZ, Q0, Q1, Q2, Q3, roll, pitch, yaw, V_BAT])
        # if len(self.data_ret) == 0:
        #     self.data_ret = np_data
        # else:
        #     self.data_ret = np.vstack((self.data_ret, np_data))

    def save_configuration(self):
        ack = "0x01"
        byte = '\x66'

        self.ser.flushInput()
        self.ser.write(byte+byte)
        r_ack = self.ser.read(1)
        if ord(r_ack) == int(ack,16):
            return True
        return False

    def send_configuration(self):
        ack = "0x01"

        for key, obj in self.config["configuration"].items():
            N_byte = 1
            # pkt = '\x64'+chr(N_byte)+'\x34\x00'+'\x03'
            pkt = '\x64'+chr(N_byte)

            add = chr(int(obj["address"]))

            val = '\x00'
            if key == "acceleration":
                val = chr(int(obj[self.accel]))
            elif key == "angular_velocity":
                val = chr(int(obj[self.gyro]))
            elif key == "sample_rate":
                val = chr(int(obj[self.sample_rate]))
            elif key == "orientation":
                val = chr(int(obj[self.algo]))

            pkt += add + '\x00' + val

            crc = self.calc_checksum(pkt.encode("hex"))
            pkt = pkt+chr(crc)

            # b_w = self.ser.write(pkt)
            # pkt = [ord(x) for x in pkt]
            self.ser.flushInput()
            self.ser.write(pkt)
            r_ack = self.ser.read(1)
            if ord(r_ack) != int(ack,16):
                return False
        return True

    def load_calibration(self, w, x, y, z):
        self.is_calibrate = True
        self.auto_calib = True
        self.average = np.array([w, x, y, z])
        print("Calibration loaded with success")
        return True

    def save_calibration(self, filename):
        with open(filename, "w") as fp:
            pkl.dump({
                "w": self.average[0],
                "x": self.average[1],
                "y": self.average[2],
                "z": self.average[3]
            }, fp)
        print("Calibration loaded with success")
        return True

    def __init__(self, port="COM7", save_conf=False, auto_calib = True,
                 accelerometer="4g", gyro="250dps", algo="kalman", sample_rate="100hz"):
        self.config = None
        try:
            with open(JSON_config) as conf_file:
                self.config = json.load(conf_file)
        except Exception as e:
            print("Failed to open configuration file, closing")
            print(e)
            raise e

        self.accel= accelerometer
        self.gyro = gyro
        self.algo = algo
        self.compass = "magnetic_field"
        self.sample_rate = sample_rate

        self.port = port

        self.auto_calib = auto_calib
        self.is_calibrate = not auto_calib

        self.calib_step = 0
        self.first_rot = np.array([0.0, 0.0, 0.0, 0.0])
        self.average = np.array([0.0, 0.0, 0.0, 0.0])
        self.cumulative = np.array([0.0, 0.0, 0.0, 0.0])

        # __init__(port=None, baudrate=9600, bytesize=EIGHTBITS, parity=PARITY_NONE, stopbits=STOPBITS_ONE, timeout=None, xonxoff=False, rtscts=False, writeTimeout=None, dsrdtr=False, interCharTimeout=None)
        self.ser = serial.Serial(port, 115200, timeout=5, xonxoff=False, rtscts=False, dsrdtr=False)
        self.ser.flushInput()
        self.ser.flushOutput()
        time.sleep(1.5)

        try:
            if not self.send_configuration():
                raise Exception("Something went wrong during configuration.")
            if save_conf:
                self.save_configuration()

            self.start_ser()

        except Exception as e:
            self.ser.close()
            print(e)
            print("Failed to send BT_START_stream, closing")
            raise e
