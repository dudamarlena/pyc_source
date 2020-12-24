# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/astro_py/astro_py.py
# Compiled at: 2019-10-17 02:54:23
# Size of source mod 2**32: 3290 bytes
"""
    Author: Stéphane Bressani <s.bressani@bluewin.ch> -> Astro py
            João Ventura <flatangleweb@gmail.com> -> Flat lib 
              -> https://buildmedia.readthedocs.org/media/pdf/flatlib/latest/flatlib.pdf
            Brandon Craig Rhodes 
              -> https://rhodesmill.org/pyephem/
            Dieter Koch and Dr. Alois Treindl 
              -> https://www.astro.com/swisseph/swephinfo_e.htm
    
    GNU public licence version 2 or later
"""
import sys
from datetime import datetime as dt, timedelta
from flatlibfr import aspects
from flatlibfr import const
from flatlibfr.chart import Chart
from flatlibfr.datetime import Datetime
from flatlibfr.geopos import GeoPos
from flatlibfr.protocols import behavior
import astro_py.export as export
import astro_py.component.my_timedelta as my_timedelta

class astro_py:

    def __init__(self, date, hour_min, utc, geo_pos_1, geo_pos_2):
        date = Datetime(date, hour_min, utc)
        pos = GeoPos(geo_pos_1, geo_pos_2)
        chart = Chart(date, pos, hsys=(const.HOUSES_PLACIDUS), IDs=(const.LIST_OBJECTS))
        angles = []
        angles.append(chart.get(const.ASC))
        angles.append(chart.get(const.IC))
        angles.append(chart.get(const.DESC))
        angles.append(chart.get(const.MC))
        houses = []
        houses.append(chart.get(const.HOUSE1))
        houses.append(chart.get(const.HOUSE2))
        houses.append(chart.get(const.HOUSE3))
        houses.append(chart.get(const.HOUSE4))
        houses.append(chart.get(const.HOUSE5))
        houses.append(chart.get(const.HOUSE6))
        houses.append(chart.get(const.HOUSE7))
        houses.append(chart.get(const.HOUSE8))
        houses.append(chart.get(const.HOUSE9))
        houses.append(chart.get(const.HOUSE10))
        houses.append(chart.get(const.HOUSE11))
        houses.append(chart.get(const.HOUSE12))
        planets = []
        planets.append(chart.get(const.SUN))
        planets.append(chart.get(const.MOON))
        planets.append(chart.get(const.MERCURY))
        planets.append(chart.get(const.VENUS))
        planets.append(chart.get(const.MARS))
        planets.append(chart.get(const.JUPITER))
        planets.append(chart.get(const.SATURN))
        planets.append(chart.get(const.URANUS))
        planets.append(chart.get(const.NEPTUNE))
        planets.append(chart.get(const.PLUTO))
        planets.append(chart.get(const.CHIRON))
        planets.append(chart.get(const.NORTH_NODE))
        planets.append(chart.get(const.SOUTH_NODE))
        planets.append(chart.get(const.PARS_FORTUNA))
        self.data = export(angles=angles, houses=houses, planets=planets)

    def get_data(self):
        """ Export json of all datas """
        return self.data.to_json()

    def helloworld(self, n, p):
        print('Hello world ' + n + ' ' + p)