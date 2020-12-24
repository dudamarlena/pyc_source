# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/lib/iprir/api.py
# Compiled at: 2017-03-21 22:17:22
# Size of source mod 2**32: 353 bytes
import iprir.database, iprir.ipset
__all__ = ('get_db', 'by_ip', 'by_country')
_ipdb = None

def get_db():
    global _ipdb
    if _ipdb is None:
        _ipdb = iprir.database.DB()
    return _ipdb


def by_ip(ipobj):
    return get_db().by_ip(ipobj)


def by_country(type_, country):
    return iprir.ipset.IpSet.by_country(type_, country)