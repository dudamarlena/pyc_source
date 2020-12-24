# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/cifitlib/test_procs.py
# Compiled at: 2011-01-27 14:39:21
__doc__ = '\ntest_procs.py\n\nCreated by Craig Sawyer on 2010-01-14.\nCopyright (c) 2009, 2010 Craig Sawyer (csawyer@yumaed.org). All rights reserved. see LICENSE.\n'
import nose, procs

def test_isRunning():
    assert procs.isRunning('launchd')


def test_getByCommand():
    assert len(procs.getProcesses().getByCommand('login')) == 8


if __name__ == '__main__':
    nose.run()