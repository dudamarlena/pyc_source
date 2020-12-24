# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cgcloud/core/cluster.py
# Compiled at: 2016-11-22 15:21:45
import logging
from abc import ABCMeta, abstractproperty
from cgcloud.core.box import Box
from cgcloud.lib.util import abreviated_snake_case_class_name, papply, thread_pool
log = logging.getLogger(__name__)

class Cluster(object):
    """
    A cluster consists of one leader box and N worker boxes. A box that is part of a cluster is
    referred to as "node". There is one role (subclass of Box) describing the leader node and
    another one describing the workers. Leader and worker roles are siblings and their common
    ancestor--the node role--describes the software deployed on them, which is identical for both
    leader and workers. The node role is used to create the single image from which the actual
    nodes will be booted from when the cluster is created. In other words, the specialization
    into leader and workers happens at cluster creation time, not earlier.
    """
    __metaclass__ = ABCMeta

    def __init__(self, ctx):
        super(Cluster, self).__init__()
        self.ctx = ctx

    @abstractproperty
    def leader_role(self):
        """
        :return: The Box subclass to use for the leader
        """
        raise NotImplementedError()

    @abstractproperty
    def worker_role(self):
        """
        :return: The Box subclass to use for the workers
        """
        raise NotImplementedError()

    @classmethod
    def name(cls):
        return abreviated_snake_case_class_name(cls, Cluster)

    def apply(self, f, cluster_name=None, ordinal=None, leader_first=True, skip_leader=False, wait_ready=True, operation='operation', pool_size=None, callback=None):
        """
        Apply a callable to the leader and each worker. The callable may be applied to multiple
        workers concurrently.
        """
        leader = self.leader_role(self.ctx)
        leader.bind(cluster_name=cluster_name, ordinal=ordinal, wait_ready=wait_ready)
        first_worker = self.worker_role(self.ctx)

        def apply_leader():
            if not skip_leader:
                log.info('=== Performing %s on leader ===', operation)
                result = f(leader)
                if callback is not None:
                    callback(result)
            return

        def apply_workers():
            log.info('=== Performing %s on workers ===', operation)
            workers = first_worker.list(leader_instance_id=leader.instance_id, wait_ready=wait_ready)
            papply(f, seq=zip(workers), pool_size=pool_size, callback=callback)

        if leader_first:
            apply_leader()
            apply_workers()
        else:
            apply_workers()
            apply_leader()


class ClusterBox(Box):
    """
    A mixin for a box that is part of a cluster
    """

    def _set_instance_options(self, options):
        super(ClusterBox, self)._set_instance_options(options)
        self.ebs_volume_size = int(options.get('ebs_volume_size') or 0)

    def _get_instance_options(self):
        return dict(super(ClusterBox, self)._get_instance_options(), ebs_volume_size=str(self.ebs_volume_size), leader_instance_id=self.instance_id)

    @classmethod
    def _get_node_role(cls):
        """
        Return the role (box class) from which the node image should be created.
        """
        while cls not in (ClusterBox, ClusterLeader, ClusterWorker, Box):
            if ClusterBox in cls.__bases__:
                return cls
            cls = cls.__bases__[0]

        assert False, "Class %s doesn't have an ancestor that mixes in %s" % (cls, ClusterBox)

    def _image_name_prefix(self):
        return self._get_node_role().role()

    def _security_group_name(self):
        return self._get_node_role().role()


class ClusterLeader(ClusterBox):
    """
    A mixin for a box that serves as a leader in a cluster
    """

    def _get_instance_options(self):
        return dict(super(ClusterLeader, self)._get_instance_options())


class ClusterWorker(ClusterBox):
    """
    A mixin for a box that serves as a leader in a cluster
    """

    def __init__(self, ctx):
        super(ClusterWorker, self).__init__(ctx)
        self.leader_instance_id = None
        return

    def _set_instance_options(self, options):
        super(ClusterWorker, self)._set_instance_options(options)
        self.leader_instance_id = options.get('leader_instance_id')
        if self.cluster_name is None:
            self.cluster_name = self.leader_instance_id
        return

    def _get_instance_options(self):
        return dict(super(ClusterWorker, self)._get_instance_options(), leader_instance_id=self.leader_instance_id)