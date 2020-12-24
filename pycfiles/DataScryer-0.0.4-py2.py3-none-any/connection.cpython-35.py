# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Programmieren\dataScryer\datascryer\influxdb\connection.py
# Compiled at: 2016-06-14 11:45:34
# Size of source mod 2**32: 323 bytes


def gen_url(address, db, args, query_type):
    if not str.endswith(address, '/'):
        address += '/'
    return '%s%s?db=%s&%s' % (address, query_type, db, args)


def gen_clean_url(address, query_type):
    if not str.endswith(address, '/'):
        address += '/'
    return '%s%s' % (address, query_type)