# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/reg/src/tools/ethiopian_date/ethiopian_date/__init__.py
# Compiled at: 2010-12-28 07:21:09
""" Ethiopian Date Converter

Convert from Ethiopian date to Gregorian date (and vice-versa)

Examples:

greg_date = EthiopianDateConverter.to_gregorian(2003, 4, 11)
ethi_date = EthiopianDateConverter.date_to_ethiopian(datetime.date.today())

"""
VERSION = (0, 1, 1)

def get_version():
    version = '%s.%s' % (VERSION[0], VERSION[1])
    if VERSION[2] != 0:
        version = '%s.%s' % (version, VERSION[2])
    return version


__version__ = get_version()
from ethiopian_date import EthiopianDateConverter