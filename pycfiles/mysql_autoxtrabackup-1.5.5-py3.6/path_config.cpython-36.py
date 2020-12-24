# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/general_conf/path_config.py
# Compiled at: 2018-09-13 02:55:15
# Size of source mod 2**32: 410 bytes
from os.path import expanduser, join
home = expanduser('~')
config_path = join(home, '.autoxtrabackup')
config_path_file = join(config_path, 'autoxtrabackup.cnf')
log_file_path = join(config_path, 'autoxtrabackup.log')