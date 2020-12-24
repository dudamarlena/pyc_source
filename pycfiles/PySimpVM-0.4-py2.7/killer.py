# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\vm\killer.py
# Compiled at: 2014-12-06 15:15:50


def kill_process(proc):
    import sys
    from os import system as cmd
    if sys.platform != 'win32':
        cmd('kill -9 ' + proc)
    else:
        from warnings import error
        error('error: kill_process not supported on windows')
        return