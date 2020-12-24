# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/krantsonemailgo/logger.py
# Compiled at: 2017-10-19 19:38:44
import logging

def get_logger(log_level=logging.INFO):
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s [emcli] [%(levelname)s]: %(message)s', '%Y-%m-%d %H:%M:%S')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.handlers = [
     handler]
    return logger