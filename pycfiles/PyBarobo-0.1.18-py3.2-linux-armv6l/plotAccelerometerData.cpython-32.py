# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv6l/egg/barobo/demo/with_BaroboCtx_sfp/plotAccelerometerData.py
# Compiled at: 2014-09-16 14:39:13
from barobo import Linkbot, Dongle
import pylab, threading, time, math, sys
if sys.version_info[0] == 3:
    raw_input = input

class RecordAccelData(threading.Thread):

    def __init__(self, linkbot):
        threading.Thread.__init__(self)
        self.continueRunning = False
        self.linkbot = linkbot
        self.times = []
        self.mags = []

    def run(self):
        while self.continueRunning:
            self.times.append(time.time() - self.startTime)
            alpha = self.linkbot.getAccelerometerData()
            mymag = 0
            for a in alpha:
                mymag += a ** 2

            mymag = math.sqrt(mymag)
            self.mags.append(mymag)
            time.sleep(0.01)

    def start(self):
        self.continueRunning = True
        self.startTime = time.time()
        threading.Thread.start(self)

    def join(self, *args, **kwargs):
        self.continueRunning = False
        threading.Thread.join(self, *args, **kwargs)

    def plot(self):
        pylab.plot(self.times, self.mags)
        pylab.show()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: {0} <Com_Port> [Linkbot Serial ID]'.format(sys.argv[0]))
        quit()
    if len(sys.argv) == 3:
        serialID = sys.argv[2]
    else:
        serialID = None
    dongle = Dongle()
    dongle.connectDongleSFP(sys.argv[1])
    linkbot = dongle.getLinkbot(serialID)
    record = RecordAccelData(linkbot)
    record.start()
    raw_input('Press enter to stop recording')
    record.join()
    record.plot()