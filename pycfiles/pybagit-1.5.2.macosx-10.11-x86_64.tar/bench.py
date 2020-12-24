# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/pybagit/bench.py
# Compiled at: 2014-11-17 12:30:17
import os, timeit
pyb_statement = '\n    import os\n    os.system("~/Documents/code/git/pybagit/pybagit/multichecksum.py ~/Documents/code/git/edsu-bagit/newbag/data")\n'
t = timeit.Timer(pyb_statement)
print 'pybagit took %.2f seconds' % (10 * t.timeit(number=10) / 10)