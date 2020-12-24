# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/libsnmp/rfc1902.py
# Compiled at: 2008-10-18 18:59:45
import util, debug, logging, types
from rfc1155 import *
log = logging.getLogger('rfc1902')
log.setLevel(logging.INFO)
asnTagNumbers['Counter64'] = 6

class Integer32(Integer):
    """ A 32 bit integer
    """
    MINVAL = -2147483648
    MAXVAL = 2147483648


class Counter32(Counter):
    """ A 32 bit counter
    """
    pass


class Guage32(Guage):
    """ A 32 bit Guage
    """
    pass


class Counter64(Counter):
    """ A 64 bit counter
    """
    MINVAL = 0
    MAXVAL = 18446744073709551615
    asnTagClass = asnTagNumbers['Counter64']


class OctetString(OctetString):
    """ An SNMP v2 OctetString must be between
        0 and 65535 bytes in length
    """

    def __init__(self, value=''):
        if len(value) > 65535:
            raise ValueError('OctetString must be shorter than 65535 bytes')
        OctetString.__init__(self, value)


tagDecodeDict[2] = Integer32
tagDecodeDict[65] = Counter32
tagDecodeDict[66] = Guage32
tagDecodeDict[70] = Counter64