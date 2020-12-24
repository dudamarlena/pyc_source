# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/core/ObjectCache.py
# Compiled at: 2019-12-11 16:37:48
"""Base class for the generic database object cache."""
from .BaseTables import AbstractCard, RarityPair, Rarity, CardType, Expansion, Ruling, PhysicalCard, Keyword, Artist
from .DBUtility import init_cache

class ObjectCache(object):
    """Holds references to commonly used database objects so that they don't
       get removed from the cache during big reads.

       Including AbstractCard in the cache gives about a 40% speed up on
       filtering at the cost of using about 3MB extra memory.

       Including Ruling costs about an extra 1MB for no real speed up, but
       we threw it in anyway (on the assumption it may be useful sometime
       in the future).
       """

    def __init__(self, aExtraTypesToCache):
        self._dCache = {}
        aTypesToCache = [
         Rarity, Expansion, RarityPair, CardType,
         Ruling, Keyword, Artist, AbstractCard,
         PhysicalCard] + aExtraTypesToCache
        for cType in aTypesToCache:
            self._dCache[cType] = list(cType.select())

        init_cache()