# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/core/Abbreviations.py
# Compiled at: 2019-12-11 16:37:56
"""A catalog of common abbreviations for VtES terms.
   """
from sutekh.base.core.BaseAbbreviations import AbbreviationLookup, DatabaseAbbreviation
from sutekh.base.core.BaseTables import LookupHints

class Clans(DatabaseAbbreviation):
    """Standard names and common abbreviations for the VtES clans."""
    sLookupDomain = 'Clans'


class Creeds(DatabaseAbbreviation):
    """The Imbued creeds."""
    sLookupDomain = 'Creeds'


class Disciplines(DatabaseAbbreviation):
    """Standard abbreviations and names for the VtES disciplines."""
    sLookupDomain = 'Disciplines'

    @classmethod
    def fullname(cls, sShortName):
        """Return the full name for the given abbreviation."""
        sFullName = None
        sCanonical = cls.canonical(sShortName)
        for oLookup in LookupHints.selectBy(domain=cls.sLookupDomain):
            if oLookup.value == sCanonical and len(oLookup.lookup) > 3:
                sFullName = oLookup.lookup
                break

        return sFullName


class Sects(DatabaseAbbreviation):
    """Common strings for the different sects."""
    sLookupDomain = 'Sects'


class Titles(AbbreviationLookup):
    """Common strings used to refer to the different titles."""
    dKeys = {'Primogen': [], 'Prince': [], 'Justicar': [], 'Inner Circle': [], 'Bishop': [], 'Archbishop': [], 'Priscus': [], 'Cardinal': [], 'Regent': [], 'Independent with 1 vote': [], 'Independent with 2 votes': [], 'Independent with 3 votes': [], 'Magaji': [], 'Baron': []}
    dVoteValues = {'Primogen': 1, 
       'Prince': 2, 'Justicar': 3, 'Inner Circle': 4, 
       'Bishop': 1, 
       'Archbishop': 2, 'Priscus': 3, 'Cardinal': 3, 
       'Regent': 4, 'Independent with 1 vote': 1, 
       'Independent with 2 votes': 2, 
       'Independent with 3 votes': 3, 
       'Magaji': 2, 
       'Baron': 2}

    @classmethod
    def vote_value(cls, sTitle):
        """Get the vote value for the title"""
        return cls.dVoteValues[sTitle]


class Virtues(DatabaseAbbreviation):
    """Common abbreviations for Imbued Virtues"""
    sLookupDomain = 'Virtues'

    @classmethod
    def fullname(cls, sCanonical):
        """Return the canonical long name of the Virtue"""
        sFullName = None
        sCanonical = cls.canonical(sCanonical)
        for oLookup in LookupHints.selectBy(domain=cls.sLookupDomain):
            if oLookup.value == sCanonical and oLookup.lookup != sCanonical:
                sFullName = oLookup.lookup
                break

        return sFullName