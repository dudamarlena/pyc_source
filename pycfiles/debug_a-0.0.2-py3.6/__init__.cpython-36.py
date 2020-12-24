# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\debug_a\__init__.py
# Compiled at: 2018-06-02 23:42:01
# Size of source mod 2**32: 628 bytes
import os
__version__ = '0.0.2'
__author__ = 'zengbin93'
__email__ = 'zeng_bin8888@163.com'
USER_HOME = os.path.expanduser('~')
PATH = os.path.join(USER_HOME, '.debug_a')
LOG_DIR = os.path.join(USER_HOME, '.debug_a/log/')
DATA_DIR = os.path.join(USER_HOME, '.debug_a/data/')
ACCOUNT_DIR = os.path.join(USER_HOME, '.debug_a/account/')
POOL_DIR = os.path.join(USER_HOME, '.debug_a/pool/')
for P in [PATH, LOG_DIR, DATA_DIR, ACCOUNT_DIR, POOL_DIR]:
    if not os.path.exists(P):
        os.mkdir(P)

from debug_a.utils import print_constitutions