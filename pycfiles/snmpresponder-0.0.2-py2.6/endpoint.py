# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snmpresponder/endpoint.py
# Compiled at: 2019-01-13 12:56:28
import re
from snmpresponder.error import SnmpResponderError
from pysnmp.carrier.asyncore.dgram import udp
try:
    from pysnmp.carrier.asyncore.dgram import udp6
except ImportError:
    udp6 = None

def parseTransportAddress(transportDomain, transportAddress, transportOptions, defaultPort=0):
    if ('transparent-proxy' in transportOptions or 'virtual-interface' in transportOptions) and '$' in transportAddress:
        addrMacro = transportAddress
        if transportDomain[:len(udp.domainName)] == udp.domainName:
            h, p = '0.0.0.0', defaultPort
        else:
            h, p = '::0', defaultPort
    else:
        addrMacro = None
        if transportDomain[:len(udp.domainName)] == udp.domainName:
            if ':' in transportAddress:
                (h, p) = transportAddress.split(':', 1)
            else:
                h, p = transportAddress, defaultPort
        else:
            hp = re.split('^\\[(.*?)\\]:([0-9]+)', transportAddress, maxsplit=1)
            if len(hp) != 4:
                raise SnmpResponderError('bad address specification')
            (h, p) = hp[1:3]
        try:
            p = int(p)
        except (ValueError, IndexError):
            raise SnmpResponderError('bad port specification')

        return ((h, p), addrMacro)