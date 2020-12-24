# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyenergy/test.py
# Compiled at: 2014-03-12 12:05:35
import pyenergy, numpy
m1 = pyenergy.Measurement(1, 2)
m2 = pyenergy.Measurement(3, 4)
print m1
print m2
print numpy.mean([m1, m2])
print m1 + m2