# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/baroque/exceptions/configuration.py
# Compiled at: 2017-03-03 13:38:20
# Size of source mod 2**32: 231 bytes


class ConfigurationNotFoundError(Exception):
    __doc__ = 'Raised when configuration source file is not available'


class ConfigurationParseError(Exception):
    __doc__ = 'Raised on failures in parsing configuration data'