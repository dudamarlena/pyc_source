# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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