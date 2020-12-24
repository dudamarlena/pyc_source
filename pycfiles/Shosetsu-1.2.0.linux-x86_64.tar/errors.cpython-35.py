# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.5/site-packages/Shosetsu/errors.py
# Compiled at: 2016-06-15 20:40:51
# Size of source mod 2**32: 1584 bytes


class Error(Exception):
    pass


class VNDBOneResult(Error):
    __doc__ = '\n    This exception is raised when we search for an item but only get on result so VNDB passes us directly to that content.\n\n    Attributes:\n            expression - The input name that returned only one result\n            vnid - The ID of this result\n    '

    def __init__(self, expression, vnid):
        self.expression = expression
        self.vnid = vnid

    def __str__(self):
        return 'Search {} only had one result at ID {}.'.format(self.expression, self.vnid)

    def __repr__(self):
        return 'Search {} only had one result at ID {}.'.format(self.expression, self.vnid)


class VNDBNoResults(Error):
    __doc__ = '\n    This exception is raised when we search for content but find no results\n\n    Attributes:\n            expression - The input name that returned no results\n    '

    def __init__(self, expression):
        self.expression = expression

    def __str__(self):
        return 'Search {} has no results.'.format(self.expression)

    def __repr__(self):
        return 'Search {} has no results.'.format(self.expression)


class VNDBBadStype(Error):
    __doc__ = '\n    This exception is raised when a bad search type is passed\n\n    Attributes:\n            expression - The input name that returned only one result\n    '

    def __init__(self, expression):
        self.expression = expression

    def __str__(self):
        return '{} is not a valid search type.'.format(self.expression)

    def __repr__(self):
        return '{} is not a valid search type.'.format(self.expression)