# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kvlayer/_exceptions.py
# Compiled at: 2015-07-31 13:31:44
"""Exceptions for :mod:`kvlayer`.

.. This software is released under an MIT/X11 open source license.
   Copyright 2012-2014 Diffeo, Inc.

"""

class KVLayerError(Exception):
    """Base class for all :mod:`kvlayer` exceptions."""
    pass


class ConfigurationError(KVLayerError):
    """An invalid value was passed to an object.

    The value is probably something user-provided, such as the name of
    the storage backend.  This error is raised if the invalid value is
    not detected until code is being executed.  If the value can be
    detected during the :mod:`yakonfig` configuration phase, then
    :class:`yakonfig.ConfigurationError` will be raised there instead.

    """
    pass


class ProgrammerError(KVLayerError):
    """The API was used incorrectly."""
    pass


class StorageClosed(KVLayerError):
    """A storage object was used after it was explicitly closed."""
    pass


class DatabaseEmpty(KVLayerError):
    pass


class BadKey(KVLayerError):
    """A key value passed to a kvlayer function was not of the correct form.

    Keys must be tuples of a fixed length and with specific types.
    The length of the tuple is specified in the initial call to
    :meth:`kvlayer._abstract_storage.AbstractStorage.setup_namespace`.

    """
    pass


class SerializationError(KVLayerError):
    """Converting between an item and a serialized form failed."""
    pass