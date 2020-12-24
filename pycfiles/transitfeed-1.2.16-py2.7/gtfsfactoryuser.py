# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/transitfeed/gtfsfactoryuser.py
# Compiled at: 2018-01-24 00:52:58


class GtfsFactoryUser(object):
    """Base class for objects that must store a GtfsFactory in order to
     be able to instantiate Gtfs classes.

     If a non-default GtfsFactory is to be used, it must be set explicitly."""
    _gtfs_factory = None

    def GetGtfsFactory(self):
        """Return the object's GTFS Factory.

    Returns:
        The GTFS Factory that was set for this object. If none was explicitly
        set, it first sets the object's factory to transitfeed's GtfsFactory
        and returns it"""
        if self._gtfs_factory is None:
            import gtfsfactory
            self._gtfs_factory = gtfsfactory.GetGtfsFactory()
        return self._gtfs_factory

    def SetGtfsFactory(self, factory):
        self._gtfs_factory = factory