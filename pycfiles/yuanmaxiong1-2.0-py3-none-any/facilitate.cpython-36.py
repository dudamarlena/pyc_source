# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\研发资料\瓦力课程\试听课\代码\dianyi\facilitate.py
# Compiled at: 2019-07-31 23:22:58
# Size of source mod 2**32: 217 bytes
import time

def time_count(func):

    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        print(func, time.time() - start)
        return res

    return wrapper