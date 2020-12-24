# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kong/certificates.py
# Compiled at: 2019-08-12 17:48:16
# Size of source mod 2**32: 270 bytes
from .components import CrudComponent, KongEntity
from .snis import Snis

class Certificate(KongEntity):

    @property
    def snis(self):
        return Snis(self)


class Certificates(CrudComponent):
    __doc__ = 'Kong TLS certificate component'
    Entity = Certificate