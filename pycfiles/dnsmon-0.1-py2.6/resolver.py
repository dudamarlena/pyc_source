# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dnsmon/resolver.py
# Compiled at: 2011-03-21 18:00:36
"""Wrapper to pyDNS to retrieve all DNS results for a given hostname"""
import DNS
DNS.ParseResolvConf()
resolver = DNS.DnsRequest(qtype='A')

def lookup(hostname):
    global resolver
    res = resolver.req(hostname)
    if len(res.answers) == 0:
        return []
    return [ x['data'] for x in res.answers if x['typename'] == 'A' ]