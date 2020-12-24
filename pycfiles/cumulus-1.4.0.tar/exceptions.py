# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sebastian/git/skymill/cumulus/cumulus/cumulus_ds/exceptions.py
# Compiled at: 2014-03-04 09:28:50


class ChecksumMismatchException(Exception):
    """ A checksum check has failed """
    pass


class ConfigurationException(Exception):
    """ Configuration exception """
    pass


class HookExecutionException(Exception):
    """ Failed to execute a hook """
    pass


class InvalidTemplateException(Exception):
    """ Invalid CloudFormation template """
    pass


class UnsupportedCompression(Exception):
    """ An unsupported compression format for the bundle found """
    pass