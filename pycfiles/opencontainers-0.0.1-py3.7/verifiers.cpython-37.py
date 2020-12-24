# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/opencontainers/digest/verifiers.py
# Compiled at: 2019-11-04 17:26:27
# Size of source mod 2**32: 1312 bytes
from opencontainers.struct import Struct
from hashlib import new
from .digest import Digest

class hashVerifier(Struct):

    def __init__(self, hashObj=None, digest=None):
        super().__init__()
        self.newAttr(name='hash', attType=new)
        self.newAttr(name='digest', attType=Digest)
        self.add('digest', digest)
        self.add('hash', hashObj)