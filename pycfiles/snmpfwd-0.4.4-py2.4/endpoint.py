# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snmpfwd/trunking/endpoint.py
# Compiled at: 2018-12-30 12:01:29
import re, socket
from snmpfwd.error import SnmpfwdError
IP_TEMPLATES = [
 (
  socket.AF_INET, '^([0-9]+\\.[0-9]+\\.[0-9]+\\.[0-9]+):([0-9]+)$|^([0-9]+\\.[0-9]+\\.[0-9]+\\.[0-9]+)$')]
if socket.has_ipv6:
    IP_TEMPLATES.append((socket.AF_INET6, '^\\[([0-9:]+?)\\]:([0-9]+)$|^\\[([0-9:]+?)\\]$'))

def parseTrunkEndpoint(address, defaultPort=0):
    for (af, pattern) in IP_TEMPLATES:
        hp = re.split(pattern, address, maxsplit=1)
        if len(hp) == 5:
            if hp[1]:
                (h, p) = hp[1:3]
            elif hp[3]:
                h, p = hp[3], defaultPort
            else:
                continue
            try:
                p = int(p)
            except (ValueError, IndexError):
                raise SnmpfwdError('bad port specification: %s' % (address,))
            else:
                return (
                 af, h, p)

    raise SnmpfwdError('bad address specification: %s' % (address,))