# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/wehrle/opt/FuzzAnPy2/FuzzAnPy/FuzzyNumber.py
# Compiled at: 2019-08-20 07:43:54
# Size of source mod 2**32: 3314 bytes
import numpy as np

class UncertainNumber(object):

    def __init__(self, values, Form='interval', nalpha=1):
        self.Form = Form
        self.nalpha = nalpha
        if self.Form == 'trapazoid':
            alpha = np.linspace(0, 1.0, self.nalpha)
            if values[1] == values[0]:
                A = values[1] - 0 * alpha
            else:
                A = values[1] - (values[1] - values[0]) * alpha
            if values[2] == values[3]:
                B = values[3] + 0 * alpha
            else:
                B = values[2] + (values[3] - values[2]) * alpha
            self.Value = np.array([A, B]).T
        else:
            if self.Form == 'triangular':
                alpha = np.linspace(0, 1, self.nalpha)
                A = values[1] - (values[1] - values[0]) * alpha
                B = values[1] + (values[2] - values[1]) * alpha
                self.Value = np.array([A, B]).T
            else:
                if self.Form == 'interval':
                    alpha = np.linspace(0, 1, self.nalpha)
                    A = values[0] - 0 * alpha
                    B = values[1] + 0 * alpha
                    self.Value = np.array([A, B]).T
                else:
                    if self.Form == 'gauss-cuttoff':
                        mean = values[0]
                        sigmaleft = values[1]
                        sigmaright = values[2]
                        sigmatrunc = values[3]
                        alpha = np.linspace(0, 1, self.nalpha)
                        A = np.zeros([self.nalpha, 2])
                        A[(0, 0)] = mean
                        A[(0, 1)] = mean
                        A[1:self.nalpha - 1, 0] = mean - np.sqrt(-2 * sigmaleft ** 2 * np.log(alpha[1:self.nalpha - 1]))
                        A[1:self.nalpha - 1, 1] = mean + np.sqrt(-2 * sigmaleft ** 2 * np.log(alpha[1:self.nalpha - 1]))
                        A[(self.nalpha - 1, 0)] = mean - sigmatrunc * sigmaleft
                        A[(self.nalpha - 1, 1)] = mean + sigmatrunc * sigmaright
                        self.Value = A

    def normalize(self):
        self.ValueNorm = np.zeros(np.shape(self.Value))
        for ii in range(np.size(self.Value, 0)):
            self.ValueNorm[ii, :, :] = self.Value[ii, :, :] / (self.Value[(ii, 0, 0)] + self.Value[(ii, 0, 1)]) / 2

    def calcArea(self):
        self.normalize()
        self.Area = np.zeros([np.size(self.Value, 0), 1])
        self.AreaNorm = np.zeros([np.size(self.Value, 0), 1])
        mu = np.linspace(0, 1, self.nAlpha)
        mu1 = np.linspace(1, 0, self.nAlpha)
        ymu = [mu, mu1]
        ymu = np.resize(ymu, [self.nAlpha * 2])
        for ii in range(np.size(self.Value, 0)):
            xVal = [
             self.Value[ii, :, 0], self.Value[ii, :, 1]] + np.min(self.Value[ii, :, :])
            xVal = np.resize(xVal, [self.nAlpha * 2])
            self.Area[ii] = np.abs(np.trapz(y=ymu, x=xVal))
            xValNorm = [self.ValueNorm[ii, :, 0], self.ValueNorm[ii, :, 1]]
            xValNorm = np.resize(xValNorm, [self.nAlpha * 2])
            self.AreaNorm[ii] = np.abs(np.trapz(y=ymu, x=xValNorm))

    def printValue(self):
        for ai in self.Value:
            print('[{},  {}]'.format(ai[0], ai[1]))


if __name__ == '__main__':
    print('Test printing of interval number:')
    AInt = UncertainNumber([10, 20])
    AInt.calcArea()
    AInt.printValue()
    print('Test printing of trapazoidal fuzzy number:')
    ATrap = UncertainNumber([10, 20, 30, 40], Form='trapazoid', nalpha=6)
    ATrap.printValue()