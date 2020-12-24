# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snafulib/executors/inmemory.py
# Compiled at: 2018-07-01 01:56:00
# Size of source mod 2**32: 372 bytes
import os, time

def execute(func, funcargs, envvars, sourceinfos):
    for envvar in envvars:
        os.environ[envvar] = envvars[envvar]

    stime = time.time()
    try:
        res = func(*funcargs)
        success = True
    except Exception as e:
        res = e
        success = False

    dtime = (time.time() - stime) * 1000
    return (
     dtime, success, res)