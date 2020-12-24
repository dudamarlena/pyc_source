# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/project/data_maker.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 1879 bytes
import numpy
from ctypes import c_float, c_uint8
from multiprocessing.sharedctypes import RawArray
from ..util import log
from . import importer
NUMPY_TYPES = ('int', 'int8', 'int16', 'int32', 'int64', 'uint', 'uint8', 'uint16',
               'uint32', 'uint64', 'float', 'float32', 'float64')
NUMPY_DEFAULTS = (True, 'true', 'True', 'float')

class Maker:

    def __init__(self, floating=None, shared_memory=False, numpy_dtype=None):
        if numpy_dtype:
            log.debug('Using numpy')
            if numpy_dtype in NUMPY_DEFAULTS:
                numpy_dtype = 'float32'
            if numpy_dtype not in numpy.sctypeDict:
                raise ValueError(BAD_NUMPY_TYPE_ERROR % numpy_dtype)
            if shared_memory:
                if numpy_dtype:
                    log.error('Shared memory for numpy arrays is not yet supported.')
                    numpy_dtype = None
        elif floating is None:
            floating = not shared_memory
        else:
            c_type = c_float if floating else c_uint8
            if shared_memory:
                self.bytes = lambda size: RawArray(c_uint8, size)
                self.color_list = lambda size: RawArray(3 * c_type, size)
            else:
                if numpy_dtype:
                    self.bytes = bytearray
                    self.color_list = lambda size: numpy.zeros((size, 3), numpy_dtype)
                else:
                    self.bytes = bytearray
            self.color_list = lambda size: [
             (0, 0, 0)] * size


MAKER = Maker()
NUMPY_MAKER = Maker(numpy_dtype='float')
ColorList = MAKER.color_list
NumpyColorList = NUMPY_MAKER.color_list
BAD_NUMPY_TYPE_ERROR = '\nBad numpy_type "%s"\n\nPossible numpy_type values include:\n    ' + ' '.join(NUMPY_TYPES)