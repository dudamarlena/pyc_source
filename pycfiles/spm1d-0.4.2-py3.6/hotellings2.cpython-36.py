# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/data/mv1d/hotellings2.py
# Compiled at: 2019-08-22 04:37:03
# Size of source mod 2**32: 984 bytes
import os, numpy as np
from .. import _base

class Besier2009muscleforces(_base.DatasetHotellings2, _base.Dataset1D):

    def _set_values(self):
        self.cite = 'Besier, T. F., Fredericson, M., Gold, G. E., Beaupré, G. S., & Delp, S. L. (2009). Knee muscle forces during walking and running in patellofemoral pain patients and pain-free controls. Journal of Biomechanics, 42(7), 898–905. http://doi.org/10.1016/j.jbiomech.2009.01.032'
        self.www = 'https://simtk.org/home/muscleforces'
        self.note = ('Results  ', 'Pataky, T., Robinson, M., & Vanrenterghem, J. (2015). Journal of Biomechanics. Journal of Biomechanics, 48(1), 190–192. http://doi.org/10.1016/j.jbiomech.2014.09.025')
        self.datafile = os.path.join(_base.get_datafilepath(), 'Besier2009muscleforces.npz')
        Z = np.load(self.datafile)
        self.YA = Z['YA']
        self.YB = Z['YB']
        Z.close()
        self.z = None
        self.df = None
        self.p = None