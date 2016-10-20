import threading
import json
import cv2
from cv2.cv import CV_FOURCC

class SaveThread(threading.Thread):
    def __init__(self, writeQueue, save_dir):
        super(SaveThread, self).__init__()
        self.stoprequest = False

        self.writeQueue = writeQueue
        self.save_dir = save_dir

        # fourcc = CV_FOURCC('X','V','I','D')
        # self.videoWr = cv2.VideoWriter(self.save_dir + "/video.avi", -1, 30.0, (1920, 1080), isColor=True)
        # self.videoWr = cv2.VideoWriter(self.save_dir + "/video.avi", fourcc, 30.0, (1920, 1080), isColor=True)

        self.f_txt = open(self.save_dir+"/data.txt", "w")
        self.f_json = open(self.save_dir+"/data.json", "w")
        self.l_json = {}

    def writeFrame(self):
        frame = self.writeQueue.get()

        if not frame.body_tracked:
            return

        self.l_json["%06d" % frame.frame_num] = frame.to_json()
        self.f_txt.write(frame.to_str() + "\n")

        # self.videoWr.write(frame.frameRGB)
        frame.save_img(self.save_dir, save_rgb=True)


    def write(self):
        if self.f_txt is None:
            self.f_txt = open(self.save_dir+"/data.txt", "w")
        if self.f_json is None:
            self.f_json = open(self.save_dir+"/data.json", "w")

        while True:
            self.writeFrame()

            if self.stopped():
                break

    def run(self):
        self.write()

    def stop(self):
        print "Save thread is shutting down"
        # print self.writeQueue.qsize()
        self.stoprequest = True

        while not self.writeQueue.empty():
            self.writeFrame()

        # self.videoWr.release()

        json.dump(self.l_json, self.f_json, indent=2, sort_keys=True)
        self.l_json = {}

        self.f_txt.close()
        self.f_json.close()

        self.writeQueue.queue.clear()

    def stopped(self):
        return self.stoprequest
