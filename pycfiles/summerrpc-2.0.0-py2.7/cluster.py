# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summerrpc/cluster.py
# Compiled at: 2018-07-31 10:42:31
__all__ = [
 'Cluster', 'AbstractCluster', 'RandomCluster']
__authors__ = ['Tim Chow']
from abc import ABCMeta, abstractmethod
import random

class Cluster(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_remote(self, class_name, method_name, transport, serializer):
        pass

    @abstractmethod
    def choice_remote(self, remotes):
        pass


class AbstractCluster(Cluster):

    def __init__(self, registry):
        self._registry = registry

    def get_remote(self, class_name, method_name, transport, serializer):
        remotes = self._registry.get_remotes(class_name, method_name, transport, serializer)
        if len(remotes) == 0:
            return None
        else:
            remote = self.choice_remote(remotes)
            return remote

    def close(self):
        self._registry.close()


class RandomCluster(AbstractCluster):

    def choice_remote(self, remotes):
        return random.choice(remotes)