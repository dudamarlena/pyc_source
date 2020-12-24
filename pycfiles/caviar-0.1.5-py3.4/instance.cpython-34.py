# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/caviar/domain/instance.py
# Compiled at: 2017-10-25 18:02:55
# Size of source mod 2**32: 2297 bytes
"""
Instance module.
"""

class Instance:
    __doc__ = '\n\tInstance.\n\n\t:param caviar.domain.ManagedDomainContext context:\n\t   Managed domain context.\n\t:param str name:\n\t   Instance name.\n\t:param caviar.domain.cluster.Cluster cluster:\n\t   Cluster where instance participates.\n\t:param caviar.domain.node.Node node:\n\t   Node where instance resides.\n\t:param str ajp_port:\n\t   AJP 1.3 port.\n\t'

    def __init__(self, context, name, node, ajp_port):
        self._Instance__context = context
        self._Instance__name = name
        self._Instance__node = node
        self._Instance__ajp_port = ajp_port

    def __eq__(self, other):
        return self._Instance__name == other._Instance__name

    @property
    def name(self):
        """
                Instance name.
                
                :rtype:
                   str
                """
        return self._Instance__name

    @property
    def host(self):
        """
                Instance host.
                
                :rtype:
                   str
                """
        return self._Instance__node.host

    @property
    def ajp_port(self):
        """
                AJP 1.3 port.
                
                :rtype:
                   str
                """
        return self._Instance__ajp_port


def restore(context, name, node, resource):
    config_ref = resource.extra_properties.entity.configRef
    res = context.management().domain()
    res = res.extra_properties.child_resources['configs']
    res = res.extra_properties.child_resources['config']
    res = res.extra_properties.child_resources[config_ref]
    res = res.raise_not_success()
    res = res.extra_properties.child_resources['network-config']
    res = res.extra_properties.child_resources['network-listeners']
    res = res.extra_properties.child_resources['network-listener']
    res = res.extra_properties.child_resources['http-listener-1']
    res = res.raise_not_success()
    return Instance(context, name, node, res.extra_properties.entity.port)