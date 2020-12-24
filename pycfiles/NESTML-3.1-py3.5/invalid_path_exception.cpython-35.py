# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/exceptions/invalid_path_exception.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 891 bytes


class InvalidPathException(Exception):
    __doc__ = '\n    This exception is thrown whenever neither a file nor a dir has been handed over. This should not happen.\n    '