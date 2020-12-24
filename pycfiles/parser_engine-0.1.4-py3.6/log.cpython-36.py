# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/parser_engine/log.py
# Compiled at: 2019-04-16 05:55:04
# Size of source mod 2**32: 679 bytes
from .config import logging
logger = logging.getLogger('parser-engine')

def pretty_dict_str(data):
    return '\n'.join([str(k) + ':\t' + str(v) for k, v in data.items()])


def log(level, data, *msgs, **kwargs):
    logger.log(level, '%s %s %s', str(data), ' '.join([str(msg) for msg in msgs]), pretty_dict_str(kwargs))


def info(data, *msgs, **kwargs):
    log(logging.INFO, data, *msgs, **kwargs)


def debug(data, *msgs, **kwargs):
    log(logging.DEBUG, data, *msgs, **kwargs)


def warning(data, *msgs, **kwargs):
    log(logging.WARNING, data, *msgs, **kwargs)


def error(data, *msgs, **kwargs):
    log(logging.ERROR, data, *msgs, **kwargs)