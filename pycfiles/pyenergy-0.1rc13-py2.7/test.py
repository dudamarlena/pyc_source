# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyenergy/test.py
# Compiled at: 2014-03-12 12:05:35
import pyenergy, numpy
m1 = pyenergy.Measurement(1, 2)
m2 = pyenergy.Measurement(3, 4)
print m1
print m2
print numpy.mean([m1, m2])
print m1 + m2