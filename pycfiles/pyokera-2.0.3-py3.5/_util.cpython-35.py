# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/okera/_util.py
# Compiled at: 2020-02-27 14:06:57
# Size of source mod 2**32: 1569 bytes
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
    msg = '{0} functionality in pyokera is now deprecated and will be removed in a future release'.format(functionality)
    if alternative:
        msg += '; Please use {0} instead.'.format(alternative)
    warnings.warn(msg, Warning)