# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/cerebro/_util.py
# Compiled at: 2018-05-22 15:24:37
# Size of source mod 2**32: 1577 bytes
from __future__ import absolute_import
import builtins, warnings, logging
from logging import NullHandler
import string, random, six

def get_logger_and_init_null(logger_name):
    logger = logging.getLogger(logger_name)
    logger.addHandler(NullHandler())
    return logger


log = get_logger_and_init_null(__name__)

def _random_id(prefix='', length=8):
    return prefix + ''.join(random.sample(string.ascii_uppercase, length))


def to_bytes(text):
    if isinstance(text, builtins.bytes):
        return text
    if isinstance(text, list):
        return builtins.bytes(text)
    return builtins.bytes(str(text), encoding='utf-8')


def _escape(s):
    e = s
    e = e.replace('\\', '\\\\')
    e = e.replace('\n', '\\n')
    e = e.replace('\r', '\\r')
    e = e.replace("'", "\\'")
    e = e.replace('"', '\\"')
    log.debug('%s => %s', s, e)
    return e


def _py_to_sql_string(value):
    if value is None:
        return 'NULL'
    if isinstance(value, six.string_types):
        return "'" + _escape(value) + "'"
    return str(value)


def warn_deprecate(functionality='This', alternative=None):
    msg = '{0} functionality in pycerebro is now deprecated and will be removed in a future release'.format(functionality)
    if alternative:
        msg += '; Please use {0} instead.'.format(alternative)
    warnings.warn(msg, Warning)