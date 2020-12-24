# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/unitsystem/metricsystem.py
# Compiled at: 2019-08-19 02:52:33
# Size of source mod 2**32: 1931 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '01/09/2016'
meter = 1.0
m = meter
centimeter = meter / 100.0
cm = centimeter
millimeter = 0.1 * centimeter
mm = millimeter
micrometer = 1e-06 * meter
nanometer = 1e-09 * meter
nm = nanometer
mm2 = millimeter * millimeter
cm2 = centimeter * centimeter
m2 = meter * meter

def getUnitName(value):
    """Return the name in (None, nm, cm, m, mm) from the given unit"""
    if value == nanometer:
        return 'nm'
    if value == millimeter:
        return 'mm'
    if value == centimeter:
        return 'cm'
    if value == meter:
        return 'm'