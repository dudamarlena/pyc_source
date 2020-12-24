# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cgcloud/toil/toil_cluster.py
# Compiled at: 2016-11-22 15:21:45
from cgcloud.core.cluster import Cluster
from cgcloud.toil.toil_box import ToilLeader, ToilWorker

class ToilCluster(Cluster):

    @property
    def worker_role(self):
        return ToilWorker

    @property
    def leader_role(self):
        return ToilLeader