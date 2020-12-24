# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snafulib/executors/c.py
# Compiled at: 2018-07-01 01:56:00
# Size of source mod 2**32: 565 bytes
import subprocess, os, time

def execute(func, funcargs, envvars, sourceinfos):
    ccmd = 'snafulib/executors/c/cexec {} {}'.format(sourceinfos.source, ' '.join(funcargs))
    stime = time.time()
    out, err = subprocess.Popen(ccmd, shell=True, stdout=subprocess.PIPE).communicate()
    dtime = (time.time() - stime) * 1000
    try:
        out = out.decode('utf-8').split('\n')[(-2)]
        success = True
    except:
        out = ''
        success = False

    return (dtime, success, out)