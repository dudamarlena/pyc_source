# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/amplitf/likelihood.py
# Compiled at: 2020-03-13 07:22:48
# Size of source mod 2**32: 1705 bytes
import tensorflow as tf
import amplitf.interface as atfi

@atfi.function
def integral(pdf):
    """
      Return the graph for the integral of the PDF
        pdf : PDF
    """
    return tf.reduce_mean(pdf)


@atfi.function
def weighted_integral(pdf, weight_func):
    """
      Return the graph for the integral of the PDF
        pdf : PDF
        weight_func : weight function
    """
    return tf.reduce_mean(pdf * weight_func)


@atfi.function
def unbinned_nll(pdf, integral):
    """
      Return unbinned negative log likelihood graph for a PDF
        pdf      : PDF 
        integral : precalculated integral
    """
    return -tf.reduce_sum(atfi.log(pdf / integral))


@atfi.function
def unbinned_weighted_nll(pdf, integral, weight_func):
    """
      Return unbinned weighted negative log likelihood graph for a PDF
        pdf         : PDF
        integral    : precalculated integral
        weight_func : weight function
    """
    return -tf.reduce_sum(atfi.log(pdf / integral) * weight_func)