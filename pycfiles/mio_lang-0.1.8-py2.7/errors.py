# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/prologic/work/mio/mio/errors.py
# Compiled at: 2013-12-04 07:14:58


class Error(Exception):
    """Error"""

    def __init__(self, *args):
        super(Error, self).__init__(*args)
        self.stack = []


class AttributeError(Error):
    """AttributeError"""
    pass


class ImportError(Error):
    """ImportError"""
    pass


class IndexError(Error):
    """IndexError"""
    pass


class KeyError(Error):
    """KeyError"""
    pass


class TypeError(Error):
    """TypeError"""
    pass


class StopIteration(Error):
    """StopIteration"""
    pass


class UserError(Error):
    """UserError"""
    pass