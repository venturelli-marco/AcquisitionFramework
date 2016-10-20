import matplotlib.pyplot as plt
import numpy as np
import json
from operator import itemgetter

filepath = "sens_data/0.txt"
myo_filepath = "D:/Marco/GRFramework/gestures/data/default_name_myo.json"

try:
    data = np.loadtxt(filepath)
except:
    lines = open(filepath).readlines()
    open(filepath, 'w').writelines(lines[:-1])
    data = np.loadtxt(filepath)


with open(myo_filepath) as data_file:
    myo_data = json.load(data_file)

np_diff = np.array([])
np_myo = np.array([])
np_imu = np.array([])


for key, val in myo_data.items():
    diff = abs(data[:,0] - val['ts'])
    IMU_val = data[np.argmin(diff)]

    myo_data[key]['IMU_ts'] = IMU_val[0]

    myo_data[key]['IMU_quat'] = {
        "w": IMU_val[11],
        "x": IMU_val[12],
        "y": IMU_val[13],
        "z": IMU_val[14]
    }

    myo_data[key]['IMU_euler'] = {
        "roll": IMU_val[15],
        "pitch": IMU_val[16],
        "yaw": IMU_val[17]
    }

    diff_w = abs(val['quaternion']['w'] - IMU_val[11])
    diff_x = abs(val['quaternion']['x'] - IMU_val[12])
    diff_y = abs(val['quaternion']['y'] - IMU_val[13])
    diff_z = abs(val['quaternion']['z'] - IMU_val[14])

    diff_r = abs(val['euler']['pitch'] - IMU_val[17])
    diff_p = abs(val['euler']['roll'] - IMU_val[16])
    diff_a = abs(val['euler']['yaw'] - IMU_val[15])

    if len(np_diff) == 0:
        np_diff = np.array([key,diff_x,diff_y,diff_z,diff_w,diff_r,diff_p,diff_a])
        np_imu = np.array([key, IMU_val[11],IMU_val[12],IMU_val[13],IMU_val[14],IMU_val[15],IMU_val[16],IMU_val[17]])
        np_myo = np.array([key,val['quaternion']['w'],val['quaternion']['x'],val['quaternion']['y'],val['quaternion']['z'],val['euler']['pitch'],val['euler']['roll'],val['euler']['yaw']])
    else:
        np_diff = np.vstack((np_diff, np.array([key,diff_x,diff_y,diff_z,diff_w,diff_r,diff_p,diff_a])))
        np_imu = np.vstack((np_imu, np.array([key, IMU_val[11],IMU_val[12],IMU_val[13],IMU_val[14],IMU_val[15],IMU_val[16],IMU_val[17]])))
        np_myo = np.vstack((np_myo, np.array([key, val['quaternion']['w'],val['quaternion']['x'],val['quaternion']['y'],val['quaternion']['z'],val['euler']['pitch'],val['euler']['roll'],val['euler']['yaw']])))


with open(myo_filepath, "w") as data_file:
    json.dump(myo_data, data_file, indent=2, sort_keys=True)

np_diff = np.array(sorted(np_diff, key=itemgetter(0)))
np_myo = np.array(sorted(np_myo, key=itemgetter(0)))
np_imu = np.array(sorted(np_imu, key=itemgetter(0)))


plt.figure(1)

plt.subplot(611)
plt.title('diff quaternion')
plt.plot(np_diff[:,0], np_diff[:,1], 'r', np_diff[:,0], np_diff[:,2], 'g', np_diff[:,0], np_diff[:,3], 'b', np_diff[:,0], np_diff[:,4], 'y')

plt.subplot(612)
plt.title('diff euler')
plt.plot(np_diff[:,0], np_diff[:,5], 'r', np_diff[:,0], np_diff[:,6], 'g', np_diff[:,0], np_diff[:,7], 'b')


plt.subplot(613)
plt.title('MYO orientation quaternion')
plt.plot(np_myo[:,0], np_myo[:,1], 'r', np_myo[:,0], np_myo[:,2], 'g', np_myo[:,0], np_myo[:,3], 'b', np_myo[:,0], np_myo[:,4], 'y')

plt.subplot(615)
plt.title('MYO orientation euler')
plt.plot(np_myo[:,0], np_myo[:,5], 'r', np_myo[:,0], np_myo[:,6], 'g', np_myo[:,0], np_myo[:,7], 'b')


plt.subplot(614)
plt.title('IMU orientation quaternion')
plt.plot(np_imu[:,0], np_imu[:,1], 'r', np_imu[:,0], np_imu[:,2], 'g', np_imu[:,0], np_imu[:,3], 'b', np_imu[:,0], np_imu[:,4], 'y')
# plt.plot(data[:,1], data[:,11], 'r', data[:,1], data[:,12], 'g', data[:,1], data[:,13], 'b', data[:,1], data[:,14], 'y')

plt.subplot(616)
plt.title('IMU orientation euler')
plt.plot(np_imu[:,0], np_imu[:,5], 'r', np_imu[:,0], np_imu[:,6], 'g', np_imu[:,0], np_imu[:,7], 'b')
# plt.plot(data[:,1], data[:,15], 'r', data[:,1], data[:,16], 'g', data[:,1], data[:,17], 'b')



plt.show()
