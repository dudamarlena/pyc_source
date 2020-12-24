# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\wl\errors.py
# Compiled at: 2017-11-03 06:51:45
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
__author__ = b'd01'
__email__ = b'jungflor@gmail.com'
__copyright__ = b'Copyright (C) 2017, Florian JUNG'
__license__ = b'MIT'
__version__ = b'0.1.0'
__date__ = b'2017-11-01'
DATE_INVALID = -1
DATE_OFR_YEAR = -10
DATE_OFR_MONTH = -20
DATE_OFR_DAY = -30
DATE_OUT_OF_PLAN = -4001
TIME_INVALID = -1
TIME_OFR_HOUR = -10
TIME_OFR_MINUTE = -20

class WL_Exception(Exception):
    """ Base WL exception """
    pass


class RequestException(WL_Exception):
    """ Error while making request """
    pass


class ProtocolViolation(Exception):
    """ Response did not follow documentation """
    pass