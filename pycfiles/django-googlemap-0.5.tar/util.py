# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gmy/project/xperiment/xperiment/googlemap/ip2geo/util.py
# Compiled at: 2013-11-19 22:47:08


def ip2long(ip):
    """
    Convert a IPv4 address into a 32-bit integer.

    @param ip: quad-dotted IPv4 address
    @type ip: str
    @return: network byte order 32-bit integer
    @rtype: int
    """
    ip_array = ip.split('.')
    ip_long = long(ip_array[0]) * 16777216 + long(ip_array[1]) * 65536 + long(ip_array[2]) * 256 + long(ip_array[3])
    return ip_long