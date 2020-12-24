# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp/carrier/sockfix.py
# Compiled at: 2019-08-18 17:24:05
import socket
from pysnmp import debug
SYMBOLS = {'IP_PKTINFO': 8, 'IP_TRANSPARENT': 19, 'SOL_IPV6': 41, 'IPV6_RECVPKTINFO': 49, 'IPV6_PKTINFO': 50, 'IPV6_TRANSPARENT': 75}
for (symbol, value) in SYMBOLS.items():
    if not hasattr(socket, symbol):
        setattr(socket, symbol, value)
        debug.logger & debug.flagIO and debug.logger('WARNING: the socket module on this platform misses option %s. Assuming its value is %d.' % (symbol, value))