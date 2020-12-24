# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\exceptions.py
# Compiled at: 2018-01-15 10:37:44
# Size of source mod 2**32: 1015 bytes


class NamespaceRedefineException(Exception):
    pass


class PrefixRedefineException(Exception):
    pass


class UnattachedElementException(Exception):
    pass


class UnknownNamespaceException(Exception):
    pass


class UnknownPrefixException(Exception):
    pass