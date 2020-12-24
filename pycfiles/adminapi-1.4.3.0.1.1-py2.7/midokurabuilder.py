# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cloud_admin/cloudview/midokurabuilder.py
# Compiled at: 2018-01-31 14:44:08
"""
midokura:
    bgp-peers:
    - local-as: 65169
      peer-address: 10.116.133.173
      port-ip: 10.116.129.41
      remote-as: 65000
      route: 10.116.45.0/24
      router-name: eucart
    cassandras:
    - 10.111.1.41:9160
    initial-tenant: euca_tenant_1
    midolman-host-mapping:
      c-06.qa1.eucalyptus-systems.com: 10.111.1.41
      g-05-03.qa1.eucalyptus-systems.com: 10.111.1.175
      b-40.qa1.eucalyptus-systems.com: 10.111.5.88
      d-39.qa1.eucalyptus-systems.com: 10.111.5.101
      g-08-09.qa1.eucalyptus-systems.com: 10.111.5.151
    midonet-api-url: http://10.111.1.41:8080/midonet-api
    repo-password: 8yU8Pj6h
    repo-username: eucalyptus
    yum-options: --nogpg
    zookeepers:
    - 10.111.1.41:2181
"""
from cloud_admin.cloudview import ConfigBlock

class MidokuraBuilder(ConfigBlock):
    pass


class BgpBuilder(ConfigBlock):
    pass


class Cassandras(ConfigBlock):
    pass


class ZooKeepers(ConfigBlock):
    pass