# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/flatlibfr/predictives/primarydirections.py
# Compiled at: 2019-10-17 02:47:28
# Size of source mod 2**32: 9967 bytes
"""
    This file is part of flatlib - (C) FlatAngle
    Author: João Ventura (flatangleweb@gmail.com)
    flatlibfr translation of const by Stéphane Bressani (s.bressani@bluewin.ch)

    This module implements the Primary Directions
    method.

    Default assumptions:
    - only directions with the primary motion (direct)
    - only semi-arc method
    - in-zodiaco aspects of promissors to significators
    - in-mundo directions uses latitude of both promissors and significators
    
"""
from flatlibfr import angle
from flatlibfr import utils
from flatlibfr import const
from flatlibfr.dignities import tables

def arc(pRA, pDecl, sRA, sDecl, mcRA, lat):
    """ Returns the arc of direction between a Promissor 
    and Significator. It uses the generic proportional 
    semi-arc method.
    
    """
    pDArc, pNArc = utils.dnarcs(pDecl, lat)
    sDArc, sNArc = utils.dnarcs(sDecl, lat)
    mdRA = mcRA
    sArc = sDArc
    pArc = pDArc
    if not utils.isAboveHorizon(sRA, sDecl, mcRA, lat):
        mdRA = angle.norm(mcRA + 180)
        sArc = sNArc
        pArc = pNArc
    pDist = angle.closestdistance(mdRA, pRA)
    sDist = angle.closestdistance(mdRA, sRA)
    if pDist < sDist:
        pDist += 360
    sPropDist = sDist / (sArc / 2.0)
    pPropDist = pDist / (pArc / 2.0)
    return (pPropDist - sPropDist) * (pArc / 2.0)


def getArc(prom, sig, mc, pos, zerolat):
    """ Returns the arc of direction between a promissor
    and a significator. Arguments are also the MC, the
    geoposition and zerolat to assume zero ecliptical 
    latitudes.
    
    ZeroLat true => inZodiaco, false => inMundo
    
    """
    pRA, pDecl = prom.eqCoords(zerolat)
    sRa, sDecl = sig.eqCoords(zerolat)
    mcRa, mcDecl = mc.eqCoords()
    return arc(pRA, pDecl, sRa, sDecl, mcRa, pos.lat)


class PrimaryDirections:
    __doc__ = ' This class represents the Primary Directions\n    for a Chart.\n    \n    Given the complexity of all possible combinations,\n    this class encodes the objects in the following\n    functions:\n    \n    T() - Returns a term\n    A() - Returns the antiscia\n    C() - Returns the contra antiscia\n    D() - Returns the dexter aspect\n    S() - Returns the sinister aspect\n    N() - Returns the conjunction or opposition aspect\n    \n    '
    SIG_HOUSES = []
    SIG_ANGLES = [
     const.ASC, const.MC]
    SIG_OBJECTS = [
     const.SUN, const.MOON, const.MERCURY,
     const.VENUS, const.MARS, const.JUPITER,
     const.SATURN, const.PARS_FORTUNA,
     const.NORTH_NODE, const.SOUTH_NODE]
    MAX_ARC = 100

    def __init__(self, chart):
        self.chart = chart
        self.lat = chart.pos.lat
        mc = self.chart.getAngle(const.MC)
        self.mcRA = mc.eqCoords()[0]
        self.terms = self._buildTerms()

    def _buildTerms(self):
        """ Builds a data structure indexing the terms
        longitude by sign and object.
        
        """
        termLons = tables.termLons(tables.EGYPTIAN_TERMS)
        res = {}
        for ID, sign, lon in termLons:
            try:
                res[sign][ID] = lon
            except KeyError:
                res[sign] = {}
                res[sign][ID] = lon

        return res

    def G(self, ID, lat, lon):
        """ Creates a generic entry for an object. """
        eqM = utils.eqCoords(lon, lat)
        eqZ = eqM
        if lat != 0:
            eqZ = utils.eqCoords(lon, 0)
        return {'id':ID, 
         'lat':lat, 
         'lon':lon, 
         'ra':eqM[0], 
         'decl':eqM[1], 
         'raZ':eqZ[0], 
         'declZ':eqZ[1]}

    def T(self, ID, sign):
        """ Returns the term of an object in a sign. """
        lon = self.terms[sign][ID]
        ID = 'T_%s_%s' % (ID, sign)
        return self.G(ID, 0, lon)

    def A(self, ID):
        """ Returns the Antiscia of an object. """
        obj = self.chart.getObject(ID).antiscia()
        ID = 'A_%s' % ID
        return self.G(ID, obj.lat, obj.lon)

    def C(self, ID):
        """ Returns the CAntiscia of an object. """
        obj = self.chart.getObject(ID).cantiscia()
        ID = 'C_%s' % ID
        return self.G(ID, obj.lat, obj.lon)

    def D(self, ID, asp):
        """ Returns the dexter aspect of an object. """
        obj = self.chart.getObject(ID).copy()
        obj.relocate(obj.lon - asp)
        ID = 'D_%s_%s' % (ID, asp)
        return self.G(ID, obj.lat, obj.lon)

    def S(self, ID, asp):
        """ Returns the sinister aspect of an object. """
        obj = self.chart.getObject(ID).copy()
        obj.relocate(obj.lon + asp)
        ID = 'S_%s_%s' % (ID, asp)
        return self.G(ID, obj.lat, obj.lon)

    def N(self, ID, asp=0):
        """ Returns the conjunction or opposition aspect 
        of an object. 
        
        """
        obj = self.chart.get(ID).copy()
        obj.relocate(obj.lon + asp)
        ID = 'N_%s_%s' % (ID, asp)
        return self.G(ID, obj.lat, obj.lon)

    def _arc(self, prom, sig):
        """ Computes the in-zodiaco and in-mundo arcs 
        between a promissor and a significator.
        
        """
        arcm = arc(prom['ra'], prom['decl'], sig['ra'], sig['decl'], self.mcRA, self.lat)
        arcz = arc(prom['raZ'], prom['declZ'], sig['raZ'], sig['declZ'], self.mcRA, self.lat)
        return {'arcm':arcm, 
         'arcz':arcz}

    def getArc(self, prom, sig):
        """ Returns the arcs between a promissor and
        a significator. Should uses the object creation 
        functions to build the objects.
        
        """
        res = self._arc(prom, sig)
        res.update({'prom':prom['id'], 
         'sig':sig['id']})
        return res

    def _elements(self, IDs, func, aspList):
        """ Returns the IDs as objects considering the
        aspList and the function.
        
        """
        res = []
        for asp in aspList:
            if asp in (0, 180):
                if func == self.N:
                    res.extend([func(ID, asp) for ID in IDs])
                else:
                    res.extend([func(ID) for ID in IDs])
            else:
                res.extend([self.D(ID, asp) for ID in IDs])
                res.extend([self.S(ID, asp) for ID in IDs])

        return res

    def _terms(self):
        """ Returns a list with the objects as terms. """
        res = []
        for sign, terms in self.terms.items():
            for ID, lon in terms.items():
                res.append(self.T(ID, sign))

        return res

    def getList(self, aspList):
        """ Returns a sorted list with all
        primary directions. 
        
        """
        objects = self._elements(self.SIG_OBJECTS, self.N, [0])
        houses = self._elements(self.SIG_HOUSES, self.N, [0])
        angles = self._elements(self.SIG_ANGLES, self.N, [0])
        significators = objects + houses + angles
        objects = self._elements(self.SIG_OBJECTS, self.N, aspList)
        terms = self._terms()
        antiscias = self._elements(self.SIG_OBJECTS, self.A, [0])
        cantiscias = self._elements(self.SIG_OBJECTS, self.C, [0])
        promissors = objects + terms + antiscias + cantiscias
        res = []
        for prom in promissors:
            for sig in significators:
                if prom['id'] == sig['id']:
                    continue
                arcs = self._arc(prom, sig)
                for x, y in (('arcm', 'M'), ('arcz', 'Z')):
                    arc = arcs[x]
                    if 0 < arc < self.MAX_ARC:
                        res.append([
                         arcs[x],
                         prom['id'],
                         sig['id'],
                         y])

        return sorted(res)


class PDTable:
    __doc__ = ' Represents the Primary Directions table\n    for a chart.\n\n    '

    def __init__(self, chart, aspList=const.MAJOR_ASPECTS):
        pd = PrimaryDirections(chart)
        self.table = pd.getList(aspList)

    def view(self, arcmin, arcmax):
        """ Returns the directions within the
        min and max arcs.

        """
        res = []
        for direction in self.table:
            if arcmin < direction[0] < arcmax:
                res.append(direction)

        return res

    def bySignificator(self, ID):
        """ Returns all directions to a significator. """
        res = []
        for direction in self.table:
            if ID in direction[2]:
                res.append(direction)

        return res

    def byPromissor(self, ID):
        """ Returns all directions to a promissor. """
        res = []
        for direction in self.table:
            if ID in direction[1]:
                res.append(direction)

        return res