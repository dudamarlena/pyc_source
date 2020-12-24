# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/core/BaseAbbreviations.py
# Compiled at: 2019-12-11 16:37:48
"""Base classes for handling the abbrevations."""
from .BaseTables import LookupHints

class AbbrevMeta(type):
    """Meta class for the abbreviation classes"""

    def __init__(cls, _sName, _aBases, _dDict):
        if cls.dKeys:
            cls.make_lookup()

    def make_lookup(cls):
        """Create a lookup table for the class."""
        cls._dLook = {}
        for sKey, aAlts in cls.dKeys.iteritems():
            cls._dLook[sKey] = sKey
            for sAlt in aAlts:
                cls._dLook[sAlt] = sKey


class AbbreviationLookup(object):
    """Base class for specific abbreviation tables."""
    __metaclass__ = AbbrevMeta
    dKeys = None

    @classmethod
    def canonical(cls, sName):
        """Translate a possibly abbreviated name into a canonical one.
           """
        return cls._dLook[sName]

    @classmethod
    def fullname(cls, sCanonical):
        """Translate a canonical name into a full name.
           """
        raise NotImplementedError

    @classmethod
    def shortname(cls, sCanonical):
        """Translate a canonical name into a short name.
           """
        raise NotImplementedError


class DatabaseAbbreviation(object):
    """Base class for database backed abbrevations"""
    _dLook = {}
    _dLookupPrefix = {}
    _dReversePrefix = {}
    _dReverse = {}
    sLookupDomain = None

    @classmethod
    def make_lookup(cls):
        """Create a lookup table for the class."""
        cls._dLook = {}
        cls._dPrefix = {}
        cls._dReversePrefix = {}
        cls._dReverse = {}
        for oLookup in LookupHints.selectBy(domain=cls.sLookupDomain):
            cls._dLook[oLookup.value] = oLookup.value
            if oLookup.lookup.startswith('Prefix:'):
                sPrefix = oLookup.lookup.replace('Prefix:', '')
                cls._dPrefix[sPrefix] = oLookup.value
            elif oLookup.lookup.startswith('ReversePrefix:'):
                sPrefix = oLookup.lookup.replace('ReversePrefix:', '')
                cls._dReversePrefix[sPrefix] = oLookup.value
            else:
                cls._dLook[oLookup.lookup] = oLookup.value
                if oLookup.lookup != oLookup.value:
                    cls._dReverse.setdefault(oLookup.value, oLookup.lookup)

    @classmethod
    def canonical(cls, sName):
        """Translate a possibly abbreviated name into a canonical one.
           """
        for sPrefix, sLookup in cls._dPrefix.items():
            if sName.startswith(sPrefix):
                return sLookup

        return cls._dLook[sName]

    @classmethod
    def shortname(cls, sCanonical):
        """Translate a canonical name into a short name.
           """
        for sPrefix, sLookup in cls._dReversePrefix.items():
            if sCanonical.startswith(sPrefix):
                return sLookup

        if sCanonical in cls._dReverse and cls._dReverse[sCanonical]:
            return cls._dReverse[sCanonical]
        return sCanonical


class CardTypes(DatabaseAbbreviation):
    """Card Types Abbrevations"""
    sLookupDomain = 'CardTypes'


class Expansions(DatabaseAbbreviation):
    """Expansion Abbrevations"""
    sLookupDomain = 'Expansions'

    @classmethod
    def canonical(cls, sName):
        """Translate, using prefixes if specified"""
        try:
            sResult = super(Expansions, cls).canonical(sName)
        except KeyError:
            sResult = cls._dLook[sName] = sName

        return sResult


class Rarities(DatabaseAbbreviation):
    """Card rarity abbrevations"""
    sLookupDomain = 'Rarities'

    @classmethod
    def canonical(cls, sName):
        """Lookup rarity"""
        try:
            sResult = super(Rarities, cls).canonical(sName)
        except KeyError:
            sResult = cls._dLook[sName] = 'Unknown'

        return sResult