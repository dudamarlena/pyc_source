# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/flatlibfr/tools/arabicparts.py
# Compiled at: 2019-10-17 02:47:28
# Size of source mod 2**32: 4693 bytes
"""
    This file is part of flatlib - (C) FlatAngle
    Author: João Ventura (flatangleweb@gmail.com)
    
    
    This module provides useful functions for computing 
    Arabic Parts.
  
"""
from flatlibfr import const
from flatlibfr.object import GenericObject
from flatlibfr.dignities import essential
PARS_FORTUNA = const.PARS_FORTUNA
PARS_SPIRIT = 'Pars Spirit'
PARS_FAITH = 'Pars Faith'
PARS_SUBSTANCE = 'Pars Substance'
PARS_WEDDING_MALE = 'Pars Wedding [Male]'
PARS_WEDDING_FEMALE = 'Pars Wedding [Female]'
PARS_SONS = 'Pars Sons'
PARS_FATHER = 'Pars Father'
PARS_MOTHER = 'Pars Mother'
PARS_BROTHERS = 'Pars Brothers'
PARS_DISEASES = 'Pars Diseases'
PARS_DEATH = 'Pars Death'
PARS_TRAVEL = 'Pars Travel'
PARS_FRIENDS = 'Pars Friends'
PARS_ENEMIES = 'Pars Enemies'
PARS_SATURN = 'Pars Saturn'
PARS_JUPITER = 'Pars Jupiter'
PARS_MARS = 'Pars Mars'
PARS_VENUS = 'Pars Venus'
PARS_MERCURY = 'Pars Mercury'
PARS_HORSEMANSHIP = 'Pars Horsemanship'
FORMULAS = {}
FORMULAS[PARS_FORTUNA] = [
 [
  const.SUN, const.MOON, const.ASC],
 [
  const.MOON, const.SUN, const.ASC]]
FORMULAS[PARS_SPIRIT] = [
 [
  const.MOON, const.SUN, const.ASC],
 [
  const.SUN, const.MOON, const.ASC]]
FORMULAS[PARS_FAITH] = [
 [
  const.MOON, const.MERCURY, const.ASC],
 [
  const.MERCURY, const.MOON, const.ASC]]
FORMULAS[PARS_SUBSTANCE] = [
 [
  '$R' + const.HOUSE2, const.HOUSE2, const.ASC],
 [
  '$R' + const.HOUSE2, const.HOUSE2, const.ASC]]
FORMULAS[PARS_WEDDING_MALE] = [
 [
  const.SATURN, const.VENUS, const.ASC],
 [
  const.SATURN, const.VENUS, const.ASC]]
FORMULAS[PARS_WEDDING_FEMALE] = [
 [
  const.VENUS, const.SATURN, const.ASC],
 [
  const.VENUS, const.SATURN, const.ASC]]
FORMULAS[PARS_SONS] = [
 [
  const.JUPITER, const.SATURN, const.ASC],
 [
  const.SATURN, const.JUPITER, const.ASC]]
FORMULAS[PARS_FATHER] = [
 [
  const.SUN, const.SATURN, const.ASC],
 [
  const.SATURN, const.SUN, const.ASC]]
FORMULAS[PARS_MOTHER] = [
 [
  const.VENUS, const.MOON, const.ASC],
 [
  const.MOON, const.VENUS, const.ASC]]
FORMULAS[PARS_BROTHERS] = [
 [
  const.SATURN, const.JUPITER, const.ASC],
 [
  const.SATURN, const.JUPITER, const.ASC]]
FORMULAS[PARS_DISEASES] = [
 [
  const.SATURN, const.MARS, const.ASC],
 [
  const.MARS, const.SATURN, const.ASC]]
FORMULAS[PARS_DEATH] = [
 [
  const.MOON, const.HOUSE8, const.SATURN],
 [
  const.MOON, const.HOUSE8, const.SATURN]]
FORMULAS[PARS_TRAVEL] = [
 [
  '$R' + const.HOUSE9, const.HOUSE9, const.ASC],
 [
  '$R' + const.HOUSE9, const.HOUSE9, const.ASC]]
FORMULAS[PARS_FRIENDS] = [
 [
  const.MOON, const.MERCURY, const.ASC],
 [
  const.MOON, const.MERCURY, const.ASC]]
FORMULAS[PARS_ENEMIES] = [
 [
  '$R' + const.HOUSE12, const.HOUSE12, const.ASC],
 [
  '$R' + const.HOUSE12, const.HOUSE12, const.ASC]]
FORMULAS[PARS_SATURN] = [
 [
  const.SATURN, const.PARS_FORTUNA, const.ASC],
 [
  const.PARS_FORTUNA, const.SATURN, const.ASC]]
FORMULAS[PARS_JUPITER] = [
 [
  PARS_SPIRIT, const.JUPITER, const.ASC],
 [
  const.JUPITER, PARS_SPIRIT, const.ASC]]
FORMULAS[PARS_MARS] = [
 [
  const.MARS, const.PARS_FORTUNA, const.ASC],
 [
  const.PARS_FORTUNA, const.MARS, const.ASC]]
FORMULAS[PARS_VENUS] = [
 [
  PARS_SPIRIT, const.VENUS, const.ASC],
 [
  const.VENUS, PARS_SPIRIT, const.ASC]]
FORMULAS[PARS_MERCURY] = [
 [
  const.MERCURY, const.PARS_FORTUNA, const.ASC],
 [
  const.PARS_FORTUNA, const.MERCURY, const.ASC]]
FORMULAS[PARS_HORSEMANSHIP] = [
 [
  const.SATURN, const.MOON, const.ASC],
 [
  const.MOON, const.SATURN, const.ASC]]

def objLon(ID, chart):
    """ Returns the longitude of an object. """
    if ID.startswith('$R'):
        ID = ID[2:]
        obj = chart.get(ID)
        rulerID = essential.ruler(obj.sign)
        ruler = chart.getObject(rulerID)
        return ruler.lon
    if ID.startswith('Pars'):
        return partLon(ID, chart)
    obj = chart.get(ID)
    return obj.lon


def partLon(ID, chart):
    """ Returns the longitude of an arabic part. """
    abc = FORMULAS[ID][0] if chart.isDiurnal() else FORMULAS[ID][1]
    a = objLon(abc[0], chart)
    b = objLon(abc[1], chart)
    c = objLon(abc[2], chart)
    return c + b - a


def getPart(ID, chart):
    """ Returns an Arabic Part. """
    obj = GenericObject()
    obj.id = ID
    obj.type = const.OBJ_ARABIC_PART
    obj.relocate(partLon(ID, chart))
    return obj