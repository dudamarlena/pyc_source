# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/flatlibfr/protocols/behavior.py
# Compiled at: 2019-10-17 02:47:28
# Size of source mod 2**32: 2144 bytes
"""
    This file is part of flatlib - (C) FlatAngle
    Author: João Ventura (flatangleweb@gmail.com)
    flatlibfr translation of const by Stéphane Bressani (s.bressani@bluewin.ch)

    This module implements the Behavior Traditional 
    Protocol.
    
"""
from flatlibfr import const
from flatlibfr import aspects
from flatlibfr.dignities import essential

def _merge(listA, listB):
    """ Merges two list of objects removing
    repetitions. 
    
    """
    listA = [x.id for x in listA]
    listB = [x.id for x in listB]
    listA.extend(listB)
    set_ = set(listA)
    return list(set_)


def compute(chart):
    """ Computes the behavior. """
    factors = []
    house1 = chart.getHouse(const.HOUSE1)
    planetsHouse1 = chart.objects.getObjectsInHouse(house1)
    asc = chart.getAngle(const.ASC)
    planetsConjAsc = chart.objects.getObjectsAspecting(asc, [0])
    _set = _merge(planetsHouse1, planetsConjAsc)
    factors.append(['Planets in House1 or Conj Asc', _set])
    moon = chart.get(const.MOON)
    mercury = chart.get(const.MERCURY)
    planetsConjMoon = chart.objects.getObjectsAspecting(moon, [0])
    planetsConjMercury = chart.objects.getObjectsAspecting(mercury, [0])
    _set = _merge(planetsConjMoon, planetsConjMercury)
    factors.append(['Planets Conj Moon or Mercury', _set])
    ascRulerID = essential.ruler(asc.sign)
    ascRuler = chart.getObject(ascRulerID)
    disposerID = essential.ruler(ascRuler.sign)
    disposer = chart.getObject(disposerID)
    _set = []
    if aspects.isAspecting(disposer, ascRuler, const.MAJOR_ASPECTS):
        _set = [
         ascRuler.id]
    factors.append(['Asc Ruler if aspected by its disposer', _set])
    aspMoon = chart.objects.getObjectsAspecting(moon, [60, 90, 120, 180])
    aspMercury = chart.objects.getObjectsAspecting(mercury, [60, 90, 120, 180])
    _set = _merge(aspMoon, aspMercury)
    factors.append(['Planets Asp Moon or Mercury', _set])
    return factors