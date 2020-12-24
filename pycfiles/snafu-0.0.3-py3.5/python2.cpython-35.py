# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snafulib/executors/python2.py
# Compiled at: 2018-07-01 01:56:00
# Size of source mod 2**32: 1074 bytes
import json, subprocess, pickle, base64, tempfile

def strbool(x):
    if x == 'True':
        return True
    return False


def execute(func, funcargs, envvars, sourceinfos):
    for i, funcarg in enumerate(funcargs):
        if '__class__' in dir(funcarg) and funcarg.__class__.__name__ == 'SnafuContext':
            funcargs[i] = 'pickle:' + base64.b64encode(pickle.dumps(funcarg, protocol=2)).decode('utf-8')

    funcargs = json.dumps(funcargs)
    envvars = json.dumps(envvars)
    if len(funcargs) > 256:
        tf = tempfile.NamedTemporaryFile()
        tf.write(bytes(funcargs, 'utf-8'))
        funcargs = 'tempfile:' + tf.name
    p = subprocess.run("python2 snafulib/executors/python2-exec.py {} {} '{}' '{}'".format(sourceinfos.source, func.__name__, funcargs, envvars), stdout=subprocess.PIPE, shell=True)
    try:
        dtime, success, *res = p.stdout.decode('utf-8').strip().split(' ')
    except:
        dtime = 0.0
        success = False
        res = []

    dtime = float(dtime)
    success = strbool(success)
    res = ' '.join(res)
    return (
     dtime, success, res)