# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vLabtool/SENSORS/MPU6050.py
# Compiled at: 2015-07-23 02:10:38
from numpy import int16

class MPU6050:
    GYRO_CONFIG = 27
    ACCEL_CONFIG = 28
    GYRO_SCALING = [131, 65.5, 32.8, 16.4]
    ACCEL_SCALING = [16384, 8192, 4096, 2048]
    AR = 3
    GR = 3
    NUMPLOTS = 7

    def __init__(self, I2C):
        self.I2C = I2C
        self.ADDRESS = 104
        self.name = 'Accel/gyro'
        self.params = {'powerUp': ['Go'], 'setGyroRange': [250, 500, 1000, 2000], 'setAccelRange': [2, 4, 8, 16]}
        self.setGyroRange(2000)
        self.setAccelRange(16)
        self.powerUp(True)

    def getVals(self, addr, bytes):
        vals = self.I2C.readBulk(self.ADDRESS, addr, bytes)
        return vals

    def powerUp(self, x):
        self.I2C.writeBulk(self.ADDRESS, [107, 0])

    def setGyroRange(self, rs):
        self.GR = self.params['setGyroRange'].index(rs)
        self.I2C.writeBulk(self.ADDRESS, [self.GYRO_CONFIG, self.GR << 3])

    def setAccelRange(self, rs):
        self.AR = self.params['setAccelRange'].index(rs)
        self.I2C.writeBulk(self.ADDRESS, [self.ACCEL_CONFIG, self.AR << 3])

    def getRaw(self):
        """
                This method must be defined if you want GUIs to use this class to generate 
                plots on the fly.
                It must return a set of different values read from the sensor. such as X,Y,Z acceleration.
                The length of this list must not change, and must be defined in the variable NUMPLOTS.
                
                GUIs will generate as many plots, and the data returned from this method will be appended appropriately
                """
        vals = self.getVals(59, 14)
        if vals:
            if len(vals) == 14:
                raw = [
                 0] * 7
                for a in range(3):
                    raw[a] = 1.0 * int16(vals[(a * 2)] << 8 | vals[(a * 2 + 1)]) / self.ACCEL_SCALING[self.AR]

                for a in range(4, 7):
                    raw[a] = 1.0 * int16(vals[(a * 2)] << 8 | vals[(a * 2 + 1)]) / self.GYRO_SCALING[self.GR]

                raw[3] = int16(vals[6] << 8 | vals[7]) / 340.0 + 36.53
                return raw
            else:
                return False

        else:
            return False

    def getAccel(self):
        vals = self.getVals(59, 6)
        ax = int16(vals[0] << 8 | vals[1])
        ay = int16(vals[2] << 8 | vals[3])
        az = int16(vals[4] << 8 | vals[5])
        return [ax / 65535.0, ay / 65535.0, az / 65535.0]

    def getTemp(self):
        vals = self.getVals(65, 6)
        t = int16(vals[0] << 8 | vals[1])
        return t / 65535.0

    def getGyro(self):
        vals = self.getVals(67, 6)
        ax = int16(vals[0] << 8 | vals[1])
        ay = int16(vals[2] << 8 | vals[3])
        az = int16(vals[4] << 8 | vals[5])
        return [ax / 65535.0, ay / 65535.0, az / 65535.0]