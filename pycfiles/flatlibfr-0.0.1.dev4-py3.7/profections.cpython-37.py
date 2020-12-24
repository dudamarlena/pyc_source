# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/flatlibfr/predictives/profections.py
# Compiled at: 2019-10-17 02:47:28
# Size of source mod 2**32: 1304 bytes
"""
    This file is part of flatlib - (C) FlatAngle
    Author: João Ventura (flatangleweb@gmail.com)
    flatlibfr translation of const by Stéphane Bressani (s.bressani@bluewin.ch)

    This module provides useful functions for 
    handling profections.
    
"""
import math
from flatlibfr import const
import flatlibfr.ephem as ephem

def compute(chart, date, fixedObjects=False):
    """ Returns a profection chart for a given
    date. Receives argument 'fixedObjects' to
    fix chart objects in their natal locations.
    
    """
    sun = chart.getObject(const.SUN)
    prevSr = ephem.prevSolarReturn(date, sun.lon)
    nextSr = ephem.nextSolarReturn(date, sun.lon)
    rotation = 30 * (date.jd - prevSr.jd) / (nextSr.jd - prevSr.jd)
    age = math.floor((date.jd - chart.date.jd) / 365.25)
    rotation = 30 * age + rotation
    pChart = chart.copy()
    for obj in pChart.objects:
        if not fixedObjects:
            obj.relocate(obj.lon + rotation)

    for house in pChart.houses:
        house.relocate(house.lon + rotation)

    for angle in pChart.angles:
        angle.relocate(angle.lon + rotation)

    return pChart