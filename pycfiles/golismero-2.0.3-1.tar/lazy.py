# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/tools/theHarvester/discovery/DNS/lazy.py
# Compiled at: 2013-12-09 06:41:17
import Base, string

def revlookup(name):
    """convenience routine for doing a reverse lookup of an address"""
    if Base.defaults['server'] == []:
        Base.DiscoverNameServers()
    a = string.split(name, '.')
    a.reverse()
    b = string.join(a, '.') + '.in-addr.arpa'
    return Base.DnsRequest(b, qtype='ptr').req().answers[0]['data']


def mxlookup(name):
    """
    convenience routine for doing an MX lookup of a name. returns a
    sorted list of (preference, mail exchanger) records
    """
    if Base.defaults['server'] == []:
        Base.DiscoverNameServers()
    a = Base.DnsRequest(name, qtype='mx').req().answers
    l = map(lambda x: x['data'], a)
    l.sort()
    return l