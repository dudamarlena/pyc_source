# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc6210.py
# Compiled at: 2019-10-17 01:00:24
from pyasn1.type import constraint
from pyasn1.type import univ
from pyasn1_modules import rfc5280
id_alg_MD5_XOR_EXPERIMENT = univ.ObjectIdentifier('1.2.840.113549.1.9.16.3.13')

class MD5_XOR_EXPERIMENT(univ.OctetString):
    __module__ = __name__


MD5_XOR_EXPERIMENT.subtypeSpec = constraint.ValueSizeConstraint(64, 64)
mda_xor_md5_EXPERIMENT = rfc5280.AlgorithmIdentifier()
mda_xor_md5_EXPERIMENT['algorithm'] = id_alg_MD5_XOR_EXPERIMENT
mda_xor_md5_EXPERIMENT['parameters'] = MD5_XOR_EXPERIMENT()
_algorithmIdentifierMapUpdate = {id_alg_MD5_XOR_EXPERIMENT: MD5_XOR_EXPERIMENT()}
rfc5280.algorithmIdentifierMap.update(_algorithmIdentifierMapUpdate)