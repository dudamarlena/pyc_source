# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/core/SutekhObjectCache.py
# Compiled at: 2019-12-11 16:37:56
"""Cache various objects used by sutekh to speed up database queries."""
from sutekh.core.SutekhTables import SutekhAbstractCard, Clan, Discipline, DisciplinePair, Sect, Title, Creed, Virtue
from sutekh.base.core.ObjectCache import ObjectCache

class SutekhObjectCache(ObjectCache):
    """Add Sutekh specific classes to the generic database cache.
       """

    def __init__(self):
        aExtraTypesToCache = [
         Discipline, DisciplinePair, Clan,
         Creed, Virtue, Sect, Title,
         SutekhAbstractCard]
        super(SutekhObjectCache, self).__init__(aExtraTypesToCache)