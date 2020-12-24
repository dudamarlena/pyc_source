# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/core/SutekhObjectMaker.py
# Compiled at: 2019-12-11 16:37:56
"""The Sutekh Card and related database objects creation helper"""
from sqlobject import SQLObjectNotFound
from sutekh.base.core.BaseAdapters import IAbstractCard
from sutekh.base.core.BaseObjectMaker import BaseObjectMaker
from sutekh.core.SutekhTables import SutekhAbstractCard, Clan, Creed, Discipline, DisciplinePair, Sect, Title, Virtue
from sutekh.core.SutekhAdapters import IClan, ICreed, IDiscipline, IDisciplinePair, ISect, ITitle, IVirtue
from sutekh.core.Abbreviations import Clans, Creeds, Disciplines, Sects, Titles, Virtues

class SutekhObjectMaker(BaseObjectMaker):
    """Creates all kinds of SutekhTables from simple strings.

       All the methods will return either a copy of an existing object
       or a new object.
       """

    def make_clan(self, sClan):
        return self._make_object(Clan, IClan, Clans, sClan, bShortname=True)

    def make_creed(self, sCreed):
        return self._make_object(Creed, ICreed, Creeds, sCreed, bShortname=True)

    def make_discipline(self, sDis):
        return self._make_object(Discipline, IDiscipline, Disciplines, sDis, bFullname=True)

    def make_sect(self, sSect):
        return self._make_object(Sect, ISect, Sects, sSect)

    def make_title(self, sTitle):
        return self._make_object(Title, ITitle, Titles, sTitle)

    def make_virtue(self, sVirtue):
        return self._make_object(Virtue, IVirtue, Virtues, sVirtue, bFullname=True)

    def make_abstract_card(self, sCard):
        try:
            return IAbstractCard(sCard)
        except SQLObjectNotFound:
            sName = sCard.strip()
            sCanonical = sName.lower()
            return SutekhAbstractCard(canonicalName=sCanonical, name=sName, text='')

    def make_discipline_pair(self, sDiscipline, sLevel):
        try:
            return IDisciplinePair((sDiscipline, sLevel))
        except SQLObjectNotFound:
            oDis = self.make_discipline(sDiscipline)
            return DisciplinePair(discipline=oDis, level=sLevel)