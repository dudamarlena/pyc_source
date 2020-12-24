# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/prologic/work/clusterprocessing/tests/conftest.py
# Compiled at: 2013-10-25 00:23:29
__doc__ = 'pytest config'
from pytest import fixture

@fixture(scope='session')
def cluster(request):
    pass