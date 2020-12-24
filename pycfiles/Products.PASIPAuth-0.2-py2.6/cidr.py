# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Products/PASIPAuth/cidr.py
# Compiled at: 2009-12-02 03:10:07
import socket

def cidr(address):
    try:
        x = socket.inet_aton(address)
    except:
        raise ValueError('%s is not a valid ip address' % address)

    x = (ord(x[0]) << 24) + (ord(x[1]) << 16) + (ord(x[2]) << 8) + ord(x[3])
    return x


def in_cidr(address, net):
    """
    Takes two strings, the first an IP address, the second a network in
    CIDR format
    Returns True if the adress is in the network

    Example:
    >>> in_cidr('10.0.0.7', '10.0.0.0/29')
    True
    >>> in_cidr('10.0.0.8', '10.0.0.0/29')
    False
    >>> in_cidr('127.0.0.1', '127.0.0.1')
    True
    """
    mask = 4294967295
    components = net.split('/')
    if len(components) > 1:
        mask = ~(4294967295 >> int(components[1]))
    x = cidr(address)
    y = cidr(components[0])
    return x & mask == y