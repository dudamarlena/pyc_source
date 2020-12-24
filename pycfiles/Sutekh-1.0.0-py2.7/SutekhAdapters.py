# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/core/SutekhAdapters.py
# Compiled at: 2019-12-11 16:37:56
"""The singledispatch adapters for Sutekh"""
from singledispatch import singledispatch
from sutekh.base.core.BaseAdapters import Adapter, StrAdaptMeta, fail_adapt, passthrough
from sutekh.core.SutekhTables import Clan, Creed, Discipline, DisciplinePair, Sect, Title, Virtue
from sutekh.core.Abbreviations import Clans, Creeds, Disciplines, Sects, Titles, Virtues

@singledispatch
def IDisciplinePair(oUnknown):
    """Default DisplincePair adapter"""
    return fail_adapt(oUnknown, 'DisciplinePair')


@singledispatch
def IDiscipline(oUnknown):
    """Default Displince adapter"""
    return fail_adapt(oUnknown, 'Discipline')


@singledispatch
def IClan(oUnknown):
    """Default Clan adapter"""
    return fail_adapt(oUnknown, 'Clan')


@singledispatch
def ISect(oUnknown):
    """Default Sect adapter"""
    return fail_adapt(oUnknown, 'Sect')


@singledispatch
def ITitle(oUnknown):
    """Default Title adapter"""
    return fail_adapt(oUnknown, 'Title')


@singledispatch
def ICreed(oUnknown):
    """Default Creed adapter"""
    return fail_adapt(oUnknown, 'Creed')


@singledispatch
def IVirtue(oUnknown):
    """Default Virtue adapter"""
    return fail_adapt(oUnknown, 'Virtue')


class ClanAdapter(Adapter):
    __metaclass__ = StrAdaptMeta

    @classmethod
    def lookup(cls, sName):
        return cls.fetch(Clans.canonical(sName), Clan)


IClan.register(Clan, passthrough)
IClan.register(basestring, ClanAdapter.lookup)

class CreedAdapter(Adapter):
    __metaclass__ = StrAdaptMeta

    @classmethod
    def lookup(cls, sName):
        return cls.fetch(Creeds.canonical(sName), Creed)


ICreed.register(Creed, passthrough)
ICreed.register(basestring, CreedAdapter.lookup)

class DisciplineAdapter(Adapter):
    __metaclass__ = StrAdaptMeta

    @classmethod
    def lookup(cls, sName):
        return cls.fetch(Disciplines.canonical(sName), Discipline)


IDiscipline.register(Discipline, passthrough)
IDiscipline.register(basestring, DisciplineAdapter.lookup)

class SectAdapter(Adapter):
    __metaclass__ = StrAdaptMeta

    @classmethod
    def lookup(cls, sName):
        return cls.fetch(Sects.canonical(sName), Sect)


ISect.register(Sect, passthrough)
ISect.register(basestring, SectAdapter.lookup)

class TitleAdapter(Adapter):
    __metaclass__ = StrAdaptMeta

    @classmethod
    def lookup(cls, sName):
        return cls.fetch(Titles.canonical(sName), Title)


ITitle.register(Title, passthrough)
ITitle.register(basestring, TitleAdapter.lookup)

class VirtueAdapter(Adapter):
    __metaclass__ = StrAdaptMeta

    @classmethod
    def lookup(cls, sName):
        return cls.fetch(Virtues.canonical(sName), Virtue)


IVirtue.register(Virtue, passthrough)
IVirtue.register(basestring, VirtueAdapter.lookup)

class DisciplinePairAdapter(Adapter):
    __dCache = {}

    @classmethod
    def make_object_cache(cls):
        cls.__dCache = {}

    @classmethod
    def lookup(cls, tData):
        oDis = IDiscipline(tData[0])
        sLevel = str(tData[1])
        oPair = cls.__dCache.get((oDis.id, sLevel), None)
        if oPair is None:
            oPair = DisciplinePair.selectBy(discipline=oDis, level=sLevel).getOne()
            cls.__dCache[(oDis.id, sLevel)] = oPair
        return oPair


IDisciplinePair.register(DisciplinePair, passthrough)
IDisciplinePair.register(tuple, DisciplinePairAdapter.lookup)