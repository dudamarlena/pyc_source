# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/boldfield/Work/s3-encryption/s3_encryption/exceptions.py
# Compiled at: 2016-05-17 02:23:27


class ArgumentError(Exception):
    """Raised when incorrect arguments are passed to constructors.
    """
    pass


class IncompleteMetadataError(Exception):
    """Raised when incomplete  metadata is used to construct request envelope.
    """
    pass