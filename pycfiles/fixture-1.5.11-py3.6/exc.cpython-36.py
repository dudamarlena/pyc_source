# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fixture/exc.py
# Compiled at: 2017-10-02 03:31:12
# Size of source mod 2**32: 1524 bytes
"""Fixture exceptions"""

class UninitializedError(Exception):
    pass


class DataSetActionException(Exception):
    __doc__ = '\n    An exception while performing some action with a DataSet.\n    \n    In addtion to ``etype`` and ``val`` adds these properties:\n    \n    ``dataset``\n        :class:`DataSet <fixture.dataset.DataSet>` that caused the exception\n        \n    ``key``\n        Key on DataSet row if there is one\n        \n    ``row``\n        :class:`DataRow <fixture.dataset.DataRow>` if there is one\n        \n    ``stored_object``\n        Stored object if there is one\n        \n    used by :mod:`fixture.loadable` classes\n    '

    def __init__(self, etype, val, dataset, key=None, row=None, stored_object=None):
        msg = 'in %s' % dataset
        if key or row:
            msg = "with '%s' of '%s' %s" % (key, row, msg)
        else:
            if stored_object:
                msg = 'with %s %s' % (stored_object, msg)
        Exception.__init__(self, '%s: %s (%s)' % (etype.__name__, val, msg))


class LoadError(DataSetActionException):
    __doc__ = '\n    An exception while loading data in DataSet.\n    \n    used by :mod:`fixture.loadable` classes\n    '


class UnloadError(DataSetActionException):
    __doc__ = '\n    An exception while unloading data from a DataSet.\n    \n    used by :mod:`fixture.loadable` classes\n    '


class StorageMediaNotFound(LookupError):
    __doc__ = '\n    Looking up a storable object failed.\n    \n    used by :mod:`fixture.loadable` classes\n    '