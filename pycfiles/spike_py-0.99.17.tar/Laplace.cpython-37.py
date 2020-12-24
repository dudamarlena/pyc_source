# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/Algo/Laplace.py
# Compiled at: 2017-08-31 16:40:33
# Size of source mod 2**32: 5059 bytes
"""
Laplace.py

Created by Marc-André on 2012-07-27.
Copyright (c) 2012 IGBMC. All rights reserved.
"""
from __future__ import print_function
import numpy as np, math, maxent as me
from ..Display import testplot
plt = testplot.plot()

class TfILT(me.TransferFunction):
    __doc__ = " defines the transfert functions for a Inverse Laplace Transform\n    data    <-- transform --  image         The experimental transfer function\n    data     -- t_transform -->  image      The transpose of `transform'\n    \n    This is animplementation of maxentropy.TransferFunction()\n    \n    trivial (means slow...) implementation based on explicit exponentiation.\n    "

    def __init__(self):
        """
        sets-up the default function, which should be overloaded by a sub classer
        """
        self.init_transform = self.init_laplace

    def t_transform(self, datain):
        return self.laplace(datain, self.data_sampling, self.image_sampling)

    def transform(self, datain):
        """
        Laplace transform
        """
        return self.laplace(datain, self.image_sampling, self.data_sampling)

    def init_laplace(self, data_sampling, image_sampling):
        """
        sampling is the array containing the locations where the mesure is sampled
        evaluating is the array containing the locations where the ILT is to be computed
        copied over for security
        """
        self.data_sampling = np.copy(data_sampling)
        self.image_sampling = np.copy(image_sampling)
        ndata = data_sampling.size
        nimage = image_sampling.size
        self.norm = math.sqrt(self.laplace(np.ones(ndata) / ndata, data_sampling, image_sampling).sum() * self.laplace(np.ones(nimage) / nimage, image_sampling, data_sampling).sum())
        print('Norm of transform :', self.norm)

    def laplace(self, datain, samp_from, samp_to):
        """
        compute Laplace transform of datain
        samp_from is the sampling of datain
        samp_to is the sampling fo output
        """
        if samp_from.size != datain.size:
            raise Exception('size mismatch in Laplace transform')
        rr = np.zeros(samp_to.size)
        for i in range(samp_to.size):
            rr[i] = np.sum(datain * np.exp(-samp_from * samp_to[i]))

        return rr

    def exp_sampling(self, KK1, KK2, n):
        """
        returns n exponentially located points located between KK1 and KK2
        """
        K = (math.log(KK2) - math.log(KK1)) / (n - 1)
        rr = KK1 * np.exp(K * np.arange(n))
        return rr


def setup1(M):
    M.algo = 'Gifa'
    M.exptang = 0.0
    M.lambdacont = 'cosine'
    M.lambdamax = 1.05
    M.lambdasp = 2
    M.miniter = 5


def test_ILT():
    T = TfILT()
    experimental_samp = T.exp_sampling(1, 1000, 30)
    print('experimental_samp  (msec)\n', experimental_samp)
    image_samp = T.exp_sampling(0.001, 1.0, 100)
    print('image_samp  (msec-1)\n', image_samp)
    T.init_transform(experimental_samp, image_samp)
    size = 100
    sc = 100.0
    noise = 0.3
    Ideal = me.initial_scene_2delta(size, sc)
    Exp = T.transform(Ideal)
    Exp += sc * noise * np.random.randn(Exp.size)
    D = me.ExpData(Exp)
    D.noise = sc * noise
    dfig = me.plot(D.data, 'exp data')
    M = me.MaxEnt(T, D, debug=1, iterations=300)
    M.true_s = Ideal
    M.report()
    M.solve()
    if M.debug > 0:
        f = me.plot(Ideal, 'ideal')
        me.plot((M.image), 'finale', fig=f)
        me.plot(D.data, 'exp')
        residu = T.transform(M.image) - D.data
        me.plot(residu, 'residu')
    Dd = T.transform(M.image)
    me.plot(Dd, 'fitted data', dfig)
    plt.show()


def main():
    test_ILT()


if __name__ == '__main__':
    main()