# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/gcp_bigtable_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 21222 bytes
from typing import Iterable
import google.api_core.exceptions
from airflow import AirflowException
from airflow.models import BaseOperator
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.contrib.hooks.gcp_bigtable_hook import BigtableHook
from airflow.utils.decorators import apply_defaults
from google.cloud.bigtable_admin_v2 import enums
from google.cloud.bigtable.table import ClusterState

class BigtableValidationMixin(object):
    """BigtableValidationMixin"""
    REQUIRED_ATTRIBUTES = []

    def _validate_inputs(self):
        for attr_name in self.REQUIRED_ATTRIBUTES:
            if not getattr(self, attr_name):
                raise AirflowException('Empty parameter: {}'.format(attr_name))


class BigtableInstanceCreateOperator(BaseOperator, BigtableValidationMixin):
    """BigtableInstanceCreateOperator"""
    REQUIRED_ATTRIBUTES = ('instance_id', 'main_cluster_id', 'main_cluster_zone')
    template_fields = ['project_id', 'instance_id', 'main_cluster_id',
     'main_cluster_zone']

    @apply_defaults
    def __init__(self, instance_id, main_cluster_id, main_cluster_zone, project_id=None, replica_cluster_id=None, replica_cluster_zone=None, instance_display_name=None, instance_type=None, instance_labels=None, cluster_nodes=None, cluster_storage_type=None, timeout=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        self.project_id = project_id
        self.instance_id = instance_id
        self.main_cluster_id = main_cluster_id
        self.main_cluster_zone = main_cluster_zone
        self.replica_cluster_id = replica_cluster_id
        self.replica_cluster_zone = replica_cluster_zone
        self.instance_display_name = instance_display_name
        self.instance_type = instance_type
        self.instance_labels = instance_labels
        self.cluster_nodes = cluster_nodes
        self.cluster_storage_type = cluster_storage_type
        self.timeout = timeout
        self._validate_inputs()
        self.hook = BigtableHook(gcp_conn_id=gcp_conn_id)
        (super(BigtableInstanceCreateOperator, self).__init__)(*args, **kwargs)

    def execute(self, context):
        instance = self.hook.get_instance(project_id=(self.project_id), instance_id=(self.instance_id))
        if instance:
            self.log.info("The instance '%s' already exists in this project. Consider it as created", self.instance_id)
            return
        try:
            self.hook.create_instance(project_id=(self.project_id),
              instance_id=(self.instance_id),
              main_cluster_id=(self.main_cluster_id),
              main_cluster_zone=(self.main_cluster_zone),
              replica_cluster_id=(self.replica_cluster_id),
              replica_cluster_zone=(self.replica_cluster_zone),
              instance_display_name=(self.instance_display_name),
              instance_type=(self.instance_type),
              instance_labels=(self.instance_labels),
              cluster_nodes=(self.cluster_nodes),
              cluster_storage_type=(self.cluster_storage_type),
              timeout=(self.timeout))
        except google.api_core.exceptions.GoogleAPICallError as e:
            self.log.error('An error occurred. Exiting.')
            raise e


class BigtableInstanceDeleteOperator(BaseOperator, BigtableValidationMixin):
    """BigtableInstanceDeleteOperator"""
    REQUIRED_ATTRIBUTES = ('instance_id', )
    template_fields = ['project_id', 'instance_id']

    @apply_defaults
    def __init__(self, instance_id, project_id=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        self.project_id = project_id
        self.instance_id = instance_id
        self._validate_inputs()
        self.hook = BigtableHook(gcp_conn_id=gcp_conn_id)
        (super(BigtableInstanceDeleteOperator, self).__init__)(*args, **kwargs)

    def execute(self, context):
        try:
            self.hook.delete_instance(project_id=(self.project_id), instance_id=(self.instance_id))
        except google.api_core.exceptions.NotFound:
            self.log.info("The instance '%s' does not exist in project '%s'. Consider it as deleted", self.instance_id, self.project_id)
        except google.api_core.exceptions.GoogleAPICallError as e:
            self.log.error('An error occurred. Exiting.')
            raise e


class BigtableTableCreateOperator(BaseOperator, BigtableValidationMixin):
    """BigtableTableCreateOperator"""
    REQUIRED_ATTRIBUTES = ('instance_id', 'table_id')
    template_fields = ['project_id', 'instance_id', 'table_id']

    @apply_defaults
    def __init__(self, instance_id, table_id, project_id=None, initial_split_keys=None, column_families=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        self.project_id = project_id
        self.instance_id = instance_id
        self.table_id = table_id
        self.initial_split_keys = initial_split_keys or list()
        self.column_families = column_families or dict()
        self._validate_inputs()
        self.hook = BigtableHook(gcp_conn_id=gcp_conn_id)
        self.instance = None
        (super(BigtableTableCreateOperator, self).__init__)(*args, **kwargs)

    def _compare_column_families(self):
        table_column_families = self.hook.get_column_families_for_table(self.instance, self.table_id)
        if set(table_column_families.keys()) != set(self.column_families.keys()):
            self.log.error("Table '%s' has different set of Column Families", self.table_id)
            self.log.error('Expected: %s', self.column_families.keys())
            self.log.error('Actual: %s', table_column_families.keys())
            return False
        else:
            for key in table_column_families.keys():
                if table_column_families[key].gc_rule != self.column_families[key]:
                    self.log.error("Column Family '%s' differs for table '%s'.", key, self.table_id)
                    return False

            return True

    def execute(self, context):
        self.instance = self.hook.get_instance(project_id=(self.project_id), instance_id=(self.instance_id))
        if not self.instance:
            raise AirflowException("Dependency: instance '{}' does not exist in project '{}'.".format(self.instance_id, self.project_id))
        try:
            self.hook.create_table(instance=(self.instance),
              table_id=(self.table_id),
              initial_split_keys=(self.initial_split_keys),
              column_families=(self.column_families))
        except google.api_core.exceptions.AlreadyExists:
            if not self._compare_column_families():
                raise AirflowException("Table '{}' already exists with different Column Families.".format(self.table_id))
            self.log.info("The table '%s' already exists. Consider it as created", self.table_id)


class BigtableTableDeleteOperator(BaseOperator, BigtableValidationMixin):
    """BigtableTableDeleteOperator"""
    REQUIRED_ATTRIBUTES = ('instance_id', 'table_id')
    template_fields = ['project_id', 'instance_id', 'table_id']

    @apply_defaults
    def __init__(self, instance_id, table_id, project_id=None, app_profile_id=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        self.project_id = project_id
        self.instance_id = instance_id
        self.table_id = table_id
        self.app_profile_id = app_profile_id
        self._validate_inputs()
        self.hook = BigtableHook(gcp_conn_id=gcp_conn_id)
        (super(BigtableTableDeleteOperator, self).__init__)(*args, **kwargs)

    def execute(self, context):
        instance = self.hook.get_instance(project_id=(self.project_id), instance_id=(self.instance_id))
        if not instance:
            raise AirflowException("Dependency: instance '{}' does not exist.".format(self.instance_id))
        try:
            self.hook.delete_table(project_id=(self.project_id),
              instance_id=(self.instance_id),
              table_id=(self.table_id))
        except google.api_core.exceptions.NotFound:
            self.log.info("The table '%s' no longer exists. Consider it as deleted", self.table_id)
        except google.api_core.exceptions.GoogleAPICallError as e:
            self.log.error('An error occurred. Exiting.')
            raise e


class BigtableClusterUpdateOperator(BaseOperator, BigtableValidationMixin):
    """BigtableClusterUpdateOperator"""
    REQUIRED_ATTRIBUTES = ('instance_id', 'cluster_id', 'nodes')
    template_fields = ['project_id', 'instance_id', 'cluster_id', 'nodes']

    @apply_defaults
    def __init__(self, instance_id, cluster_id, nodes, project_id=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        self.project_id = project_id
        self.instance_id = instance_id
        self.cluster_id = cluster_id
        self.nodes = nodes
        self._validate_inputs()
        self.hook = BigtableHook(gcp_conn_id=gcp_conn_id)
        (super(BigtableClusterUpdateOperator, self).__init__)(*args, **kwargs)

    def execute(self, context):
        instance = self.hook.get_instance(project_id=(self.project_id), instance_id=(self.instance_id))
        if not instance:
            raise AirflowException("Dependency: instance '{}' does not exist.".format(self.instance_id))
        try:
            self.hook.update_cluster(instance=instance,
              cluster_id=(self.cluster_id),
              nodes=(self.nodes))
        except google.api_core.exceptions.NotFound:
            raise AirflowException("Dependency: cluster '{}' does not exist for instance '{}'.".format(self.cluster_id, self.instance_id))
        except google.api_core.exceptions.GoogleAPICallError as e:
            self.log.error('An error occurred. Exiting.')
            raise e


class BigtableTableWaitForReplicationSensor(BaseSensorOperator, BigtableValidationMixin):
    """BigtableTableWaitForReplicationSensor"""
    REQUIRED_ATTRIBUTES = ('instance_id', 'table_id')
    template_fields = ['project_id', 'instance_id', 'table_id']

    @apply_defaults
    def __init__(self, instance_id, table_id, project_id=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        self.project_id = project_id
        self.instance_id = instance_id
        self.table_id = table_id
        self._validate_inputs()
        self.hook = BigtableHook(gcp_conn_id=gcp_conn_id)
        (super(BigtableTableWaitForReplicationSensor, self).__init__)(*args, **kwargs)

    def poke(self, context):
        instance = self.hook.get_instance(project_id=(self.project_id), instance_id=(self.instance_id))
        if not instance:
            self.log.info("Dependency: instance '%s' does not exist.", self.instance_id)
            return False
        try:
            cluster_states = self.hook.get_cluster_states_for_table(instance=instance, table_id=(self.table_id))
        except google.api_core.exceptions.NotFound:
            self.log.info("Dependency: table '%s' does not exist in instance '%s'.", self.table_id, self.instance_id)
            return False
        else:
            ready_state = ClusterState(enums.Table.ClusterState.ReplicationState.READY)
            is_table_replicated = True
            for cluster_id in cluster_states.keys():
                if cluster_states[cluster_id] != ready_state:
                    self.log.info("Table '%s' is not yet replicated on cluster '%s'.", self.table_id, cluster_id)
                    is_table_replicated = False

            if not is_table_replicated:
                return False
            else:
                self.log.info("Table '%s' is replicated.", self.table_id)
                return True