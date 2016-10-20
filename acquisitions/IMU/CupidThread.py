import threading
import Cupid
from datetime import datetime, date
import time
import numpy as np


class CupidThread(threading.Thread):

    def acquire(self):
        count=0
        # f = open("data/{0:05d}".format(count) + ".txt", "w")
        # d_now = str(datetime.now())
        # f = open("data/data_{}_{}_{}_{}".format(d_now[:10], d_now[11:13], d_now[14:16], d_now[17:19]) + ".txt", "w")

        while True:
            try:
                count += 1
                pkt = self.node.get_pkt()

                #decode data
                data = self.node.get_pkt_data(pkt)

                # self.node.pkt_print(pkt)

                if self.node.is_calibrate:
                    ts = int(time.time() * 1000)
                    item = np.array([data])
                    self.outQ.put(item)

                    # str_data = ""
                    # for x in data:
                    #     str_data = str_data + str(x) + "\t"

                    # f.write("%d" % ts + "\t" + str_data +"\n")

                if self.stopped():
                    break

            except Exception as e:
                print e
                print "Failed something during pkt read"
                return

        # f.close()

    def __init__(self, outQ, port="COM7", save_conf=False, auto_calib = True,
                 accelerometer="4g", gyro="250dps", algo="kalman", sample_rate="100hz"):
        super(CupidThread, self).__init__()
        self.stoprequest = threading.Event()
        self.node = Cupid.Cupid(port, save_conf, auto_calib, accelerometer, gyro, algo, sample_rate)
        self.outQ = outQ

    def run(self):
        self.acquire()

    def stop(self):
        self.stoprequest.set()

    def stopped(self):
        return self.stoprequest.isSet()
