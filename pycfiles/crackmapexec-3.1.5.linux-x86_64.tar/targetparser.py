# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/byt3bl33d3r/.virtualenvs/CME_old/lib/python2.7/site-packages/cme/targetparser.py
# Compiled at: 2016-12-29 01:49:52
from netaddr import IPAddress, IPRange, IPNetwork, AddrFormatError

def parse_targets(target):
    if '-' in target:
        ip_range = target.split('-')
        try:
            hosts = IPRange(ip_range[0], ip_range[1])
        except AddrFormatError:
            try:
                start_ip = IPAddress(ip_range[0])
                start_ip_words = list(start_ip.words)
                start_ip_words[-1] = ip_range[1]
                start_ip_words = [ str(v) for v in start_ip_words ]
                end_ip = IPAddress(('.').join(start_ip_words))
                t = IPRange(start_ip, end_ip)
            except AddrFormatError:
                t = target

    else:
        try:
            t = IPNetwork(target)
        except AddrFormatError:
            t = target

    if type(t) == IPNetwork or type(t) == IPRange:
        return list(t)
    else:
        return [
         t.strip()]