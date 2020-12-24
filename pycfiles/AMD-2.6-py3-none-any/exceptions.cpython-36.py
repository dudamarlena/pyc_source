# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/phil/repos/python-amcrest/src/amcrest/exceptions.py
# Compiled at: 2019-05-14 22:48:33
# Size of source mod 2**32: 300 bytes
__doc__ = "\namcrest.exceptions\n\nThis module contains the set of amcrest's exceptions.\n"

class AmcrestError(Exception):
    """AmcrestError"""
    pass


class CommError(AmcrestError):
    """CommError"""
    pass


class LoginError(AmcrestError):
    """LoginError"""
    pass