# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.7.0-Power_Macintosh/egg/atomstorage/__init__.py
# Compiled at: 2006-08-11 05:04:56
from pkg_resources import iter_entry_points

def EntryManager(dsn):
    """
    Generic entry manager.

    This class delegates a connection to the proper manager.
    """
    (protocol, location) = dsn.split('://', 1)
    for entrypoint in iter_entry_points('atomstorage.backend'):
        if entrypoint.name == protocol:
            em = entrypoint.load()
            return em(location)

    raise Exception, 'No backend found for protocol "%s"!' % protocol