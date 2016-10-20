import numpy as np
import cv2
import json

BASE_DIR = "data"

class frameSet():

    def __init__(self):
        self.ts = 0.0

        self.frame_num = 0
        self.frameRGB = None
        self.frameDepth = None
        self.frameSkeleton = None
        self.frameDepthQuantized = None
        self.bodyJoints = np.array([])
        self.bodyJoints3D = np.array([])
        self.bodyJointsRGB = np.array([])
        self.bodyJointState = np.array([])
        self.body_tracked = False

        self.orientation_euler = {
            "roll": 0.0000,
            "pitch": 0.0000,
            "yaw": 0.0000
        }
        self.orientation_quat = np.array([0.0000,0.0000,0.0000,0.0000])

        self.shoulder_orientation_euler = {
            "roll": 0.0000,
            "pitch": 0.0000,
            "yaw": 0.0000
        }
        self.shoulder_orientation_quat = np.array([0.0000,0.0000,0.0000,0.0000])

    def save_img(self, dir_name, save_rgb=True):
        if self.frameRGB is not None and save_rgb:
            # h,w = self.frameRGB.shape[:2]
            # cv2.imwrite(dir_name+"/RGB/%06d_RGB.png" % self.frame_num, self.frameRGB[:,int(w/4.5):-int(w/4.5)])
            cv2.imwrite(dir_name+"/RGB/%06d_RGB.png" % self.frame_num, self.frameRGB)
        if self.frameDepth is not None:
            cv2.imwrite(dir_name+"/DEPTH/%06d_DEPTH.png" % self.frame_num, self.frameDepth)
        # if self.frameSkeleton is not None:
        #     cv2.imwrite(dir_name+"/Skeleton/%06d_Skel.png" % self.frame_num, self.frameSkeleton)

    def to_json(self):
        js = {
            "ts": self.ts,
            "frame_num": self.frame_num,
            "orientation": {
                "euler": self.orientation_euler,
                "quaternion": list(self.orientation_quat.astype(float))
            },
            "shoulder_orientation": {
                "euler": self.shoulder_orientation_euler,
                "quaternion": list(self.shoulder_orientation_quat.astype(float))
            },
            "joints": [(bj.x, bj.y) for bj in self.bodyJoints],
            "joints3D": [(bj.x, bj.y, bj.z) for bj in self.bodyJoints3D],
            "jointsRGB": [(bj.x, bj.y) for bj in self.bodyJointsRGB],
            "jointsState": [bj for bj in self.bodyJointState]
        }
        return json.dumps(js)

    def to_str(self):
        s = "{}\t".format(self.ts)
        s += "%06d\t" % self.frame_num

        s += "{}\t".format(self.orientation_euler["roll"])
        s += "{}\t".format(self.orientation_euler["pitch"])
        s += "{}\t".format(self.orientation_euler["yaw"])

        s += "{}\t".format(self.orientation_quat[0])
        s += "{}\t".format(self.orientation_quat[1])
        s += "{}\t".format(self.orientation_quat[2])
        s += "{}\t".format(self.orientation_quat[3])

        s += "{}\t".format(self.shoulder_orientation_euler["roll"])
        s += "{}\t".format(self.shoulder_orientation_euler["pitch"])
        s += "{}\t".format(self.shoulder_orientation_euler["yaw"])

        s += "{}\t".format(self.shoulder_orientation_quat[0])
        s += "{}\t".format(self.shoulder_orientation_quat[1])
        s += "{}\t".format(self.shoulder_orientation_quat[2])
        s += "{}\t".format(self.shoulder_orientation_quat[3])

        # for j in self.bodyJoints:
        #     s += "{}\t{}\t".format(j.x,j.y)
        s_joints = ["{}\t{}\t".format(j.x,j.y) for j in self.bodyJoints]
        s += "".join(s_joints)

        s_joints = ["{}\t{}\t{}\t".format(j.x, j.y, j.z) for j in self.bodyJoints3D]
        s += "".join(s_joints)

        s_joints = ["{}\t{}\t".format(j.x, j.y) for j in self.bodyJointsRGB]
        s += "".join(s_joints)

        s_joints = ["{}\t".format(j) for j in self.bodyJointState]
        s += "".join(s_joints)

        return s

    # @classmethod
    # def save_list(cls, frames, dir_name):
    #     dir_name = BASE_DIR+"/"+str(dir_name)
    #     if os.path.isdir(dir_name):
    #         # raise OSError("Directory already exists")
    #         print "Directory already exists"
    #         try:
    #             for i in range(1,100):
    #                 if not os.path.isdir(dir_name+"({})".format(i)):
    #                     dir_name += "({})".format(i)
    #                     break
    #         except:
    #             raise OSError("Directory already exists")
    #
    #     os.mkdir(dir_name)
    #     os.mkdir(dir_name+"/RGB")
    #     os.mkdir(dir_name+"/DEPTH")
    #     os.mkdir(dir_name+"/Skeleton")
    #
    #     with open(dir_name+"/data.txt", "w") as f_txt, open(dir_name+"/data.json", "w") as f_json:
    #         l_json = {}
    #         # f_txt.write("\n")
    #         for i,f in enumerate(frames):
    #             f.frame_num = i
    #             l_json["%06d" % i] = f.to_json()
    #             f_txt.write(f.to_str()+"\n")
    #             f.save_img(dir_name)
    #         json.dump(l_json, f_json, indent=2)