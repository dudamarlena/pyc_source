# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cloud_admin/cloudview/midokurabuilder.py
# Compiled at: 2018-01-31 14:44:08
__doc__ = '\nmidokura:\n    bgp-peers:\n    - local-as: 65169\n      peer-address: 10.116.133.173\n      port-ip: 10.116.129.41\n      remote-as: 65000\n      route: 10.116.45.0/24\n      router-name: eucart\n    cassandras:\n    - 10.111.1.41:9160\n    initial-tenant: euca_tenant_1\n    midolman-host-mapping:\n      c-06.qa1.eucalyptus-systems.com: 10.111.1.41\n      g-05-03.qa1.eucalyptus-systems.com: 10.111.1.175\n      b-40.qa1.eucalyptus-systems.com: 10.111.5.88\n      d-39.qa1.eucalyptus-systems.com: 10.111.5.101\n      g-08-09.qa1.eucalyptus-systems.com: 10.111.5.151\n    midonet-api-url: http://10.111.1.41:8080/midonet-api\n    repo-password: 8yU8Pj6h\n    repo-username: eucalyptus\n    yum-options: --nogpg\n    zookeepers:\n    - 10.111.1.41:2181\n'
from cloud_admin.cloudview import ConfigBlock

class MidokuraBuilder(ConfigBlock):
    pass


class BgpBuilder(ConfigBlock):
    pass


class Cassandras(ConfigBlock):
    pass


class ZooKeepers(ConfigBlock):
    pass