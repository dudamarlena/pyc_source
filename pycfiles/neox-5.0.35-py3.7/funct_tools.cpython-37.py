# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/neox/commons/funct_tools.py
# Compiled at: 2020-02-26 23:29:02
# Size of source mod 2**32: 672 bytes
import time, locale
from datetime import datetime
try:
    locale.setlocale(locale.LC_ALL, str('es_CO.UTF-8'))
except:
    print('Warning: Error setting locale')

starttime = datetime.now()

def time_record(x):
    now = datetime.now()
    print((x, (now - starttime).total_seconds()))


def time_dec(func):

    def time_mes(self, *arg):
        t1 = time.clock()
        res = func(self, *arg)
        t2 = time.clock()
        delta = (t2 - t1) * 1000.0
        print('%s take %0.5f ms' % (func.__name__, delta))
        return res

    return time_mes