# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vmcontroller/common/exceptions.py
# Compiled at: 2011-03-04 15:52:41
"""
Exceptions
"""

class NoSuchVirtualMachine(Exception):

    def __init__(self, msg):
        self._msg = msg

    def __str__(self):
        return 'No VM by the name/id %s found' % self._msg


class ConfigError(Exception):

    def __init__(self, msg):
        self._msg = msg

    def __str__(self):
        return 'Configuration error: %s' % self._msg


class NotInitialized(Exception):

    def __init__(self, msg):
        self._msg = msg

    def __str__(self):
        return "Instance isn't fully initialized: %s" % self._msg