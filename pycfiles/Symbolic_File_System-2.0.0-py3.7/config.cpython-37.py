# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sfs/config.py
# Compiled at: 2018-12-22 22:16:03
# Size of source mod 2**32: 379 bytes
import os
SFS_ROOT_DIR = os.path.expanduser('~/.sfs')
LOG_DIR_ENV_VAR = 'SFS_LOG_DIR'
LOG_DIR_DEFAULT = os.path.join(SFS_ROOT_DIR, 'logs')
LOG_FILE_NAME = 'sfs.log'
LOG_LEVEL_FILE = 'DEBUG'
LOG_FILE_MAX_SIZE = 10485760
LOG_FILE_NUM_BACKUPS = 10
CLI_OUTPUT_PREFIX = '>> '
TEST_DIR = os.path.join(SFS_ROOT_DIR, 'tests')