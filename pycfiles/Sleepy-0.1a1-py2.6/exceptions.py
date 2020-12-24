# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-i386/egg/sleepy/exceptions.py
# Compiled at: 2010-12-27 10:39:36


class InvalidPathException(Exception):
    pass


class PathException(Exception):
    pass


class NotFoundException(Exception):
    pass