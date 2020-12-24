# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/thirdparty_libs/geopy/units.py
# Compiled at: 2013-10-14 11:27:57
import math
from geopy import util

def degrees(radians=0, arcminutes=0, arcseconds=0):
    deg = 0.0
    if radians:
        deg = math.degrees(radians)
    if arcminutes:
        deg += arcminutes / arcmin(degrees=1.0)
    if arcseconds:
        deg += arcseconds / arcsec(degrees=1.0)
    return deg


def radians(degrees=0, arcminutes=0, arcseconds=0):
    if arcminutes:
        degrees += arcminutes / arcmin(degrees=1.0)
    if arcseconds:
        degrees += arcseconds / arcsec(degrees=1.0)
    return math.radians(degrees)


def arcminutes(degrees=0, radians=0, arcseconds=0):
    if radians:
        degrees += math.degrees(radians)
    if arcseconds:
        degrees += arcseconds / arcsec(degrees=1.0)
    return degrees * 60.0


def arcseconds(degrees=0, radians=0, arcminutes=0):
    if radians:
        degrees += math.degrees(radians)
    if arcminutes:
        degrees += arcminutes / arcmin(degrees=1.0)
    return degrees * 3600.0


rad = radians
arcmin = arcminutes
arcsec = arcseconds

def kilometers(meters=0, miles=0, feet=0, nautical=0):
    km = 0.0
    if meters:
        km += meters / 1000.0
    if feet:
        miles += feet / ft(1.0)
    if nautical:
        km += nautical / nm(1.0)
    km += miles * 1.609344
    return km


def meters(kilometers=0, miles=0, feet=0, nautical=0):
    meters = 0.0
    kilometers += km(nautical=nautical, miles=miles, feet=feet)
    meters += kilometers * 1000.0
    return meters


def miles(kilometers=0, meters=0, feet=0, nautical=0):
    mi = 0.0
    if nautical:
        kilometers += nautical / nm(1.0)
    if feet:
        mi += feet / ft(1.0)
    if meters:
        kilometers += meters / 1000.0
    mi += kilometers * 0.621371192
    return mi


def feet(kilometers=0, meters=0, miles=0, nautical=0):
    ft = 0.0
    if nautical:
        kilometers += nautical / nm(1.0)
    if meters:
        kilometers += meters / 1000.0
    if kilometers:
        miles += mi(kilometers=kilometers)
    ft += miles * 5280
    return ft


def nautical(kilometers=0, meters=0, miles=0, feet=0):
    nm = 0.0
    if feet:
        miles += feet / ft(1.0)
    if miles:
        kilometers += km(miles=miles)
    if meters:
        kilometers += meters / 1000.0
    nm += kilometers / 1.852
    return nm


km = kilometers
m = meters
mi = miles
ft = feet
nm = nautical