# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ht/PycharmProjects/THANN/Power_core.py
# Compiled at: 2019-11-04 01:47:06
import data as d, numpy as np
from Powerspectrum_Emulator import pk_pred

class PScore(object):

    def __init__(self):
        pass

    def __call__(self, ctx):
        params = ctx.getParams()
        ctx.add('params_pk', params)
        n_ion, R_mfp, NoH = params
        prm = [
         [
          n_ion, R_mfp, NoH]]
        prm = np.array(prm)
        prm.reshape(1, 3)
        pk_th = pk_pred(prm)
        ctx.add('key_data', pk_th)

    def setup(self):
        print 'Powerspectrum core setup is done'