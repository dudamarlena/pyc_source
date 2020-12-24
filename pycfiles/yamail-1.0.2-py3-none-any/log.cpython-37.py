# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/didi/PycharmProjects/nnmail/yamail/log.py
# Compiled at: 2018-06-04 09:32:49
# Size of source mod 2**32: 1112 bytes
"""
The logging options for yagmail. Note that the logger is set on the SMTP class.

The default is to only log errors. If wanted, it is possible to do logging with:

yag = SMTP()
yag.setLog(log_level = logging.DEBUG)

Furthermore, after creating a SMTP object, it is possible to overwrite and use your own logger by:

yag = SMTP()
yag.log = myOwnLogger
"""
import logging

def get_logger(log_level=logging.DEBUG, file_path_name=None):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)
    if file_path_name:
        ch = logging.FileHandler(file_path_name)
    else:
        if log_level is None:
            logger.handlers = [
             logging.NullHandler()]
            return logger
        ch = logging.StreamHandler()
    ch.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s [yagmail] [%(levelname)s] : %(message)s', '%Y-%m-%d %H:%M:%S')
    ch.setFormatter(formatter)
    logger.handlers = [
     ch]
    return logger