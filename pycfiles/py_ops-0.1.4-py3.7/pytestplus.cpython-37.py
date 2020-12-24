# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pyops\pytestplus.py
# Compiled at: 2019-12-22 00:25:50
# Size of source mod 2**32: 212 bytes


def pytest_addoption(parser):
    group = parser.getgroup('general')
    group.addoption('--force_run', action='store_true', dest='force_run', default=False,
      help='force run ahAPICore case.')