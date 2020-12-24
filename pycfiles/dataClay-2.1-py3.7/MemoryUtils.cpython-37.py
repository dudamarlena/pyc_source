# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataclay/heap/MemoryUtils.py
# Compiled at: 2019-10-28 11:50:26
# Size of source mod 2**32: 1366 bytes
""" Class description goes here. """
import os
_proc_status = '/proc/%d/status' % os.getpid()
_scale = {'kB':1024.0, 
 'mB':1048576.0,  'KB':1024.0, 
 'MB':1048576.0}

def _VmB(VmKey):
    """Private.
    """
    global _proc_status
    global _scale
    try:
        t = open(_proc_status)
        v = t.read()
        t.close()
    except:
        return 0.0
        i = v.index(VmKey)
        v = v[i:].split(None, 3)
        if len(v) < 3:
            return 0.0
        return float(v[1]) * _scale[v[2]]


def memory(since=0.0):
    """Return memory usage in bytes.
    """
    return _VmB('VmSize:') - since


def resident(since=0.0):
    """Return resident memory usage in bytes.
    """
    return _VmB('VmRSS:') - since


def stacksize(since=0.0):
    """Return stack size in bytes.
    """
    return _VmB('VmStk:') - since


def datasize(since=0.0):
    """Return data size in bytes.
    """
    return _VmB('VmData:') - since


def textsize(since=0.0):
    """Return text size in bytes.
    """
    return _VmB('VmExe:') - since


def peaksize(since=0.0):
    """Return peak size in bytes.
    """
    return _VmB('VmPeak:') - since