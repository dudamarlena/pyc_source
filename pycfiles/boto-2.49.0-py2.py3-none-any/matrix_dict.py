# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/botnee/process/matrix_dict.py
# Compiled at: 2012-08-16 08:10:08
__doc__ = '\nWrapper class over standard dictionary with some added functionality \n(print summary etc)\n'
from bidict import bidict
from ordereddict import OrderedDict
from scipy import sparse
import numpy as np, logging
from botnee import debug
import botnee_config

class MatrixDict(OrderedDict):

    def __init__(self, initial={}, verbose=True):
        OrderedDict.__init__(self)
        self.reset()
        self.update(initial)
        self.logger = logging.getLogger(__name__)

    def reset(self):
        """
        Initalise/Reset matrices. 
        Only resets the matrices defined in the config (does not touch any 
        additional fields)
        """
        for name in botnee_config.MATRIX_TYPES:
            for suffix in botnee_config.SUFFIXES:
                for ngstr in [ '_%d' % ngram for ngram in botnee_config.NGRAMS.keys() ]:
                    fullname = name + suffix + ngstr
                    self[fullname] = None

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