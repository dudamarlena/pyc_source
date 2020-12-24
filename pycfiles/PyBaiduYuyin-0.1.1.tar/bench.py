# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/site-packages/pybagit/bench.py
# Compiled at: 2014-11-17 12:30:17
import os, timeit
pyb_statement = '\n    import os\n    os.system("~/Documents/code/git/pybagit/pybagit/multichecksum.py ~/Documents/code/git/edsu-bagit/newbag/data")\n'
t = timeit.Timer(pyb_statement)
print 'pybagit took %.2f seconds' % (10 * t.timeit(number=10) / 10)