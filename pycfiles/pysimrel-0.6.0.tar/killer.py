# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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