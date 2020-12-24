# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/gcp_spanner_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 19463 bytes
import six
from airflow import AirflowException
from airflow.contrib.hooks.gcp_spanner_hook import CloudSpannerHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class CloudSpannerInstanceDeployOperator(BaseOperator):
    __doc__ = '\n    Creates a new Cloud Spanner instance, or if an instance with the same instance_id\n    exists in the specified project, updates the Cloud Spanner instance.\n\n    :param instance_id: Cloud Spanner instance ID.\n    :type instance_id: str\n    :param configuration_name:  The name of the Cloud Spanner instance configuration\n      defining how the instance will be created. Required for\n      instances that do not yet exist.\n    :type configuration_name: str\n    :param node_count: (Optional) The number of nodes allocated to the Cloud Spanner\n      instance.\n    :type node_count: int\n    :param display_name: (Optional) The display name for the Cloud Spanner  instance in\n      the GCP Console. (Must be between 4 and 30 characters.) If this value is not set\n      in the constructor, the name is the same as the instance ID.\n    :type display_name: str\n    :param project_id: Optional, the ID of the project which owns the Cloud Spanner\n        Database.  If set to None or missing, the default project_id from the GCP connection is used.\n    :type project_id: str\n    :param gcp_conn_id: The connection ID used to connect to Google Cloud Platform.\n    :type gcp_conn_id: str\n    '
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
    __doc__ = '\n    Deletes a Cloud Spanner instance. If an instance does not exist,\n    no action is taken and the operator succeeds.\n\n    .. seealso::\n        For more information on how to use this operator, take a look at the guide:\n        :ref:`howto/operator:CloudSpannerInstanceDeleteOperator`\n\n    :param instance_id: The Cloud Spanner instance ID.\n    :type instance_id: str\n    :param project_id: Optional, the ID of the project that owns the Cloud Spanner\n        Database.  If set to None or missing, the default project_id from the GCP connection is used.\n    :type project_id: str\n    :param gcp_conn_id: The connection ID used to connect to Google Cloud Platform.\n    :type gcp_conn_id: str\n    '
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
    __doc__ = '\n    Executes an arbitrary DML query (INSERT, UPDATE, DELETE).\n\n    .. seealso::\n        For more information on how to use this operator, take a look at the guide:\n        :ref:`howto/operator:CloudSpannerInstanceDatabaseQueryOperator`\n\n    :param instance_id: The Cloud Spanner instance ID.\n    :type instance_id: str\n    :param database_id: The Cloud Spanner database ID.\n    :type database_id: str\n    :param query: The query or list of queries to be executed. Can be a path to a SQL\n       file.\n    :type query: str or list\n    :param project_id: Optional, the ID of the project that owns the Cloud Spanner\n        Database.  If set to None or missing, the default project_id from the GCP connection is used.\n    :type project_id: str\n    :param gcp_conn_id: The connection ID used to connect to Google Cloud Platform.\n    :type gcp_conn_id: str\n    '
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
    __doc__ = '\n    Creates a new Cloud Spanner database, or if database exists,\n    the operator does nothing.\n\n    .. seealso::\n        For more information on how to use this operator, take a look at the guide:\n        :ref:`howto/operator:CloudSpannerInstanceDatabaseDeployOperator`\n\n    :param instance_id: The Cloud Spanner instance ID.\n    :type instance_id: str\n    :param database_id: The Cloud Spanner database ID.\n    :type database_id: str\n    :param ddl_statements: The string list containing DDL for the new database.\n    :type ddl_statements: list[str]\n    :param project_id: Optional, the ID of the project that owns the Cloud Spanner\n        Database.  If set to None or missing, the default project_id from the GCP connection is used.\n    :type project_id: str\n    :param gcp_conn_id: The connection ID used to connect to Google Cloud Platform.\n    :type gcp_conn_id: str\n    '
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
    __doc__ = '\n    Updates a Cloud Spanner database with the specified DDL statement.\n\n    .. seealso::\n        For more information on how to use this operator, take a look at the guide:\n        :ref:`howto/operator:CloudSpannerInstanceDatabaseUpdateOperator`\n\n    :param instance_id: The Cloud Spanner instance ID.\n    :type instance_id: str\n    :param database_id: The Cloud Spanner database ID.\n    :type database_id: str\n    :param ddl_statements: The string list containing DDL to apply to the database.\n    :type ddl_statements: list[str]\n    :param project_id: Optional, the ID of the project that owns the the Cloud Spanner\n        Database.  If set to None or missing, the default project_id from the GCP connection is used.\n    :type project_id: str\n    :param operation_id: (Optional) Unique per database operation id that can\n           be specified to implement idempotency check.\n    :type operation_id: str\n    :param gcp_conn_id: The connection ID used to connect to Google Cloud Platform.\n    :type gcp_conn_id: str\n    '
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
    __doc__ = '\n    Deletes a Cloud Spanner database.\n\n    .. seealso::\n        For more information on how to use this operator, take a look at the guide:\n        :ref:`howto/operator:CloudSpannerInstanceDatabaseDeleteOperator`\n\n    :param instance_id: Cloud Spanner instance ID.\n    :type instance_id: str\n    :param database_id: Cloud Spanner database ID.\n    :type database_id: str\n    :param project_id: Optional, the ID of the project that owns the Cloud Spanner\n        Database.  If set to None or missing, the default project_id from the GCP connection is used.\n    :type project_id: str\n    :param gcp_conn_id: The connection ID used to connect to Google Cloud Platform.\n    :type gcp_conn_id: str\n    '
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