# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/botnee/process/data_dict.py
# Compiled at: 2012-08-13 08:59:42
"""
Wrapper class over standard dictionary with some added functionality 
(print summary etc)
"""
from bidict import bidict
from ordereddict import OrderedDict
from botnee.persistent_dict import PersistentDict
from scipy import sparse
import numpy as np, logging
from botnee import debug
import botnee_config
IGNORE_ON_LOAD = ('term_freq_bad', )

class DataDict(PersistentDict):

    def __init__(self, initial={}, verbose=True, persistent=True):
        params = {'filename': botnee_config.DATA_DICT_FILE + '.dat', 
           'flag': 'c', 
           'mode': None, 
           'format': botnee_config.DATA_DICT_STORE_TYPE, 
           'persistent': persistent, 
           'ingore_on_load': IGNORE_ON_LOAD}
        self.logger = logging.getLogger(__name__)
        PersistentDict.__init__(self, params, verbose, self.logger)
        for ngram in botnee_config.NGRAMS.keys():
            ngstr = '_%d' % ngram
            if 'idf' + ngstr not in self:
                self['idf' + ngstr] = np.array([], dtype=np.uint16)
            if 'term_freq' + ngstr not in self:
                self['term_freq' + ngstr] = np.array([], dtype=np.uint16)

        self.update(initial)
        self.flush(verbose, self.logger)
        return

    def get_summary_as_list(self):
        summary = []
        for (k, v) in self.items():
            if type(v) in [dict, bidict, OrderedDict]:
                v = np.array(v.values())
            size = debug.get_size_as_string(v)
            if sparse.isspmatrix(v):
                sparsity = '%.4f' % (np.float32(v.nnz) / np.product(v.shape))
                summary.append({'name': k, 'info': "<type 'scipy.sparse'> (%d,%d)" % v.shape, 
                   'size': size, 
                   'sparsity': sparsity})
            elif type(v) in [np.array, np.ndarray]:
                if len(v.shape) == 1:
                    shapestr = '(%d,)' % v.shape
                else:
                    shapestr = '(%d,%d)' % v.shape
                try:
                    pshape = max(np.product(v.shape), 1)
                    sparsity = '%.4f' % (np.float32(np.count_nonzero(v)) / pshape)
                    summary.append({'name': k, 'info': str(type(v)) + ' ' + shapestr, 
                       'size': size, 
                       'sparsity': sparsity})
                except TypeError, e:
                    print e

            else:
                try:
                    summary.append({'name': k, 'info': str(type(v))})
                except TypeError:
                    pass

        return summary

    def print_summary(self, verbose):
        for line in self.get_summary_as_list():
            debug.print_verbose(line, verbose, self.logger)