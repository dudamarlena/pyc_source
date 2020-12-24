# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/core/test_system.py
# Compiled at: 2013-10-31 06:07:30
from mio.version import version

def test_args(mio):
    assert mio.eval('System args') == []


def test_version(mio):
    assert mio.eval('System version') == version


def test_exit(mio):
    try:
        mio.eval('System exit()')
        assert False
    except SystemExit as e:
        assert e.args[0] == 0


def test_exit_status(mio):
    try:
        mio.eval('System exit(1)')
        assert False
    except SystemExit as e:
        assert e.args[0] == 1