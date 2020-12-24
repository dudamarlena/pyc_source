# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/cifitlib/test_procs.py
# Compiled at: 2011-01-27 14:39:21
"""
test_procs.py

Created by Craig Sawyer on 2010-01-14.
Copyright (c) 2009, 2010 Craig Sawyer (csawyer@yumaed.org). All rights reserved. see LICENSE.
"""
import nose, procs

def test_isRunning():
    assert procs.isRunning('launchd')


def test_getByCommand():
    assert len(procs.getProcesses().getByCommand('login')) == 8


if __name__ == '__main__':
    nose.run()