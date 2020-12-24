# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/yapocis/examples/demo_numpy.py
# Compiled at: 2011-08-30 23:33:15
import numpy, numpy.linalg as la, time
a = numpy.random.rand(50000)
b = numpy.random.rand(50000)
t = time.time()
a_plus_b = a + b
print 'Elapsed:', time.time() - t
print (
 la.norm(a_plus_b - (a + b)), la.norm(a_plus_b))