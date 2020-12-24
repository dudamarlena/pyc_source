# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snafulib/executors/java.py
# Compiled at: 2018-07-01 01:56:00
# Size of source mod 2**32: 834 bytes
import subprocess, os, time

def execute(func, funcargs, envvars, sourceinfos):
    classname = os.path.basename(sourceinfos.source).split('.')[0]
    methodname = func.split('.')[1]
    javacmd = 'java -cp snafulib/executors/java/:{} JavaExec {} {} {}'.format(os.path.dirname(sourceinfos.source), classname, methodname, ' '.join(funcargs))
    stime = time.time()
    out, err = subprocess.Popen(javacmd, shell=True, stdout=subprocess.PIPE).communicate()
    dtime = (time.time() - stime) * 1000
    out = out.decode('utf-8').split('\n')[(-2)]
    return (
     dtime, True, out)