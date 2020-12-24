# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/flatlibfr/protocols/temperament.py
# Compiled at: 2019-10-17 02:47:28
# Size of source mod 2**32: 7854 bytes
"""
    This file is part of flatlib - (C) FlatAngle
    Author: João Ventura (flatangleweb@gmail.com)
    flatlibfr translation of const by Stéphane Bressani (s.bressani@bluewin.ch)

    This module implements the Temperament Traditional 
    Protocol.

    The Temperament protocol returns the temperament 
    scores given the characteristics of the objects 
    and other things which affects the Asc, the Moon 
    and the Sun Season.
    
"""
from flatlibfr import const, dignities
from flatlibfr import aspects
from flatlibfr import props
from flatlibfr.dignities import essential
ASC_SIGN = 'Asc Sign'
ASC_RULER = 'Asc Ruler'
ASC_RULER_SIGN = 'Asc Ruler Sign'
HOUSE1_PLANETS_IN = 'Planets in House1'
ASC_PLANETS_CONJ = 'Planets conj Asc'
ASC_PLANETS_ASP = 'Planets asp Asc'
MOON_SIGN = 'Moon Sign'
MOON_PHASE = 'Moon Phase'
MOON_DISPOSITOR_SIGN = 'Moon Dispositor Sign'
MOON_PLANETS_CONJ = 'Planets conj Moon'
MOON_PLANETS_ASP = 'Planets asp Moon'
SUN_SEASON = 'Sun season'
MOD_ASC = 'Asc'
MOD_ASC_RULER = 'Asc Ruler'
MOD_MOON = 'Moon'

def singleFactor(factors, chart, factor, obj, aspect=None):
    """" Single factor for the table. """
    objID = obj if type(obj) == str else obj.id
    res = {'factor':factor, 
     'objID':objID, 
     'aspect':aspect}
    if type(obj) == str:
        res['element'] = props.sign.element[obj]
    else:
        if objID == const.SUN:
            sunseason = props.sign.sunseason[obj.sign]
            res['sign'] = obj.sign
            res['sunseason'] = sunseason
            res['element'] = props.base.sunseasonElement[sunseason]
        else:
            if objID == const.MOON:
                phase = chart.getMoonPhase()
                res['phase'] = phase
                res['element'] = props.base.moonphaseElement[phase]
            else:
                if objID in const.LIST_SEVEN_PLANETS:
                    if aspect:
                        res['sign'] = obj.sign
                        res['element'] = props.sign.element[obj.sign]
                    else:
                        res['element'] = obj.element()
                else:
                    try:
                        res['element']
                        factors.append(res)
                    except KeyError:
                        pass

                return res


def modifierFactor(chart, factor, factorObj, otherObj, aspList):
    """ Computes a factor for a modifier. """
    asp = aspects.aspectType(factorObj, otherObj, aspList)
    if asp != const.NO_ASPECT:
        return {'factor':factor,  'aspect':asp, 
         'objID':otherObj.id, 
         'element':otherObj.element()}


def getFactors(chart):
    """ Returns the factors for the temperament. """
    factors = []
    asc = chart.getAngle(const.ASC)
    singleFactor(factors, chart, ASC_SIGN, asc.sign)
    ascRulerID = essential.ruler(asc.sign)
    ascRuler = chart.getObject(ascRulerID)
    singleFactor(factors, chart, ASC_RULER, ascRuler)
    singleFactor(factors, chart, ASC_RULER_SIGN, ascRuler.sign)
    house1 = chart.getHouse(const.HOUSE1)
    planetsHouse1 = chart.objects.getObjectsInHouse(house1)
    for obj in planetsHouse1:
        singleFactor(factors, chart, HOUSE1_PLANETS_IN, obj)

    planetsConjAsc = chart.objects.getObjectsAspecting(asc, [0])
    for obj in planetsConjAsc:
        if obj not in planetsHouse1:
            singleFactor(factors, chart, ASC_PLANETS_CONJ, obj)

    aspList = [60, 90, 120, 180]
    planetsAspAsc = chart.objects.getObjectsAspecting(asc, aspList)
    for obj in planetsAspAsc:
        aspect = aspects.aspectType(obj, asc, aspList)
        singleFactor(factors, chart, ASC_PLANETS_ASP, obj, aspect)

    moon = chart.getObject(const.MOON)
    singleFactor(factors, chart, MOON_SIGN, moon.sign)
    singleFactor(factors, chart, MOON_PHASE, moon)
    moonRulerID = essential.ruler(moon.sign)
    moonRuler = chart.getObject(moonRulerID)
    moonFactor = singleFactor(factors, chart, MOON_DISPOSITOR_SIGN, moonRuler.sign)
    moonFactor['planetID'] = moonRulerID
    planetsConjMoon = chart.objects.getObjectsAspecting(moon, [0])
    for obj in planetsConjMoon:
        singleFactor(factors, chart, MOON_PLANETS_CONJ, obj)

    aspList = [
     60, 90, 120, 180]
    planetsAspMoon = chart.objects.getObjectsAspecting(moon, aspList)
    for obj in planetsAspMoon:
        aspect = aspects.aspectType(obj, moon, aspList)
        singleFactor(factors, chart, MOON_PLANETS_ASP, obj, aspect)

    sun = chart.getObject(const.SUN)
    singleFactor(factors, chart, SUN_SEASON, sun)
    return factors


def getModifiers(chart):
    """ Returns the factors of the temperament modifiers. """
    modifiers = []
    asc = chart.getAngle(const.ASC)
    ascRulerID = essential.ruler(asc.sign)
    ascRuler = chart.getObject(ascRulerID)
    moon = chart.getObject(const.MOON)
    factors = [
     [
      MOD_ASC, asc],
     [
      MOD_ASC_RULER, ascRuler],
     [
      MOD_MOON, moon]]
    mars = chart.getObject(const.MARS)
    saturn = chart.getObject(const.SATURN)
    sun = chart.getObject(const.SUN)
    affect = [
     [
      mars, [0, 90, 180]],
     [
      saturn, [0, 90, 180]],
     [
      sun, [0]]]
    for affectingObj, affectingAsps in affect:
        for factor, affectedObj in factors:
            modf = modifierFactor(chart, factor, affectedObj, affectingObj, affectingAsps)
            if modf:
                modifiers.append(modf)

    return modifiers


def scores(factors):
    """ Computes the score of temperaments
    and elements.
    
    """
    temperaments = {const.CHOLERIC: 0, 
     const.MELANCHOLIC: 0, 
     const.SANGUINE: 0, 
     const.PHLEGMATIC: 0}
    qualities = {const.HOT: 0, 
     const.COLD: 0, 
     const.DRY: 0, 
     const.HUMID: 0}
    for factor in factors:
        element = factor['element']
        temperament = props.base.elementTemperament[element]
        temperaments[temperament] += 1
        tqualities = props.base.temperamentQuality[temperament]
        qualities[tqualities[0]] += 1
        qualities[tqualities[1]] += 1

    return {'temperaments':temperaments, 
     'qualities':qualities}


class Temperament:
    __doc__ = ' This class represents the calculation\n    of the temperament of a chart.\n    \n    '

    def __init__(self, chart):
        self.chart = chart

    def getFactors(self):
        """ Returns the list of temperament factors. """
        return getFactors(self.chart)

    def getModifiers(self):
        """ Returns the list of temperament modifiers. """
        return getModifiers(self.chart)

    def getScore(self):
        """ Returns the temperament and qualitiy scores. """
        return scores(self.getFactors())