# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
    """Certificates"""
    Entity = Certificate