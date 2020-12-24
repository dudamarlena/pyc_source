# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/core/BaseDBManagement.py
# Compiled at: 2019-12-11 16:37:48
"""Various generic things for handling complex database operations.

   These are used when upgrading the database or reloading the underlying
   abstract card set."""
from logging import Logger
from sqlobject import sqlhub
from .CardSetHolder import make_card_set_holder
from .BaseTables import PhysicalCardSet

class UnknownVersion(Exception):
    """Exception for versions we cannot handle"""

    def __init__(self, sTableName):
        Exception.__init__(self)
        self.sTableName = sTableName

    def __str__(self):
        return 'Unrecognised version for %s' % self.sTableName


def copy_to_new_abstract_card_db(oOrigConn, oNewConn, oCardLookup, oLogHandler=None):
    """Copy the card sets to a new Physical Card and Abstract Card List.

      Given an existing database, and a new database created from
      a new cardlist, copy the CardSets, going via CardSetHolders, so we
      can adapt to changed names, etc.
      """
    aPhysCardSets = []
    oOldConn = sqlhub.processConnection
    sqlhub.processConnection = oOrigConn
    oLogger = Logger('copy to new abstract card DB')
    if oLogHandler:
        oLogger.addHandler(oLogHandler)
        if hasattr(oLogHandler, 'set_total'):
            iTotal = 1 + PhysicalCardSet.select(connection=oOrigConn).count()
            oLogHandler.set_total(iTotal)
    aSets = list(PhysicalCardSet.select(connection=oOrigConn))
    bDone = False
    aDone = []
    while not bDone:
        aToDo = []
        for oSet in aSets:
            if oSet.parent is None or oSet.parent in aDone:
                oCS = make_card_set_holder(oSet)
                aPhysCardSets.append(oCS)
                aDone.append(oSet)
            else:
                aToDo.append(oSet)

        if not aToDo:
            bDone = True
        else:
            aSets = aToDo

    oLogger.info('Memory copies made')
    dLookupCache = {}
    sqlhub.processConnection = oNewConn
    for oSet in aPhysCardSets:
        oSet.create_pcs(oCardLookup, dLookupCache)
        oLogger.info('Physical Card Set: %s', oSet.name)
        sqlhub.processConnection.cache.clear()

    sqlhub.processConnection = oOldConn
    return (True, [])