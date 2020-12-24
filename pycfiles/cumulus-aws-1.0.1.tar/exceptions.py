# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/sebastian/git/skymill/cumulus/cumulus/cumulus_ds/exceptions.py
# Compiled at: 2014-03-04 09:28:50


class ChecksumMismatchException(Exception):
    """ A checksum check has failed """


class ConfigurationException(Exception):
    """ Configuration exception """


class HookExecutionException(Exception):
    """ Failed to execute a hook """


class InvalidTemplateException(Exception):
    """ Invalid CloudFormation template """


class UnsupportedCompression(Exception):
    """ An unsupported compression format for the bundle found """