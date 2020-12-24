# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/benoit/Dev/vigilance-meteo/src/vigilancemeteo/__init__.py
# Compiled at: 2019-04-04 17:22:17
# Size of source mod 2**32: 379 bytes
"""Vigilancemeteo provide an API to fetch France weather alerts from Météo
France website.

ZoneAlerte class allows to fetch active weather alerts for a french department.
"""
from .vigilance_proxy import VigilanceMeteoFranceProxy, VigilanceMeteoError
from .department_weather_alert import DepartmentWeatherAlert
from .__version__ import __version__, VERSION