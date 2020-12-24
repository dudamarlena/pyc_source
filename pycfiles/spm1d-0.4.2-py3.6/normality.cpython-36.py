# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/data/uv1d/normality.py
# Compiled at: 2019-08-22 04:37:03
# Size of source mod 2**32: 641 bytes
import os, numpy as np
from .. import _base

class NormalityAppendixDataset(_base.DatasetNormality1D):

    def __init__(self, name='A1'):
        self.dname = str(name)
        super(NormalityAppendixDataset, self).__init__()

    def _set_values(self):
        self.datafile = os.path.join(_base.get_datafilepath(), 'normality_dataset_%s.npy' % self.dname)
        self.Y = np.load(self.datafile)
        self.cite = 'Pataky TC, Vanrenterghem J, Robinson MA (2016) Normality assessments for one-dimensional biomechanical data.  Journal of Biomechanics (in review).'
        self.note = ('Note     ', 'Appendix %s, Dataset %s' % (self.dname[0], self.dname))