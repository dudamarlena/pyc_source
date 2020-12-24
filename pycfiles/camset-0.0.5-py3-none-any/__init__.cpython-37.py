# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camsaxs/__init__.py
# Compiled at: 2019-10-03 17:57:09
# Size of source mod 2**32: 348 bytes
from .remesh_bbox import remesh
from .cwt import cwt2d
from .factory import XicamSASModel
from .fit_sasmodel import fit_sasmodel
from .loader import load_models
try:
    models = load_models()
except:
    print('Warning: failed to load SASMODLES.')
    print('Please consider submitting a but-report')