# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snafulib/executors/lxc.py
# Compiled at: 2018-07-01 01:56:00
# Size of source mod 2**32: 925 bytes
import os, time, lxc, tempfile

def wrapper(funcwithargs):
    print(funcwithargs[1](*funcwithargs[2:]), file=funcwithargs[0])


def execute(func, funcargs, envvars, sourceinfos):
    for envvar in envvars:
        os.environ[envvar] = envvars[envvar]

    c = lxc.Container('snafu')
    c.create('download', 0, {'dist': 'alpine', 'release': '3.6', 'arch': 'amd64'})
    success = c.start()
    if not success:
        raise Exception('LXC permissions insufficient')
    channel = tempfile.TemporaryFile(mode='w+', buffering=1)
    stime = time.time()
    try:
        c.attach_wait(wrapper, (channel, func, *funcargs))
        channel.seek(0)
        res = channel.read().strip()
        success = True
    except Exception as e:
        res = e
        success = False

    dtime = (time.time() - stime) * 1000
    return (
     dtime, success, res)