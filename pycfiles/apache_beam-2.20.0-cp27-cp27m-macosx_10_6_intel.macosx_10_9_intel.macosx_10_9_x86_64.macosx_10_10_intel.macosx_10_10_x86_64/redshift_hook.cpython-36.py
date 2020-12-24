# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/hooks/redshift_hook.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 4426 bytes
from airflow.contrib.hooks.aws_hook import AwsHook

class RedshiftHook(AwsHook):
    """RedshiftHook"""

    def get_conn(self):
        return self.get_client_type('redshift')

    def cluster_status(self, cluster_identifier):
        """
        Return status of a cluster

        :param cluster_identifier: unique identifier of a cluster
        :type cluster_identifier: str
        """
        conn = self.get_conn()
        try:
            response = conn.describe_clusters(ClusterIdentifier=cluster_identifier)['Clusters']
            if response:
                return response[0]['ClusterStatus']
            return
        except conn.exceptions.ClusterNotFoundFault:
            return 'cluster_not_found'

    def delete_cluster(self, cluster_identifier, skip_final_cluster_snapshot=True, final_cluster_snapshot_identifier=''):
        """
        Delete a cluster and optionally create a snapshot

        :param cluster_identifier: unique identifier of a cluster
        :type cluster_identifier: str
        :param skip_final_cluster_snapshot: determines cluster snapshot creation
        :type skip_final_cluster_snapshot: bool
        :param final_cluster_snapshot_identifier: name of final cluster snapshot
        :type final_cluster_snapshot_identifier: str
        """
        response = self.get_conn().delete_cluster(ClusterIdentifier=cluster_identifier,
          SkipFinalClusterSnapshot=skip_final_cluster_snapshot,
          FinalClusterSnapshotIdentifier=final_cluster_snapshot_identifier)
        if response['Cluster']:
            return response['Cluster']

    def describe_cluster_snapshots(self, cluster_identifier):
        """
        Gets a list of snapshots for a cluster

        :param cluster_identifier: unique identifier of a cluster
        :type cluster_identifier: str
        """
        response = self.get_conn().describe_cluster_snapshots(ClusterIdentifier=cluster_identifier)
        if 'Snapshots' not in response:
            return
        else:
            snapshots = response['Snapshots']
            snapshots = filter(lambda x: x['Status'], snapshots)
            snapshots.sort(key=(lambda x: x['SnapshotCreateTime']), reverse=True)
            return snapshots

    def restore_from_cluster_snapshot(self, cluster_identifier, snapshot_identifier):
        """
        Restores a cluster from its snapshot

        :param cluster_identifier: unique identifier of a cluster
        :type cluster_identifier: str
        :param snapshot_identifier: unique identifier for a snapshot of a cluster
        :type snapshot_identifier: str
        """
        response = self.get_conn().restore_from_cluster_snapshot(ClusterIdentifier=cluster_identifier,
          SnapshotIdentifier=snapshot_identifier)
        if response['Cluster']:
            return response['Cluster']

    def create_cluster_snapshot(self, snapshot_identifier, cluster_identifier):
        """
        Creates a snapshot of a cluster

        :param snapshot_identifier: unique identifier for a snapshot of a cluster
        :type snapshot_identifier: str
        :param cluster_identifier: unique identifier of a cluster
        :type cluster_identifier: str
        """
        response = self.get_conn().create_cluster_snapshot(SnapshotIdentifier=snapshot_identifier,
          ClusterIdentifier=cluster_identifier)
        if response['Snapshot']:
            return response['Snapshot']