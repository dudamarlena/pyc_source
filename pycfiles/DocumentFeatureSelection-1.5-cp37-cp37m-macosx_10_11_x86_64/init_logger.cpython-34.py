# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kensuke-mi/Desktop/analysis_work/document-feature-selection/DocumentFeatureSelection/init_logger.py
# Compiled at: 2016-11-29 04:36:51
# Size of source mod 2**32: 754 bytes
LOGGER_NAME = 'DocumentFeatureSelection'
import logging, os, sys
from logging import getLogger, Formatter, Logger, StreamHandler
from logging.handlers import SMTPHandler, RotatingFileHandler, TimedRotatingFileHandler
custmoFormatter = Formatter(fmt='[%(asctime)s]%(levelname)s - %(filename)s#%(funcName)s:%(lineno)d: %(message)s', datefmt='Y/%m/%d %H:%M:%S')
STREAM_LEVEL = logging.DEBUG
STREAM_FORMATTER = custmoFormatter
STREAM = sys.stdout
st_handler = StreamHandler(stream=STREAM)
st_handler.setLevel(STREAM_LEVEL)
st_handler.setFormatter(STREAM_FORMATTER)

def init_logger(logger: logging.Logger) -> logging.Logger:
    logger.addHandler(st_handler)
    logger.propagate = False
    return logger