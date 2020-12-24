# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Dev\python\django-quickview\docs\examplesite\quickview\exceptions.py
# Compiled at: 2013-02-25 04:29:52
# Size of source mod 2**32: 200 bytes


class PreSaveException(Exception):
    pass


class PostSaveException(Exception):
    pass


class PreDeleteException(Exception):
    pass


class PostDeleteException(Exception):
    pass