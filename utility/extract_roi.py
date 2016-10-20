import numpy as np
import cv2
import glob
import json
from operator import itemgetter


depth_filepath = ["D:/Marco/GRFramework/gestures/data/default_name_depth/",
                  "D:/Marco/GRFramework/gestures/data/default_name1_depth/",
                  "D:/Marco/GRFramework/gestures/data/default_name2_depth/",
                  "D:/Marco/GRFramework/gestures/data/default_name3_depth/",
                  "D:/Marco/GRFramework/gestures/data/default_name4_depth/",
                  "D:/Marco/GRFramework/gestures/data/default_name5_depth/",
                  "D:/Marco/GRFramework/gestures/data/default_name6_depth/",
                  "D:/Marco/GRFramework/gestures/data/default_name7_depth/",
                  "D:/Marco/GRFramework/gestures/data/default_name8_depth/"]

orientation_filepath = [  "D:/Marco/GRFramework/gestures/data/default_name_myo.json",
                          "D:/Marco/GRFramework/gestures/data/default_name1_myo.json",
                          "D:/Marco/GRFramework/gestures/data/default_name2_myo.json",
                          "D:/Marco/GRFramework/gestures/data/default_name3_myo.json",
                          "D:/Marco/GRFramework/gestures/data/default_name4_myo.json",
                          "D:/Marco/GRFramework/gestures/data/default_name5_myo.json",
                          "D:/Marco/GRFramework/gestures/data/default_name6_myo.json",
                          "D:/Marco/GRFramework/gestures/data/default_name7_myo.json",
                          "D:/Marco/GRFramework/gestures/data/default_name8_myo.json"]

# for f in orientation_filepath:
#     o_f = "{}_imu.txt".format(f[:-9])
#     print o_f
#     with open(f) as data_file, open(o_f, "w") as out_file:
#         imu_data = json.load(data_file)
#
#         l_out = []
#         for key, val in imu_data.items():
#             orien = "{}\t".format(key)
#             orien += "{}\t".format(val["IMU_euler"]["roll"])
#             orien += "{}\t".format(val["IMU_euler"]["pitch"])
#             orien += "{}\n".format(val["IMU_euler"]["yaw"])
#
#             l_out.append((int(key), orien))
#
#         l_out = sorted(l_out, key=itemgetter(0))
#         for _, s in l_out:
#             out_file.write(s)


for dir_name in depth_filepath:
    list_file = glob.glob(dir_name + "*.png")
    for f in list_file:
        img = cv2.imread(f, 0)

        h,w = img.shape

        if w < 200:
            continue

        x1 = int(w/2 - w/10)
        y1 = int(h/2 - h/7)
        x2 = int(w/2 + w/10)
        y2 = int(h/2 + h/8)

        # cv2.rectangle(img, (x1,y1), (x2,y2), 255)
        # cv2.imshow("", img)
        # cv2.waitKey(100)

        face = img[y1:y2,x1:x2]

        th,mask = cv2.threshold(face,110,255, cv2.THRESH_BINARY_INV)
        face_supp = cv2.bitwise_and(face,mask)

        face_norm = cv2.normalize(face_supp, None, 0, 255, cv2.NORM_MINMAX)
        face_eq = cv2.equalizeHist(face_supp)
        face_eq2 = cv2.equalizeHist(face)

        cv2.imshow("face", face)
        cv2.imshow("face background sup", face_supp)
        cv2.imshow("face norm", face_norm)
        cv2.imshow("face eq", face_eq)
        cv2.waitKey(1)

        # print "{}_face.png".format(f[:-4])
        cv2.imwrite("{}_face.png".format(f[:-4]), face)
        cv2.imwrite("{}_face_bs.png".format(f[:-4]), face_supp)
        cv2.imwrite("{}_face_nor.png".format(f[:-4]), face_norm)
        cv2.imwrite("{}_face_eq.png".format(f[:-4]), face_eq)