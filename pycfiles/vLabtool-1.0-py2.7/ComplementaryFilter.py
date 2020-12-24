# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vLabtool/SENSORS/ComplementaryFilter.py
# Compiled at: 2015-07-07 09:22:34


class ComplementaryFilter:

    def __init__(self):
        self.pitch = 0
        self.roll = 0
        self.dt = 0.001

    def addData(self, accData, gyrData):
        self.pitch += gyrData[0] * self.dt
        self.roll -= gyrData[1] * self.dt
        forceMagnitudeApprox = abs(accData[0]) + abs(accData[1]) + abs(accData[2])
        pitchAcc = np.arctan2(accData[1], accData[2]) * 180 / np.pi
        self.pitch = self.pitch * 0.98 + pitchAcc * 0.02
        rollAcc = np.arctan2(accData[0], accData[2]) * 180 / np.pi
        self.roll = self.roll * 0.98 + rollAcc * 0.02

    def getData(self):
        return (
         self.roll, self.pitch)