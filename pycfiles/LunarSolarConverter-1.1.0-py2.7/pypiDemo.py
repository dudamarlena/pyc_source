# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/LunarSolarConverter/pypiDemo.py
# Compiled at: 2018-03-04 22:02:33
__author__ = 'isee15'
from pprint import pprint
from LunarSolarConverter import LunarSolarConverter
converter = LunarSolarConverter.LunarSolarConverter()
solar = LunarSolarConverter.Solar(2016, 4, 8)
pprint(vars(solar))
lunar = converter.SolarToLunar(solar)
pprint(vars(lunar))
solar = converter.LunarToSolar(lunar)
pprint(vars(solar))