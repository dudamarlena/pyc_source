# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\cgp\test\test_poormanslock.py
# Compiled at: 2012-02-03 05:34:20
__doc__ = 'Tests for :mod:`cgp.utils.poormanslock`.'
import unittest, logging, os, signal
from ..utils.poormanslock import Lock, log
import tempfile, shutil
dtemp = None
olddir = os.getcwd()

def setup():
    global dtemp
    dtemp = tempfile.mkdtemp()
    os.chdir(dtemp)


def teardown():
    os.chdir(olddir)
    shutil.rmtree(dtemp)


def _test_reuse():
    """
    Allow reuse of a lock, rather than having to construct it anew each time.
    
    (Known failure.)
    """
    lock = Lock()
    for _i in range(2):
        with lock:
            assert os.path.exists(lock.lockname)
        assert not os.path.exists(lock.lockname)


msg = "signal.alarm() not available, timeout won't work"

@unittest.skipIf(not hasattr(signal, 'alarm'), msg)
def test_timeout():
    """Test raising of "IOError: Timed out waiting to acquire lock"."""
    oldlevel = log.level
    try:
        log.setLevel(logging.CRITICAL)
        _f = open('lock', 'w')
        try:
            with Lock(max_wait=2):
                pass
        except IOError:
            pass
        else:
            raise Exception('Lock failed to time out')

        os.remove('lock')
        with Lock():
            pass
    finally:
        log.setLevel(oldlevel)