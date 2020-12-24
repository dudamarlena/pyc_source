# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc4985.py
# Compiled at: 2020-01-09 12:20:13
from pyasn1.type import char
from pyasn1.type import constraint
from pyasn1.type import univ
from pyasn1_modules import rfc5280
MAX = float('inf')
id_pkix = rfc5280.id_pkix
id_on = id_pkix + (8, )
id_on_dnsSRV = id_on + (7, )

class SRVName(char.IA5String):
    __module__ = __name__
    subtypeSpec = constraint.ValueSizeConstraint(1, MAX)


srvName = rfc5280.AnotherName()
srvName['type-id'] = id_on_dnsSRV
srvName['value'] = SRVName()
_anotherNameMapUpdate = {id_on_dnsSRV: SRVName()}
rfc5280.anotherNameMap.update(_anotherNameMapUpdate)