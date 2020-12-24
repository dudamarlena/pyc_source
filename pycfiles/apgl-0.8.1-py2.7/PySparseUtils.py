# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/apgl/util/PySparseUtils.py
# Compiled at: 2011-02-28 15:07:52
"""
We extend the pysparse lil_matrix with some useful methods. 
"""
import numpy

class PySparseUtils(object):

    @staticmethod
    def sum(M):
        """
        Sum all of the elements of the matrix M.
        """
        rows, cols = PySparseUtils.nonzero(M)
        elements = numpy.zeros(len(rows))
        M.take(elements, rows, cols)
        return numpy.sum(elements)

    @staticmethod
    def nonzero(M):
        """
        Compute the nonzero entries of the matrix M, and return a tuple of two
        arrays - the first containing row indices and the second containing
        columns ones. 
        """
        rows = numpy.zeros(M.nnz, numpy.int)
        cols = numpy.zeros(M.nnz, numpy.int)
        kys = list(M.keys())
        for i in range(M.nnz):
            rows[i] = kys[i][0]
            cols[i] = kys[i][1]

        return (rows, cols)