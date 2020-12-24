# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fms/utils/exceptions.py
# Compiled at: 2009-02-06 13:25:36
"""
FMS custom exceptions classes
"""
import logging

class MissingParameter(Exception):
    """
    Custom exception class for missing parameter in
    simulation config file.
    """

    def __init__(self, msg):
        logger = logging.getLogger('fms.utils.exceptions')
        logger.exception('Missing parameter: %s' % msg)
        self.msg = msg

    def __str__(self):
        return self.msg


class NotAnInteger(Exception):
    """
    Custom exception class: value should be an integer.
    """

    def __init__(self, value):
        logger = logging.getLogger('fms.utils.exceptions')
        logger.exception('Not an integer: %s' % value)
        self.value = value

    def __str__(self):
        return self.value