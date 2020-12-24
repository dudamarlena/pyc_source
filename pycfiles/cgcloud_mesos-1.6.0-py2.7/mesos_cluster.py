# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cgcloud/mesos/mesos_cluster.py
# Compiled at: 2016-11-22 15:21:45
from cgcloud.core.cluster import Cluster
from cgcloud.mesos.mesos_box import MesosMaster, MesosSlave

class MesosCluster(Cluster):

    @property
    def worker_role(self):
        return MesosSlave

    @property
    def leader_role(self):
        return MesosMaster