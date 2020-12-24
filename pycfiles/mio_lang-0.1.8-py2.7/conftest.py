# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/prologic/work/mio/tests/conftest.py
# Compiled at: 2013-10-30 11:30:31
"""pytest config"""
from pytest import fixture
from mio import runtime

@fixture(scope='module')
def mio(request):
    runtime.init()
    return runtime.state