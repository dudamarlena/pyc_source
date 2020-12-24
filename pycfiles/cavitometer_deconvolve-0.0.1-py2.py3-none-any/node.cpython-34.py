# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/caviar/domain/node.py
# Compiled at: 2017-10-25 18:02:55
# Size of source mod 2**32: 3224 bytes
__doc__ = '\nNode module.\n'
import caviar, caviar.domain, caviar.domain.instance

class Node:
    """Node"""

    def __init__(self, context, name, host):
        self._Node__context = context
        self._Node__name = name
        self._Node__host = host

    def __hash__(self):
        return hash(self._Node__name)

    def __eq__(self, other):
        return self._Node__name == other._Node__name

    def __str__(self):
        return self._Node__name

    def __management(self):
        return self._Node__context.management()

    def __load_balancer(self, name):
        return self._Node__context.load_balancer(cluster)

    @property
    def name(self):
        """
                Node name.
                
                :rtype:
                   str
                """
        return self._Node__name

    @property
    def host(self):
        """
                Node host.
                
                :rtype:
                   str
                """
        return self._Node__host

    def instances(self):
        """
                Node instances.

                :rtype:
                   iter
                :return:
                   Iterator that yields node instances.
                """
        res = self._Node__management().domain()
        res = res.extra_properties.child_resources['servers']
        res = res.extra_properties.child_resources['server']
        for name, inst_res in res.extra_properties.child_resources.items():
            if inst_res.extra_properties.entity.nodeRef == self._Node__name:
                yield caviar.domain.instance.restore(self._Node__context, name, self, inst_res)
                continue

    def create_instance(self, name, cluster):
        """
                Create a new noide instance for participating in the given cluster.
                
                :param str name:
                   Instance name.
                :param caviar.domain.cluster.Cluster cluster:
                   Cluster where participate in.
                   
                :rtype:
                   caviar.domain.instance.Instance
                :return:
                   The created instance.
                """
        res = self._Node__management().domain()
        res.extra_properties.commands.create_instance(id=name, nodeagent=self._Node__name, cluster=cluster.name)
        res = self._Node__management().domain()
        res = res.extra_properties.child_resources['servers']
        res = res.extra_properties.child_resources['server']
        res.extra_properties.child_resources.cache_evict()
        created_instance = next(filter(lambda inst: inst.name == name, self.instances()), None)
        return created_instance


def restore(context, name, resource):
    return Node(context, name, resource.extra_properties.entity.nodeHost)