# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snafulib/executors/inmemstateless.py
# Compiled at: 2018-07-01 01:56:00
# Size of source mod 2**32: 566 bytes
import os, time, importlib.machinery

def execute(func, funcargs, envvars, sourceinfos):
    loader = importlib.machinery.SourceFileLoader(os.path.basename(sourceinfos.source), sourceinfos.source)
    loader.exec_module(sourceinfos.module)
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