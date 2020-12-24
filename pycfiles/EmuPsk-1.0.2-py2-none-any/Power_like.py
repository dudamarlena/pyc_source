# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ht/PycharmProjects/THANN/Power_like.py
# Compiled at: 2019-11-28 14:07:26
import data as d, numpy as np
index = d.indexx
id = d.ind
i_2 = d.i_2

class PSlikeModule(object):

    def __init__(self):
        pass

    def computeLikelihood(self, ctx):
        pk_th = ctx.get('key_data')
        pk_ob = d.PK[index[0][id]]
        pk_ob = pk_ob.reshape(1, 7)
        diff = pk_th - pk_ob
        diff = diff.reshape(1, 7)
        cov_inv = d.cov_inv
        logl = -np.dot(diff, np.dot(cov_inv, diff.T)) / 2.0
        return logl

    def setup(self):
        print 'Powerspectrum logLikelihood setup is done'