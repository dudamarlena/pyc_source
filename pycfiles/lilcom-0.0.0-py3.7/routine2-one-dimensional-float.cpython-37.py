# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/test/routine2-one-dimensional-float.py
# Compiled at: 2019-08-11 16:00:44
# Size of source mod 2**32: 739 bytes
import numpy, lilcom, random
n_samples = 1000
inputArray = numpy.array([random.uniform(0, 1) for i in range(n_samples)]).astype(numpy.float32)
outputArray = numpy.zeros(inputArray.shape, numpy.int8)
reconstruction = numpy.zeros(inputArray.shape, numpy.int16)
lilcom.compressf_8i(inputArray, outputArray)
c_exponent = lilcom.decompress(outputArray, reconstruction)
for i in range(n_samples):
    print('Sample no ', i, 'original number = ', inputArray[i], ' compressed = ', outputArray[i], ' reconstructed number = ', reconstruction[i])