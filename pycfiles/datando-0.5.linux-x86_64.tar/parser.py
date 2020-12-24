# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/datando/parser.py
# Compiled at: 2013-03-13 10:31:36
import datando.gregorian, datando.julian, datando.kernel, datando.jd, datando.mjd, datando.rjd, datando.tjd, datando.djd, datando.jd
registered_classes = [
 datando.gregorian.GregorianDateTime,
 datando.julian.JulianDateTime,
 datando.jd.JDDateTime,
 datando.mjd.MJDDateTime,
 datando.rjd.RJDDateTime,
 datando.tjd.TJDDateTime,
 datando.djd.DJDDateTime,
 datando.kernel.LPInterval]

def parse(date_str):
    for c in registered_classes:
        if date_str.startswith(c.get_prefix()):
            return c.parse(date_str)

    return datando.kernel.LPDateTime.parse(date_str)