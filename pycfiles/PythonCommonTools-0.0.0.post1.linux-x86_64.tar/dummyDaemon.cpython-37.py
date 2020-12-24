# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/dist-packages/test/daemonCommon/dummyDaemon.py
# Compiled at: 2019-05-03 20:34:21
# Size of source mod 2**32: 864 bytes
from pythoncommontools.daemonCommon.daemonCommon import startSingleInstance, stopSingleInstance, statusSingleInstance, daemonize, pidDirectory
from os.path import basename, extsep
scriptFullPath = __file__
scriptName = basename(__file__).split(extsep)[0]
statusFileFullPath = pidDirectory + scriptName + extsep + 'status'

def customStart():
    startSingleInstance(scriptName)
    while True:
        pass


def customStop():
    stopSingleInstance(scriptName)


def customStatus():
    status = statusSingleInstance(scriptName)
    with open(statusFileFullPath, 'w') as (statusFile):
        statusFile.write(str(status))
    statusFile.closed


if __name__ == '__main__':
    daemonize(customStart, customStop, customStatus)