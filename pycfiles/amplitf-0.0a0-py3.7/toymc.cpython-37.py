# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/amplitf/toymc.py
# Compiled at: 2020-03-13 07:22:48
# Size of source mod 2**32: 3314 bytes
import tensorflow as tf, numpy as np
import amplitf.interface as atfi

def accept_reject_sample(density, sample):
    """
      Return toy MC sample graph using accept-reject method
        density : function to calculate density
        sample  : input uniformly distributed sample
    """
    x = sample[..., 0:-1]
    if density is not None:
        r = sample[(Ellipsis, -1)]
        return tf.boolean_mask(x, density(x) > r)
    return x


def maximum_estimator(density, phsp, size):
    """
      Return the graph for the estimator of the maximum of density function
        density : density function
        phsp : phase space object (should have uniform_sample method implemented)
        size : size of the random sample for maximum estimation
    """
    sample = phsp.uniform_sample(size)
    return tf.reduce_max(density(sample))


def run_toymc(pdf, phsp, size, maximum, chunk=200000, seed=None):
    """
      Create toy MC sample. To save memory, the sample is generated in "chunks" of a fixed size 
             pdf : Function returning PDF graph for a given sample as an agrument
            phsp : phase space
            size : size of the target data sample (if >0) or number of chunks (if <0)
         maximum : maximum PDF value for accept-reject method
           chunk : chunk size
            seed : initial random seed. Not initalised if None
    """
    length, nchunk, curr_maximum = 0, 0, maximum
    dim = phsp.dimensionality()
    data = tf.Variable((np.empty((0, dim))), shape=(None, dim), dtype=(atfi.fptype()))
    if seed is not None:
        atfi.set_seed(seed)

    def condition(length, size, nchunk):
        return length < size or nchunk < -size

    @atfi.function
    def pdf_vals(chunk, curr_maximum):
        d = accept_reject_sample(pdf, phsp.filter(phsp.unfiltered_sample(chunk, curr_maximum)))
        return (d, pdf(d))

    print(type(length), type(size), type(nchunk))
    while condition(length, size, nchunk):
        d, v = pdf_vals(chunk, curr_maximum)
        over_maximum = v[(v > curr_maximum)]
        if len(over_maximum) > 0:
            new_maximum = tf.reduce_max(over_maximum) * 1.5
            print(f"  Updating maximum: {curr_maximum} -> {new_maximum}. Starting over.")
            length, nchunk, curr_maximum = 0, 0, new_maximum
            data = tf.Variable((np.empty((0, dim))), shape=(None, dim), dtype=(atfi.fptype()))
            continue
        data = tf.concat([data, d], axis=0)
        length += len(d)
        nchunk += 1
        print(f"  Chunk {nchunk}, size={len(d)}, total length={length}")

    if size > 0:
        return data[:size]
    return data