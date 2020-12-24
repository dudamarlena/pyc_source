# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dexstore/blockchainobject.py
# Compiled at: 2019-03-19 09:04:59
# Size of source mod 2**32: 396 bytes
from .instance import BlockchainInstance
from graphenecommon.blockchainobject import BlockchainObject as GrapheneBlockchainObject, Object as GrapheneChainObject, ObjectCache

@BlockchainInstance.inject
class BlockchainObject(GrapheneBlockchainObject):
    pass


@BlockchainInstance.inject
class Object(GrapheneChainObject):
    perform_id_tests = False