# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/flatlibfr/predictives/returns.py
# Compiled at: 2019-10-17 02:47:28
# Size of source mod 2**32: 1199 bytes
"""
    This file is part of flatlib - (C) FlatAngle
    Author: João Ventura (flatangleweb@gmail.com)
    flatlibfr translation of const by Stéphane Bressani (s.bressani@bluewin.ch)

    This module provides useful functions for 
    handling solar and lunar returns.
    It only handles solar returns for now.
    
"""
from flatlibfr import const
import flatlibfr.ephem as ephem
from flatlibfr.chart import Chart

def _computeChart(chart, date):
    """ Internal function to return a new chart for
    a specific date using properties from old chart.
    
    """
    pos = chart.pos
    hsys = chart.hsys
    IDs = [obj.id for obj in chart.objects]
    return Chart(date, pos, IDs=IDs, hsys=hsys)


def nextSolarReturn(chart, date):
    """ Returns the solar return of a Chart
    after a specific date.
    
    """
    sun = chart.getObject(const.SUN)
    srDate = ephem.nextSolarReturn(date, sun.lon)
    return _computeChart(chart, srDate)


def prevSolarReturn(chart, date):
    """ Returns the solar return of a Chart
    before a specific date.
    
    """
    sun = chart.getObject(const.SUN)
    srDate = ephem.prevSolarReturn(date, sun.lon)
    return _computeChart(chart, srDate)