# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Labtools/Apps/PyMouse-MPU6050-accel-control.py
# Compiled at: 2015-05-19 05:34:01
import numpy as np
from Labtools import interface
import pymouse
P = pymouse.PyMouse()
if __name__ == '__main__':
    I = interface.Interface()
    from gyro import *
    gyro = MPU6050(I)
    noise1 = []
    noise2 = []
    for a in range(500):
        x, y, z = gyro.getAccel()
        noise1.append(np.arcsinh(x * np.pi))
        noise2.append(np.arcsinh(y * np.pi))

    std1 = np.std(noise1)
    std2 = np.std(noise2)
    var1 = 0.0001
    var2 = 0.0001
    eVar1 = std1 ** 2
    eVar2 = std2 ** 2
    K1 = KalmanFilter(var1, eVar1)
    K2 = KalmanFilter(var2, eVar2)
    while 1:
        x, y, z = gyro.getAccel()
        K1.input_latest_noisy_measurement(np.arcsinh(x * np.pi))
        K2.input_latest_noisy_measurement(np.arcsinh(y * np.pi))
        V1 = K1.get_latest_estimated_measurement()
        V2 = K2.get_latest_estimated_measurement()
        P.move((V2 + 0.5) * 4 * 400, (V1 + 0.5) * 4 * 200)