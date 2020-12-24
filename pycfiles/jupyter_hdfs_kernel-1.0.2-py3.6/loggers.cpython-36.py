# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/hdfs_kernel/utils/loggers.py
# Compiled at: 2020-01-16 03:10:17
# Size of source mod 2**32: 373 bytes
from hdijupyterutils.log import Log
import hdfs_kernel.utils.configuration as config
from hdfs_kernel.constants import HDFS_LOGGER_NAME

class HdfsLog(Log):

    def __init__(self, class_name):
        super(HdfsLog, self).__init__(HDFS_LOGGER_NAME, config.logging_config(), class_name)