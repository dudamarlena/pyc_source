# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/apgl/util/PySparseUtils.py
# Compiled at: 2011-02-28 15:07:52
__doc__ = '\nWe extend the pysparse lil_matrix with some useful methods. \n'
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

        return (
         rows, cols)