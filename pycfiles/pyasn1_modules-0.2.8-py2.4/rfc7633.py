# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc7633.py
# Compiled at: 2019-10-17 01:03:15
from pyasn1.type import univ
from pyasn1_modules import rfc5280
id_pe = univ.ObjectIdentifier('1.3.6.1.5.5.7.1')
id_pe_tlsfeature = id_pe + (24, )

class Features(univ.SequenceOf):
    __module__ = __name__
    componentType = univ.Integer()


_certificateExtensionsMapUpdate = {id_pe_tlsfeature: Features()}
rfc5280.certificateExtensionsMap.update(_certificateExtensionsMapUpdate)