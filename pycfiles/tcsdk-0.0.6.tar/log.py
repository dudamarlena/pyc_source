# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/workspace/workspace/tcsdk_deploy/tcsdk/tcsdk/common/log.py
# Compiled at: 2019-12-18 06:42:49
import logging
from tcsdk.common import default
logger = logging.getLogger(__name__)

def init_logger(name=default.NAME, level=default.LOGGER_LEVEL):
    global logger
    format_string = '%(asctime)s %(name)s [%(levelname)s] %(thread)d : %(message)s'
    logger = logging.getLogger(name)
    logger.setLevel(level)
    fh = logging.StreamHandler()
    fh.setLevel(level)
    formatter = logging.Formatter(format_string)
    fh.setFormatter(formatter)
    logger.addHandler(fh)