# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/flatlibfr/tools/chartdynamics.py
# Compiled at: 2019-10-17 02:47:28
# Size of source mod 2**32: 4877 bytes
"""
    This file is part of flatlib - (C) FlatAngle
    Author: João Ventura (flatangleweb@gmail.com)
    
    
    This module implements the ChartDynamics class for
    handling some of the dynamics of an astrology Chart.
  
"""
from flatlibfr import const
from flatlibfr import aspects
from flatlibfr.dignities import essential

class ChartDynamics:

    def __init__(self, chart):
        self.chart = chart

    def inDignities(self, idA, idB):
        """ Returns the dignities of A which belong to B. """
        objA = self.chart.get(idA)
        info = essential.getInfo(objA.sign, objA.signlon)
        return [dign for dign, ID in info.items() if ID == idB]

    def receives(self, idA, idB):
        """ Returns the dignities where A receives B.
        A receives B when (1) B aspects A and (2) B is in 
        dignities of A.

        """
        objA = self.chart.get(idA)
        objB = self.chart.get(idB)
        asp = aspects.isAspecting(objB, objA, const.MAJOR_ASPECTS)
        if asp:
            return self.inDignities(idB, idA)
        return []

    def disposits(self, idA, idB):
        """ Returns the dignities where A is dispositor of B. """
        return self.inDignities(idB, idA)

    def mutualReceptions(self, idA, idB):
        """ Returns all pairs of dignities in mutual reception. """
        AB = self.receives(idA, idB)
        BA = self.receives(idB, idA)
        return [(a, b) for a in AB for b in BA]

    def reMutualReceptions(self, idA, idB):
        """ Returns ruler and exaltation mutual receptions. """
        mr = self.mutualReceptions(idA, idB)
        filter_ = ['ruler', 'exalt']
        return [(a, b) for a, b in mr if a in filter_ if b in filter_]

    def validAspects(self, ID, aspList):
        """ Returns a list with the aspects an object 
        makes with the other six planets, considering a
        list of possible aspects. 
        
        """
        obj = self.chart.getObject(ID)
        res = []
        for otherID in const.LIST_SEVEN_PLANETS:
            if ID == otherID:
                continue
            otherObj = self.chart.getObject(otherID)
            aspType = aspects.aspectType(obj, otherObj, aspList)
            if aspType != const.NO_ASPECT:
                res.append({'id':otherID, 
                 'asp':aspType})

        return res

    def aspectsByCat(self, ID, aspList):
        """ Returns the aspects an object makes with the
        other six planets, separated by category (applicative,
        separative, exact). 
        Aspects must be within orb of the object.
        
        """
        res = {const.APPLICATIVE: [], 
         const.SEPARATIVE: [], 
         const.EXACT: [], 
         const.NO_MOVEMENT: []}
        objA = self.chart.getObject(ID)
        valid = self.validAspects(ID, aspList)
        for elem in valid:
            objB = self.chart.getObject(elem['id'])
            asp = aspects.getAspect(objA, objB, aspList)
            role = asp.getRole(objA.id)
            if role['inOrb']:
                movement = role['movement']
                res[movement].append({'id':objB.id, 
                 'asp':asp.type, 
                 'orb':asp.orb})

        return res

    def immediateAspects(self, ID, aspList):
        """ Returns the last separation and next application
        considering a list of possible aspects.

        """
        asps = self.aspectsByCat(ID, aspList)
        applications = asps[const.APPLICATIVE]
        separations = asps[const.SEPARATIVE]
        exact = asps[const.EXACT]
        applications = applications + [val for val in exact if val['orb'] >= 0]
        applications = sorted(applications, key=(lambda var: var['orb']))
        separations = sorted(separations, key=(lambda var: var['orb']))
        return (
         separations[0] if separations else None,
         applications[0] if applications else None)

    def isVOC(self, ID):
        """ Returns if a planet is Void of Course.
        A planet is not VOC if has any exact or applicative aspects
        ignoring the sign status (associate or dissociate).
        
        """
        asps = self.aspectsByCat(ID, const.MAJOR_ASPECTS)
        applications = asps[const.APPLICATIVE]
        exacts = asps[const.EXACT]
        return len(applications) == 0 and len(exacts) == 0