# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/hdfs_kernel/constants.py
# Compiled at: 2020-01-16 03:28:53
# Size of source mod 2**32: 1220 bytes
import os
LANG_HDFS = 'hdfs'
__version__ = '1.0.2'
KERNEL_NAME = 'Hdfs'
DISPLAY_NAME = 'HDFS'
LANGUAGE = 'hdfs'
DEFAULT_TEXT_LANG = ['en']
HOME_PATH = os.environ.get('HDFS_CONF_DIR', '~/.hdfs')
CONFIG_FILE = os.environ.get('HDFS_CONF_FILE', 'config.json')
HDFS_LOGGER_NAME = 'HdfsLogger'
INTERNAL_ERROR_MSG = 'An internal error was encountered.\nError:\n{}'
EXPECTED_ERROR_MSG = 'An error was encountered:\n{}'
HDFS_PREFIX = 'hdfs://'
RESOLVED_PREFIX = 'resolved://'
HDFS_FILE_TYPE = 'FILE'
HDFS_DIRECTORY_TYPE = 'DIRECTORY'
HELP_TIPS = '\nUsage: hadoop fs [generic options]\n\t[-chgrp GROUP PATH...]\n\t[-chmod <MODE[,MODE]... | OCTALMODE> PATH...]\n\t[-chown [OWNER][:[GROUP]] PATH...]\n\t[-copyFromLocal [-f] [-p] [-l] <localsrc> ... <dst>]\n\t[-count [-q] [-h] [-v] <path> ...]\n\t[-cp [-f] [-p | -p[topax]] <src> ... <dst>]\n\t[-du [-s] [-h] <path> ...]\n\t[-get [-p] [-ignoreCrc] [-crc] <src> ... <localdst>]\n\t[-help]\n\t[-ls [-C] [-d] [-h] [-q] [-R] [-t] [-S] [-r] [-u] [<path> ...]]\n\t[-mkdir [-p] <path> ...]\n\t[-mv <src> ... <dst>]\n\t[-put [-f] [-p] [-l] <localsrc> ... <dst>]\n\t[-rm [-f] [-r|-R] <src> ...]\n'