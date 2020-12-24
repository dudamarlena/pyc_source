# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/gcp_spanner_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 19463 bytes
import six
from airflow import AirflowException
from airflow.contrib.hooks.gcp_spanner_hook import CloudSpannerHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class CloudSpannerInstanceDeployOperator(BaseOperator):
    """CloudSpannerInstanceDeployOperator"""
    template_fields = ('project_id', 'instance_id', 'configuration_name', 'display_name',
                       'gcp_conn_id')

    @apply_defaults
    def __init__(self, instance_id, configuration_name, node_count, display_name, project_id=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        self.instance_id = instance_id
        self.project_id = project_id
        self.configuration_name = configuration_name
        self.node_count = node_count
        self.display_name = display_name
        self.gcp_conn_id = gcp_conn_id
        self._validate_inputs()
        self._hook = CloudSpannerHook(gcp_conn_id=gcp_conn_id)
        (super(CloudSpannerInstanceDeployOperator, self).__init__)(*args, **kwargs)

    def _validate_inputs(self):
        if self.project_id == '':
            raise AirflowException("The required parameter 'project_id' is empty")
        if not self.instance_id:
            raise AirflowException("The required parameter 'instance_id' is empty or None")

    def execute(self, context):
        if not self._hook.get_instance(project_id=(self.project_id), instance_id=(self.instance_id)):
            self.log.info("Creating Cloud Spanner instance '%s'", self.instance_id)
            func = self._hook.create_instance
        else:
            self.log.info("Updating Cloud Spanner instance '%s'", self.instance_id)
            func = self._hook.update_instance
        func(project_id=(self.project_id), instance_id=(self.instance_id),
          configuration_name=(self.configuration_name),
          node_count=(self.node_count),
          display_name=(self.display_name))


class CloudSpannerInstanceDeleteOperator(BaseOperator):
    """CloudSpannerInstanceDeleteOperator"""
    template_fields = ('project_id', 'instance_id', 'gcp_conn_id')

    @apply_defaults
    def __init__(self, instance_id, project_id=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        self.instance_id = instance_id
        self.project_id = project_id
        self.gcp_conn_id = gcp_conn_id
        self._validate_inputs()
        self._hook = CloudSpannerHook(gcp_conn_id=gcp_conn_id)
        (super(CloudSpannerInstanceDeleteOperator, self).__init__)(*args, **kwargs)

    def _validate_inputs(self):
        if self.project_id == '':
            raise AirflowException("The required parameter 'project_id' is empty")
        if not self.instance_id:
            raise AirflowException("The required parameter 'instance_id' is empty or None")

    def execute(self, context):
        if self._hook.get_instance(project_id=(self.project_id), instance_id=(self.instance_id)):
            return self._hook.delete_instance(project_id=(self.project_id), instance_id=(self.instance_id))
        else:
            self.log.info("Instance '%s' does not exist in project '%s'. Aborting delete.", self.instance_id, self.project_id)
            return True


class CloudSpannerInstanceDatabaseQueryOperator(BaseOperator):
    """CloudSpannerInstanceDatabaseQueryOperator"""
    template_fields = ('project_id', 'instance_id', 'database_id', 'query', 'gcp_conn_id')
    template_ext = ('.sql', )

    @apply_defaults
    def __init__(self, instance_id, database_id, query, project_id=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        self.instance_id = instance_id
        self.project_id = project_id
        self.database_id = database_id
        self.query = query
        self.gcp_conn_id = gcp_conn_id
        self._validate_inputs()
        self._hook = CloudSpannerHook(gcp_conn_id=gcp_conn_id)
        (super(CloudSpannerInstanceDatabaseQueryOperator, self).__init__)(*args, **kwargs)

    def _validate_inputs(self):
        if self.project_id == '':
            raise AirflowException("The required parameter 'project_id' is empty")
        else:
            if not self.instance_id:
                raise AirflowException("The required parameter 'instance_id' is empty or None")
            if not self.database_id:
                raise AirflowException("The required parameter 'database_id' is empty or None")
            raise self.query or AirflowException("The required parameter 'query' is empty")

    def execute(self, context):
        queries = self.query
        if isinstance(self.query, six.string_types):
            queries = [x.strip() for x in self.query.split(';')]
            self.sanitize_queries(queries)
        self.log.info('Executing DML query(-ies) on projects/%s/instances/%s/databases/%s', self.project_id, self.instance_id, self.database_id)
        self.log.info(queries)
        self._hook.execute_dml(project_id=(self.project_id), instance_id=(self.instance_id),
          database_id=(self.database_id),
          queries=queries)

    @staticmethod
    def sanitize_queries(queries):
        if len(queries):
            if queries[(-1)] == '':
                del queries[-1]


class CloudSpannerInstanceDatabaseDeployOperator(BaseOperator):
    """CloudSpannerInstanceDatabaseDeployOperator"""
    template_fields = ('project_id', 'instance_id', 'database_id', 'ddl_statements',
                       'gcp_conn_id')
    template_ext = ('.sql', )

    @apply_defaults
    def __init__(self, instance_id, database_id, ddl_statements, project_id=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        self.instance_id = instance_id
        self.project_id = project_id
        self.database_id = database_id
        self.ddl_statements = ddl_statements
        self.gcp_conn_id = gcp_conn_id
        self._validate_inputs()
        self._hook = CloudSpannerHook(gcp_conn_id=gcp_conn_id)
        (super(CloudSpannerInstanceDatabaseDeployOperator, self).__init__)(*args, **kwargs)

    def _validate_inputs(self):
        if self.project_id == '':
            raise AirflowException("The required parameter 'project_id' is empty")
        else:
            if not self.instance_id:
                raise AirflowException("The required parameter 'instance_id' is empty or None")
            raise self.database_id or AirflowException("The required parameter 'database_id' is empty or None")

    def execute(self, context):
        if not self._hook.get_database(project_id=(self.project_id), instance_id=(self.instance_id),
          database_id=(self.database_id)):
            self.log.info("Creating Cloud Spanner database '%s' in project '%s' and instance '%s'", self.database_id, self.project_id, self.instance_id)
            return self._hook.create_database(project_id=(self.project_id), instance_id=(self.instance_id),
              database_id=(self.database_id),
              ddl_statements=(self.ddl_statements))
        else:
            self.log.info("The database '%s' in project '%s' and instance '%s' already exists. Nothing to do. Exiting.", self.database_id, self.project_id, self.instance_id)
            return True


class CloudSpannerInstanceDatabaseUpdateOperator(BaseOperator):
    """CloudSpannerInstanceDatabaseUpdateOperator"""
    template_fields = ('project_id', 'instance_id', 'database_id', 'ddl_statements',
                       'gcp_conn_id')
    template_ext = ('.sql', )

    @apply_defaults
    def __init__(self, instance_id, database_id, ddl_statements, project_id=None, operation_id=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        self.instance_id = instance_id
        self.project_id = project_id
        self.database_id = database_id
        self.ddl_statements = ddl_statements
        self.operation_id = operation_id
        self.gcp_conn_id = gcp_conn_id
        self._validate_inputs()
        self._hook = CloudSpannerHook(gcp_conn_id=gcp_conn_id)
        (super(CloudSpannerInstanceDatabaseUpdateOperator, self).__init__)(*args, **kwargs)

    def _validate_inputs(self):
        if self.project_id == '':
            raise AirflowException("The required parameter 'project_id' is empty")
        else:
            if not self.instance_id:
                raise AirflowException("The required parameter 'instance_id' is empty or None")
            if not self.database_id:
                raise AirflowException("The required parameter 'database_id' is empty or None")
            raise self.ddl_statements or AirflowException("The required parameter 'ddl_statements' is empty or None")

    def execute(self, context):
        if not self._hook.get_database(project_id=(self.project_id), instance_id=(self.instance_id),
          database_id=(self.database_id)):
            raise AirflowException("The Cloud Spanner database '{}' in project '{}' and instance '{}' is missing. Create the database first before you can update it.".format(self.database_id, self.project_id, self.instance_id))
        else:
            return self._hook.update_database(project_id=(self.project_id), instance_id=(self.instance_id),
              database_id=(self.database_id),
              ddl_statements=(self.ddl_statements),
              operation_id=(self.operation_id))


class CloudSpannerInstanceDatabaseDeleteOperator(BaseOperator):
    """CloudSpannerInstanceDatabaseDeleteOperator"""
    template_fields = ('project_id', 'instance_id', 'database_id', 'gcp_conn_id')

    @apply_defaults
    def __init__(self, instance_id, database_id, project_id=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        self.instance_id = instance_id
        self.project_id = project_id
        self.database_id = database_id
        self.gcp_conn_id = gcp_conn_id
        self._validate_inputs()
        self._hook = CloudSpannerHook(gcp_conn_id=gcp_conn_id)
        (super(CloudSpannerInstanceDatabaseDeleteOperator, self).__init__)(*args, **kwargs)

    def _validate_inputs(self):
        if self.project_id == '':
            raise AirflowException("The required parameter 'project_id' is empty")
        else:
            if not self.instance_id:
                raise AirflowException("The required parameter 'instance_id' is empty or None")
            raise self.database_id or AirflowException("The required parameter 'database_id' is empty or None")

    def execute(self, context):
        db = self._hook.get_database(project_id=(self.project_id), instance_id=(self.instance_id),
          database_id=(self.database_id))
        if not db:
            self.log.info("The Cloud Spanner database was missing: '%s' in project '%s' and instance '%s'. Assuming success.", self.database_id, self.project_id, self.instance_id)
            return True
        else:
            return self._hook.delete_database(project_id=(self.project_id), instance_id=(self.instance_id),
              database_id=(self.database_id))