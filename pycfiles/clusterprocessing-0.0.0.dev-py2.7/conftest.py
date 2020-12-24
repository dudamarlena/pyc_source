# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/prologic/work/clusterprocessing/tests/conftest.py
# Compiled at: 2013-10-25 00:23:29
"""pytest config"""
from pytest import fixture

@fixture(scope='session')
def cluster(request):
    pass