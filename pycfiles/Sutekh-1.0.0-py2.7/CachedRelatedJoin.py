# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/core/CachedRelatedJoin.py
# Compiled at: 2019-12-11 16:37:48
"""Implement RelatedJoin with caches"""
from sqlobject import joins
from sqlobject.sqlbuilder import Table, Select

class SOCachedRelatedJoin(joins.SORelatedJoin):
    """Version of RelatedJoin that caches the lookup of related objects.

       Updates to the database require explicitly flushing the cache on
       each join. E.g.:

       for oJoin in AbstractCard.sqlmeta.joins:
         if type(oJoin) is SOCachedRelatedJoin:
            oJoin.flush_cache()
       """

    def __init__(self, *aArgs, **kwargs):
        super(SOCachedRelatedJoin, self).__init__(*aArgs, **kwargs)
        self._dJoinCache = {}
        self._oOtherJoin = None
        self._bOtherJoinCached = None
        return

    def _find_other_join(self):
        """Locate the equivalent join on the other class."""
        if self._oOtherJoin is None:
            aJoins = [ oJ for oJ in self.otherClass.sqlmeta.joins if oJ.otherClass is self.soClass and oJ.intermediateTable == self.intermediateTable and oJ.otherColumn == self.joinColumn
                     ]
            assert len(aJoins) == 1
            self._oOtherJoin = aJoins[0]
            self._bOtherJoinCached = isinstance(self._oOtherJoin, SOCachedRelatedJoin)
        return

    def flush_cache(self):
        """Flush the contents of the cache."""
        self._dJoinCache = {}

    def init_cache(self):
        """Initialise the cache with the data from the database."""
        self._find_other_join()
        oIntermediateTable = Table(self.intermediateTable)
        oJoinColumn = getattr(oIntermediateTable, self.joinColumn)
        oOtherColumn = getattr(oIntermediateTable, self.otherColumn)
        oConn = self.soClass._connection
        for oId, oOtherId in oConn.queryAll(repr(Select((oJoinColumn, oOtherColumn)))):
            oInst = self.soClass.get(oId, oConn)
            oOther = self.otherClass.get(oOtherId, oConn)
            self._dJoinCache.setdefault(oInst, [])
            self._dJoinCache[oInst].append(oOther)

        for oInst in self._dJoinCache:
            self._dJoinCache[oInst] = self._applyOrderBy(self._dJoinCache[oInst], self.otherClass)

    def invalidate_cache_item(self, oInst, oOther, bDoOther=True):
        """Invalidate a cache item and its equivalent in the other join."""
        if oInst in self._dJoinCache:
            del self._dJoinCache[oInst]
        if bDoOther and self._bOtherJoinCached:
            self._find_other_join()
            self._oOtherJoin.invalidate_cache_item(oOther, oInst, bDoOther=False)

    def performJoin(self, oInst):
        """Return the join the result, from the cache if possible."""
        if oInst not in self._dJoinCache:
            self._dJoinCache[oInst] = joins.SORelatedJoin.performJoin(self, oInst)
        return self._dJoinCache[oInst]

    def add(self, oInst, oOther):
        """Add an item to the join."""
        self.invalidate_cache_item(oInst, oOther)
        super(SOCachedRelatedJoin, self).add(oInst, oOther)

    def remove(self, oInst, oOther):
        """Remove an item from the join."""
        self.invalidate_cache_item(oInst, oOther)
        super(SOCachedRelatedJoin, self).remove(oInst, oOther)


class CachedRelatedJoin(joins.RelatedJoin):
    """Provide CacheRelatedJoin object to Sutekh"""
    baseClass = SOCachedRelatedJoin