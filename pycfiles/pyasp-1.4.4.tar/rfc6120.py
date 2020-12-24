# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc6120.py
# Compiled at: 2020-01-09 12:20:13
from pyasn1.type import char
from pyasn1.type import univ
from pyasn1_modules import rfc5280
MAX = float('inf')
id_pkix = rfc5280.id_pkix
id_on = id_pkix + (8, )
id_on_xmppAddr = id_on + (5, )

class XmppAddr(char.UTF8String):
    __module__ = __name__


_anotherNameMapUpdate = {id_on_xmppAddr: XmppAddr()}
rfc5280.anotherNameMap.update(_anotherNameMapUpdate)