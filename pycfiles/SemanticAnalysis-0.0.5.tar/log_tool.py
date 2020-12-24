# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ../common/log_tool.py
# Compiled at: 2016-07-07 02:49:53
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', datefmt='%a, %d %b %Y %H:%M:%S', filename='/tmp/log_file.log', filemode='a')

class Logging(object):

    @staticmethod
    def get_logger():
        return logging