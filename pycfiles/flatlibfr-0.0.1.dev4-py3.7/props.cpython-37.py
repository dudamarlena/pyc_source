# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/flatlibfr/props.py
# Compiled at: 2019-10-17 02:47:28
# Size of source mod 2**32: 9001 bytes
"""
    This file is part of flatlib - (C) FlatAngle
    Author: João Ventura (flatangleweb@gmail.com)
    flatlibfr translation of const by Stéphane Bressani (s.bressani@bluewin.ch)

    This module defines some properties of Traditional Astrology core
    elements.
    
    It defines qualities of temperaments, orbs and genders of planets,
    if a house is cardinal, angular or succedent, among others.
    
    To keep things simple, properties are divided in types, such as 
    base properties, planet properties, house properties, etc. Each 
    property type is defined as a lowercased python class so that we 
    can mimic different namespaces in a single python module.
    
"""
from . import const

class base:
    elements = [
     const.FIRE,
     const.EARTH,
     const.AIR,
     const.WATER]
    temperaments = [
     const.CHOLERIC,
     const.MELANCHOLIC,
     const.SANGUINE,
     const.PHLEGMATIC]
    genders = [
     const.MASCULINE,
     const.FEMININE]
    factions = [
     const.DIURNAL,
     const.NOCTURNAL]
    sunseasons = [
     const.SPRING,
     const.SUMMER,
     const.AUTUMN,
     const.WINTER]
    elementTemperament = {const.FIRE: const.CHOLERIC, 
     const.EARTH: const.MELANCHOLIC, 
     const.AIR: const.SANGUINE, 
     const.WATER: const.PHLEGMATIC}
    temperamentElement = {const.CHOLERIC: const.FIRE, 
     const.MELANCHOLIC: const.EARTH, 
     const.SANGUINE: const.AIR, 
     const.PHLEGMATIC: const.WATER}
    elementQuality = {const.FIRE: [const.HOT, const.DRY], 
     const.EARTH: [const.COLD, const.DRY], 
     const.AIR: [const.HOT, const.HUMID], 
     const.WATER: [const.COLD, const.HUMID]}
    temperamentQuality = {const.CHOLERIC: [const.HOT, const.DRY], 
     const.MELANCHOLIC: [const.COLD, const.DRY], 
     const.SANGUINE: [const.HOT, const.HUMID], 
     const.PHLEGMATIC: [const.COLD, const.HUMID]}
    moonphaseElement = {const.MOON_FIRST_QUARTER: const.AIR, 
     const.MOON_SECOND_QUARTER: const.FIRE, 
     const.MOON_THIRD_QUARTER: const.EARTH, 
     const.MOON_LAST_QUARTER: const.WATER}
    sunseasonElement = {const.SPRING: const.AIR, 
     const.SUMMER: const.FIRE, 
     const.AUTUMN: const.EARTH, 
     const.WINTER: const.WATER}


class sign:
    _signs = const.LIST_SIGNS
    _modes = [
     const.CARDINAL, const.FIXED, const.MUTABLE]
    mode = dict(zip(_signs, _modes * 4))
    _sunseasons = [[season] * 3 for season in base.sunseasons]
    _sunseasons = sum(_sunseasons, [])
    sunseason = dict(zip(_signs, _sunseasons))
    gender = dict(zip(_signs, base.genders * 6))
    faction = dict(zip(_signs, base.factions * 6))
    element = dict(zip(_signs, base.elements * 3))
    temperament = dict(zip(_signs, base.temperaments * 3))
    fertility = {const.ARIES: const.SIGN_MODERATELY_STERILE, 
     const.TAURUS: const.SIGN_MODERATELY_FERTILE, 
     const.GEMINI: const.SIGN_STERILE, 
     const.CANCER: const.SIGN_FERTILE, 
     const.LEO: const.SIGN_STERILE, 
     const.VIRGO: const.SIGN_STERILE, 
     const.LIBRA: const.SIGN_MODERATELY_FERTILE, 
     const.SCORPIO: const.SIGN_FERTILE, 
     const.SAGITTARIUS: const.SIGN_MODERATELY_FERTILE, 
     const.CAPRICORN: const.SIGN_MODERATELY_STERILE, 
     const.AQUARIUS: const.SIGN_MODERATELY_STERILE, 
     const.PISCES: const.SIGN_FERTILE}
    number = dict(((sign, i + 1) for i, sign in enumerate(_signs)))
    figureBestial = [
     const.ARIES,
     const.TAURUS,
     const.LEO,
     const.SAGITTARIUS,
     const.CAPRICORN]
    figureHuman = [
     const.GEMINI,
     const.VIRGO,
     const.LIBRA,
     const.AQUARIUS]
    figureWild = [
     const.LEO]


class object:
    meanMotion = {const.NO_PLANET: 0, 
     const.SUN: 0.9833, 
     const.MOON: 13.1833, 
     const.MERCURY: 0.9833, 
     const.VENUS: 0.9833, 
     const.MARS: 0.5166, 
     const.JUPITER: 0.0833, 
     const.SATURN: 0.0333, 
     const.URANUS: 0.001, 
     const.NEPTUNE: 0.0001, 
     const.PLUTO: 1e-05, 
     const.CHIRON: 1e-05, 
     const.NORTH_NODE: 13.1833, 
     const.SOUTH_NODE: 13.1833, 
     const.SYZYGY: 0.0}
    orb = {const.NO_PLANET: 0, 
     const.SUN: 15, 
     const.MOON: 12, 
     const.MERCURY: 7, 
     const.VENUS: 7, 
     const.MARS: 8, 
     const.JUPITER: 9, 
     const.SATURN: 9, 
     const.URANUS: 5, 
     const.NEPTUNE: 5, 
     const.PLUTO: 5, 
     const.CHIRON: 5, 
     const.NORTH_NODE: 12, 
     const.SOUTH_NODE: 12, 
     const.SYZYGY: 0, 
     const.PARS_FORTUNA: 0}
    element = {const.SATURN: const.EARTH, 
     const.JUPITER: const.AIR, 
     const.MARS: const.FIRE, 
     const.SUN: const.FIRE, 
     const.VENUS: const.AIR, 
     const.MERCURY: const.EARTH, 
     const.MOON: const.WATER}
    temperament = {const.SATURN: const.MELANCHOLIC, 
     const.JUPITER: const.SANGUINE, 
     const.MARS: const.CHOLERIC, 
     const.SUN: const.CHOLERIC, 
     const.VENUS: const.SANGUINE, 
     const.MERCURY: const.MELANCHOLIC, 
     const.MOON: const.PHLEGMATIC}
    gender = {const.SATURN: const.MASCULINE, 
     const.JUPITER: const.MASCULINE, 
     const.MARS: const.MASCULINE, 
     const.SUN: const.MASCULINE, 
     const.VENUS: const.FEMININE, 
     const.MERCURY: const.NEUTRAL, 
     const.MOON: const.FEMININE}
    faction = {const.SATURN: const.DIURNAL, 
     const.JUPITER: const.DIURNAL, 
     const.MARS: const.NOCTURNAL, 
     const.SUN: const.DIURNAL, 
     const.VENUS: const.NOCTURNAL, 
     const.MERCURY: const.NEUTRAL, 
     const.MOON: const.NOCTURNAL}
    signJoy = {const.SATURN: const.AQUARIUS, 
     const.JUPITER: const.SAGITTARIUS, 
     const.MARS: const.SCORPIO, 
     const.SUN: const.LEO, 
     const.VENUS: const.TAURUS, 
     const.MERCURY: const.VIRGO, 
     const.MOON: const.CANCER}
    houseJoy = {const.SATURN: const.HOUSE12, 
     const.JUPITER: const.HOUSE11, 
     const.MARS: const.HOUSE6, 
     const.SUN: const.HOUSE9, 
     const.VENUS: const.HOUSE5, 
     const.MERCURY: const.HOUSE1, 
     const.MOON: const.HOUSE3}


class house:
    _houses = const.LIST_HOUSES
    _conditions = [
     const.ANGULAR, const.SUCCEDENT, const.CADENT]
    condition = dict(zip(_houses, _conditions * 4))
    gender = dict(zip(_houses, base.genders * 4))
    aboveHorizon = [
     const.HOUSE7, const.HOUSE8, const.HOUSE9,
     const.HOUSE10, const.HOUSE11, const.HOUSE12]
    belowHorizon = [
     const.HOUSE1, const.HOUSE2, const.HOUSE3,
     const.HOUSE4, const.HOUSE5, const.HOUSE6]


class aspect:
    name = {const.NO_ASPECT: 'None', 
     const.CONJUNCTION: 'Conjunction', 
     const.SEXTILE: 'Sextile', 
     const.SQUARE: 'Square', 
     const.TRINE: 'Trine', 
     const.OPPOSITION: 'Opposition', 
     const.SEMISEXTILE: 'Semisextile', 
     const.SEMIQUINTILE: 'Semiquintile', 
     const.SEMISQUARE: 'Semisquare', 
     const.QUINTILE: 'Quintile', 
     const.SESQUIQUINTILE: 'Sesquiquintile', 
     const.SESQUISQUARE: 'Sesquisquare', 
     const.BIQUINTILE: 'Biquintile', 
     const.QUINCUNX: 'Quincunx'}


class fixedStar:
    pass


class houseSystem:
    pass