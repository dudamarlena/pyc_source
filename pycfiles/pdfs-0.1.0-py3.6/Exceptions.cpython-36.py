# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pdfs/Exceptions.py
# Compiled at: 2017-08-14 16:20:11
# Size of source mod 2**32: 180 bytes


class AbortException(Exception):
    pass


class WorkExistsException(Exception):
    pass


class UserException(Exception):
    pass


class RepositoryException(Exception):
    pass