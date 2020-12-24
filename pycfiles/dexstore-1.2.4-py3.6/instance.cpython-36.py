# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dexstore/instance.py
# Compiled at: 2019-03-20 04:30:25
# Size of source mod 2**32: 1277 bytes
from graphenecommon.instance import AbstractBlockchainInstanceProvider, SharedInstance

class BlockchainInstance(AbstractBlockchainInstanceProvider):
    __doc__ = ' This is a class that allows compatibility with previous\n        naming conventions\n    '

    def __init__(self, *args, **kwargs):
        if kwargs.get('dexstore_instance'):
            kwargs['blockchain_instance'] = kwargs['dexstore_instance']
        (AbstractBlockchainInstanceProvider.__init__)(self, *args, **kwargs)

    def get_instance_class(self):
        """ Should return the Chain instance class, e.g. `dexstore.DexStore`
        """
        import dexstore as dst
        return dst.DexStore

    @property
    def dexstore(self):
        """ Alias for the specific blockchain
        """
        return self.blockchain


def shared_blockchain_instance():
    return BlockchainInstance().shared_blockchain_instance()


def set_shared_blockchain_instance(instance):
    instance.clear_cache()
    instance.set_shared_instance()


def set_shared_config(config):
    shared_blockchain_instance().set_shared_config(config)


shared_dexstore_instance = shared_blockchain_instance
set_shared_dexstore_instance = set_shared_blockchain_instance