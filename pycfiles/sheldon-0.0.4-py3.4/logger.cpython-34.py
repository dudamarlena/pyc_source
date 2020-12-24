# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/sheldon/utils/logger.py
# Compiled at: 2015-11-23 22:50:15
# Size of source mod 2**32: 512 bytes
"""
Functions for sending messages to log file

@author: Seva Zhidkov
@contact: zhidkovseva@gmail.com
@license: The MIT license

Copyright (C) 2015
"""
import logging
logging.basicConfig(filename='sheldon.log', level=logging.INFO)

def info_message(message):
    logging.info(message)


def warning_message(message):
    logging.warning(message)


def error_message(message):
    logging.error(message)


def critical_message(message):
    logging.critical(message)