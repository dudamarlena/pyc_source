# uncompyle6 version 3.7.4
# PyPy Python bytecode 3.2 (3187)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/andrewcrosio/projects/pathresolver/pypy3/site-packages/pathresolver/exceptions.py
# Compiled at: 2015-04-17 13:50:21


class PathResolverError(Exception):
    pass


class UnableToResolve(PathResolverError):
    pass


class NoMatchError(PathResolverError):

    def __init__(self, arg, root, index=0):
        self.root = root
        self.index = index
        super(NoMatchError, self).__init__(arg)