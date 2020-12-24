# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/gcp_transfer_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 29792 bytes
from copy import deepcopy
from datetime import date, time
from airflow import AirflowException
from airflow.contrib.hooks.gcp_transfer_hook import GCPTransferServiceHook, GcpTransferJobsStatus, TRANSFER_OPTIONS, OBJECT_CONDITIONS, PROJECT_ID, BUCKET_NAME, GCS_DATA_SINK, STATUS, DESCRIPTION, GCS_DATA_SOURCE, HTTP_DATA_SOURCE, SECONDS, MINUTES, HOURS, YEAR, MONTH, DAY, START_TIME_OF_DAY, SCHEDULE_END_DATE, SCHEDULE_START_DATE, SCHEDULE, SECRET_ACCESS_KEY, ACCESS_KEY_ID, AWS_ACCESS_KEY, AWS_S3_DATA_SOURCE, TRANSFER_SPEC
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
try:
    from airflow.contrib.hooks.aws_hook import AwsHook
except ImportError:
    AwsHook = None

class TransferJobPreprocessor:

    def __init__(self, body, aws_conn_id='aws_default', default_schedule=False):
        self.body = body
        self.aws_conn_id = aws_conn_id
        self.default_schedule = default_schedule

    def _inject_aws_credentials(self):
        if TRANSFER_SPEC not in self.body or AWS_S3_DATA_SOURCE not in self.body[TRANSFER_SPEC]:
            return
        aws_hook = AwsHook(self.aws_conn_id)
        aws_credentials = aws_hook.get_credentials()
        aws_access_key_id = aws_credentials.access_key
        aws_secret_access_key = aws_credentials.secret_key
        self.body[TRANSFER_SPEC][AWS_S3_DATA_SOURCE][AWS_ACCESS_KEY] = {ACCESS_KEY_ID: aws_access_key_id, 
         SECRET_ACCESS_KEY: aws_secret_access_key}

    def _reformat_date(self, field_key):
        schedule = self.body[SCHEDULE]
        if field_key not in schedule:
            return
        if isinstance(schedule[field_key], date):
            schedule[field_key] = self._convert_date_to_dict(schedule[field_key])

    def _reformat_time(self, field_key):
        schedule = self.body[SCHEDULE]
        if field_key not in schedule:
            return
        if isinstance(schedule[field_key], time):
            schedule[field_key] = self._convert_time_to_dict(schedule[field_key])

    def _reformat_schedule(self):
        if SCHEDULE not in self.body:
            if self.default_schedule:
                self.body[SCHEDULE] = {SCHEDULE_START_DATE: date.today(), 
                 SCHEDULE_END_DATE: date.today()}
            else:
                return
        self._reformat_date(SCHEDULE_START_DATE)
        self._reformat_date(SCHEDULE_END_DATE)
        self._reformat_time(START_TIME_OF_DAY)

    def process_body(self):
        self._inject_aws_credentials()
        self._reformat_schedule()
        return self.body

    @staticmethod
    def _convert_date_to_dict(field_date):
        """
        Convert native python ``datetime.date`` object  to a format supported by the API
        """
        return {DAY: field_date.day, MONTH: field_date.month, YEAR: field_date.year}

    @staticmethod
    def _convert_time_to_dict(time):
        """
        Convert native python ``datetime.time`` object  to a format supported by the API
        """
        return {HOURS: time.hour, MINUTES: time.minute, SECONDS: time.second}


class TransferJobValidator:

    def __init__(self, body):
        self.body = body

    def _verify_data_source(self):
        is_gcs = GCS_DATA_SOURCE in self.body[TRANSFER_SPEC]
        is_aws_s3 = AWS_S3_DATA_SOURCE in self.body[TRANSFER_SPEC]
        is_http = HTTP_DATA_SOURCE in self.body[TRANSFER_SPEC]
        sources_count = sum([is_gcs, is_aws_s3, is_http])
        if sources_count != 0:
            if sources_count != 1:
                raise AirflowException('More than one data source detected. Please choose exactly one data source from: gcsDataSource, awsS3DataSource and httpDataSource.')

    def _restrict_aws_credentials(self):
        if AWS_S3_DATA_SOURCE not in self.body[TRANSFER_SPEC]:
            return
        if AWS_ACCESS_KEY in self.body[TRANSFER_SPEC][AWS_S3_DATA_SOURCE]:
            raise AirflowException('AWS credentials detected inside the body parameter (awsAccessKey). This is not allowed, please use Airflow connections to store credentials.')

    def _restrict_empty_body(self):
        if not self.body:
            raise AirflowException("The required parameter 'body' is empty or None")

    def validate_body(self):
        self._restrict_empty_body()
        if TRANSFER_SPEC not in self.body:
            return
        self._restrict_aws_credentials()
        self._verify_data_source()


class GcpTransferServiceJobCreateOperator(BaseOperator):
    __doc__ = '\n    Creates a transfer job that runs periodically.\n\n    .. warning::\n\n        This operator is NOT idempotent. If you run it many times, many transfer\n        jobs will be created in the Google Cloud Platform.\n\n    .. seealso::\n        For more information on how to use this operator, take a look at the guide:\n        :ref:`howto/operator:GcpTransferServiceJobCreateOperator`\n\n    :param body: (Required) The request body, as described in\n        https://cloud.google.com/storage-transfer/docs/reference/rest/v1/transferJobs/create#request-body\n        With three additional improvements:\n\n        * dates can be given in the form :class:`datetime.date`\n        * times can be given in the form :class:`datetime.time`\n        * credentials to Amazon Web Service should be stored in the connection and indicated by the\n          aws_conn_id parameter\n\n    :type body: dict\n    :param aws_conn_id: The connection ID used to retrieve credentials to\n        Amazon Web Service.\n    :type aws_conn_id: str\n    :param gcp_conn_id: The connection ID used to connect to Google Cloud\n        Platform.\n    :type gcp_conn_id: str\n    :param api_version: API version used (e.g. v1).\n    :type api_version: str\n    '
    template_fields = ('body', 'gcp_conn_id', 'aws_conn_id')

    @apply_defaults
    def __init__(self, body, aws_conn_id='aws_default', gcp_conn_id='google_cloud_default', api_version='v1', *args, **kwargs):
        (super(GcpTransferServiceJobCreateOperator, self).__init__)(*args, **kwargs)
        self.body = deepcopy(body)
        self.aws_conn_id = aws_conn_id
        self.gcp_conn_id = gcp_conn_id
        self.api_version = api_version
        self._validate_inputs()

    def _validate_inputs(self):
        TransferJobValidator(body=(self.body)).validate_body()

    def execute(self, context):
        TransferJobPreprocessor(body=(self.body), aws_conn_id=(self.aws_conn_id)).process_body()
        hook = GCPTransferServiceHook(api_version=(self.api_version), gcp_conn_id=(self.gcp_conn_id))
        return hook.create_transfer_job(body=(self.body))


class GcpTransferServiceJobUpdateOperator(BaseOperator):
    __doc__ = '\n    Updates a transfer job that runs periodically.\n\n    .. seealso::\n        For more information on how to use this operator, take a look at the guide:\n        :ref:`howto/operator:GcpTransferServiceJobUpdateOperator`\n\n    :param job_name: (Required) Name of the job to be updated\n    :type job_name: str\n    :param body: (Required) The request body, as described in\n        https://cloud.google.com/storage-transfer/docs/reference/rest/v1/transferJobs/patch#request-body\n        With three additional improvements:\n\n        * dates can be given in the form :class:`datetime.date`\n        * times can be given in the form :class:`datetime.time`\n        * credentials to Amazon Web Service should be stored in the connection and indicated by the\n          aws_conn_id parameter\n\n    :type body: dict\n    :param aws_conn_id: The connection ID used to retrieve credentials to\n        Amazon Web Service.\n    :type aws_conn_id: str\n    :param gcp_conn_id: The connection ID used to connect to Google Cloud\n        Platform.\n    :type gcp_conn_id: str\n    :param api_version: API version used (e.g. v1).\n    :type api_version: str\n    '
    template_fields = ('job_name', 'body', 'gcp_conn_id', 'aws_conn_id')

    @apply_defaults
    def __init__(self, job_name, body, aws_conn_id='aws_default', gcp_conn_id='google_cloud_default', api_version='v1', *args, **kwargs):
        (super(GcpTransferServiceJobUpdateOperator, self).__init__)(*args, **kwargs)
        self.job_name = job_name
        self.body = body
        self.gcp_conn_id = gcp_conn_id
        self.api_version = api_version
        self.aws_conn_id = aws_conn_id
        self._validate_inputs()

    def _validate_inputs(self):
        TransferJobValidator(body=(self.body)).validate_body()
        if not self.job_name:
            raise AirflowException("The required parameter 'job_name' is empty or None")

    def execute(self, context):
        TransferJobPreprocessor(body=(self.body), aws_conn_id=(self.aws_conn_id)).process_body()
        hook = GCPTransferServiceHook(api_version=(self.api_version), gcp_conn_id=(self.gcp_conn_id))
        return hook.update_transfer_job(job_name=(self.job_name), body=(self.body))


class GcpTransferServiceJobDeleteOperator(BaseOperator):
    __doc__ = '\n    Delete a transfer job. This is a soft delete. After a transfer job is\n    deleted, the job and all the transfer executions are subject to garbage\n    collection. Transfer jobs become eligible for garbage collection\n    30 days after soft delete.\n\n    .. seealso::\n        For more information on how to use this operator, take a look at the guide:\n        :ref:`howto/operator:GcpTransferServiceJobDeleteOperator`\n\n    :param job_name: (Required) Name of the TRANSFER operation\n    :type job_name: str\n    :param project_id: (Optional) the ID of the project that owns the Transfer\n        Job. If set to None or missing, the default project_id from the GCP\n        connection is used.\n    :type project_id: str\n    :param gcp_conn_id: The connection ID used to connect to Google Cloud\n        Platform.\n    :type gcp_conn_id: str\n    :param api_version: API version used (e.g. v1).\n    :type api_version: str\n    '
    template_fields = ('job_name', 'project_id', 'gcp_conn_id', 'api_version')

    @apply_defaults
    def __init__(self, job_name, gcp_conn_id='google_cloud_default', api_version='v1', project_id=None, *args, **kwargs):
        (super(GcpTransferServiceJobDeleteOperator, self).__init__)(*args, **kwargs)
        self.job_name = job_name
        self.project_id = project_id
        self.gcp_conn_id = gcp_conn_id
        self.api_version = api_version
        self._validate_inputs()

    def _validate_inputs(self):
        if not self.job_name:
            raise AirflowException("The required parameter 'job_name' is empty or None")

    def execute(self, context):
        self._validate_inputs()
        hook = GCPTransferServiceHook(api_version=(self.api_version), gcp_conn_id=(self.gcp_conn_id))
        hook.delete_transfer_job(job_name=(self.job_name), project_id=(self.project_id))


class GcpTransferServiceOperationGetOperator(BaseOperator):
    __doc__ = '\n    Gets the latest state of a long-running operation in Google Storage Transfer\n    Service.\n\n    .. seealso::\n        For more information on how to use this operator, take a look at the guide:\n        :ref:`howto/operator:GcpTransferServiceOperationGetOperator`\n\n    :param operation_name: (Required) Name of the transfer operation.\n    :type operation_name: str\n    :param gcp_conn_id: The connection ID used to connect to Google\n        Cloud Platform.\n    :type gcp_conn_id: str\n    :param api_version: API version used (e.g. v1).\n    :type api_version: str\n    '
    template_fields = ('operation_name', 'gcp_conn_id')

    @apply_defaults
    def __init__(self, operation_name, gcp_conn_id='google_cloud_default', api_version='v1', *args, **kwargs):
        (super(GcpTransferServiceOperationGetOperator, self).__init__)(*args, **kwargs)
        self.operation_name = operation_name
        self.gcp_conn_id = gcp_conn_id
        self.api_version = api_version
        self._validate_inputs()

    def _validate_inputs(self):
        if not self.operation_name:
            raise AirflowException("The required parameter 'operation_name' is empty or None")

    def execute(self, context):
        hook = GCPTransferServiceHook(api_version=(self.api_version), gcp_conn_id=(self.gcp_conn_id))
        operation = hook.get_transfer_operation(operation_name=(self.operation_name))
        return operation


class GcpTransferServiceOperationsListOperator(BaseOperator):
    __doc__ = '\n    Lists long-running operations in Google Storage Transfer\n    Service that match the specified filter.\n\n    .. seealso::\n        For more information on how to use this operator, take a look at the guide:\n        :ref:`howto/operator:GcpTransferServiceOperationsListOperator`\n\n    :param filter: (Required) A request filter, as described in\n            https://cloud.google.com/storage-transfer/docs/reference/rest/v1/transferJobs/list#body.QUERY_PARAMETERS.filter\n    :type filter: dict\n    :param gcp_conn_id: The connection ID used to connect to Google\n        Cloud Platform.\n    :type gcp_conn_id: str\n    :param api_version: API version used (e.g. v1).\n    :type api_version: str\n    '
    template_fields = ('filter', 'gcp_conn_id')

    def __init__(self, filter, gcp_conn_id='google_cloud_default', api_version='v1', *args, **kwargs):
        (super(GcpTransferServiceOperationsListOperator, self).__init__)(*args, **kwargs)
        self.filter = filter
        self.gcp_conn_id = gcp_conn_id
        self.api_version = api_version
        self._validate_inputs()

    def _validate_inputs(self):
        if not self.filter:
            raise AirflowException("The required parameter 'filter' is empty or None")

    def execute(self, context):
        hook = GCPTransferServiceHook(api_version=(self.api_version), gcp_conn_id=(self.gcp_conn_id))
        operations_list = hook.list_transfer_operations(filter=(self.filter))
        self.log.info(operations_list)
        return operations_list


class GcpTransferServiceOperationPauseOperator(BaseOperator):
    __doc__ = '\n    Pauses a transfer operation in Google Storage Transfer Service.\n\n    .. seealso::\n        For more information on how to use this operator, take a look at the guide:\n        :ref:`howto/operator:GcpTransferServiceOperationPauseOperator`\n\n    :param operation_name: (Required) Name of the transfer operation.\n    :type operation_name: str\n    :param gcp_conn_id: The connection ID used to connect to Google Cloud Platform.\n    :type gcp_conn_id: str\n    :param api_version:  API version used (e.g. v1).\n    :type api_version: str\n    '
    template_fields = ('operation_name', 'gcp_conn_id', 'api_version')

    @apply_defaults
    def __init__(self, operation_name, gcp_conn_id='google_cloud_default', api_version='v1', *args, **kwargs):
        (super(GcpTransferServiceOperationPauseOperator, self).__init__)(*args, **kwargs)
        self.operation_name = operation_name
        self.gcp_conn_id = gcp_conn_id
        self.api_version = api_version
        self._validate_inputs()

    def _validate_inputs(self):
        if not self.operation_name:
            raise AirflowException("The required parameter 'operation_name' is empty or None")

    def execute(self, context):
        hook = GCPTransferServiceHook(api_version=(self.api_version), gcp_conn_id=(self.gcp_conn_id))
        hook.pause_transfer_operation(operation_name=(self.operation_name))


class GcpTransferServiceOperationResumeOperator(BaseOperator):
    __doc__ = '\n    Resumes a transfer operation in Google Storage Transfer Service.\n\n    .. seealso::\n        For more information on how to use this operator, take a look at the guide:\n        :ref:`howto/operator:GcpTransferServiceOperationResumeOperator`\n\n    :param operation_name: (Required) Name of the transfer operation.\n    :type operation_name: str\n    :param gcp_conn_id: The connection ID used to connect to Google Cloud Platform.\n    :param api_version: API version used (e.g. v1).\n    :type api_version: str\n    :type gcp_conn_id: str\n    '
    template_fields = ('operation_name', 'gcp_conn_id', 'api_version')

    @apply_defaults
    def __init__(self, operation_name, gcp_conn_id='google_cloud_default', api_version='v1', *args, **kwargs):
        self.operation_name = operation_name
        self.gcp_conn_id = gcp_conn_id
        self.api_version = api_version
        self._validate_inputs()
        (super(GcpTransferServiceOperationResumeOperator, self).__init__)(*args, **kwargs)

    def _validate_inputs(self):
        if not self.operation_name:
            raise AirflowException("The required parameter 'operation_name' is empty or None")

    def execute(self, context):
        hook = GCPTransferServiceHook(api_version=(self.api_version), gcp_conn_id=(self.gcp_conn_id))
        hook.resume_transfer_operation(operation_name=(self.operation_name))


class GcpTransferServiceOperationCancelOperator(BaseOperator):
    __doc__ = '\n    Cancels a transfer operation in Google Storage Transfer Service.\n\n    .. seealso::\n        For more information on how to use this operator, take a look at the guide:\n        :ref:`howto/operator:GcpTransferServiceOperationCancelOperator`\n\n    :param operation_name: (Required) Name of the transfer operation.\n    :type operation_name: str\n    :param api_version: API version used (e.g. v1).\n    :type api_version: str\n    :param gcp_conn_id: The connection ID used to connect to Google\n        Cloud Platform.\n    :type gcp_conn_id: str\n    '
    template_fields = ('operation_name', 'gcp_conn_id', 'api_version')

    @apply_defaults
    def __init__(self, operation_name, api_version='v1', gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(GcpTransferServiceOperationCancelOperator, self).__init__)(*args, **kwargs)
        self.operation_name = operation_name
        self.api_version = api_version
        self.gcp_conn_id = gcp_conn_id
        self._validate_inputs()

    def _validate_inputs(self):
        if not self.operation_name:
            raise AirflowException("The required parameter 'operation_name' is empty or None")

    def execute(self, context):
        hook = GCPTransferServiceHook(api_version=(self.api_version), gcp_conn_id=(self.gcp_conn_id))
        hook.cancel_transfer_operation(operation_name=(self.operation_name))


class S3ToGoogleCloudStorageTransferOperator(BaseOperator):
    __doc__ = "\n    Synchronizes an S3 bucket with a Google Cloud Storage bucket using the\n    GCP Storage Transfer Service.\n\n    .. warning::\n\n        This operator is NOT idempotent. If you run it many times, many transfer\n        jobs will be created in the Google Cloud Platform.\n\n    **Example**:\n\n    .. code-block:: python\n\n       s3_to_gcs_transfer_op = S3ToGoogleCloudStorageTransferOperator(\n            task_id='s3_to_gcs_transfer_example',\n            s3_bucket='my-s3-bucket',\n            project_id='my-gcp-project',\n            gcs_bucket='my-gcs-bucket',\n            dag=my_dag)\n\n    :param s3_bucket: The S3 bucket where to find the objects. (templated)\n    :type s3_bucket: str\n    :param gcs_bucket: The destination Google Cloud Storage bucket\n        where you want to store the files. (templated)\n    :type gcs_bucket: str\n    :param project_id: Optional ID of the Google Cloud Platform Console project that\n        owns the job\n    :type project_id: str\n    :param aws_conn_id: The source S3 connection\n    :type aws_conn_id: str\n    :param gcp_conn_id: The destination connection ID to use\n        when connecting to Google Cloud Storage.\n    :type gcp_conn_id: str\n    :param delegate_to: The account to impersonate, if any.\n        For this to work, the service account making the request must have\n        domain-wide delegation enabled.\n    :type delegate_to: str\n    :param description: Optional transfer service job description\n    :type description: str\n    :param schedule: Optional transfer service schedule;\n        If not set, run transfer job once as soon as the operator runs\n        The format is described\n        https://cloud.google.com/storage-transfer/docs/reference/rest/v1/transferJobs.\n        With two additional improvements:\n\n        * dates they can be passed as :class:`datetime.date`\n        * times they can be passed as :class:`datetime.time`\n\n    :type schedule: dict\n    :param object_conditions: Optional transfer service object conditions; see\n        https://cloud.google.com/storage-transfer/docs/reference/rest/v1/TransferSpec\n    :type object_conditions: dict\n    :param transfer_options: Optional transfer service transfer options; see\n        https://cloud.google.com/storage-transfer/docs/reference/rest/v1/TransferSpec\n    :type transfer_options: dict\n    :param wait: Wait for transfer to finish\n    :type wait: bool\n    :param timeout: Time to wait for the operation to end in seconds\n    :type timeout: int\n    "
    template_fields = ('gcp_conn_id', 's3_bucket', 'gcs_bucket', 'description', 'object_conditions')
    ui_color = '#e09411'

    @apply_defaults
    def __init__(self, s3_bucket, gcs_bucket, project_id=None, aws_conn_id='aws_default', gcp_conn_id='google_cloud_default', delegate_to=None, description=None, schedule=None, object_conditions=None, transfer_options=None, wait=True, timeout=None, *args, **kwargs):
        (super(S3ToGoogleCloudStorageTransferOperator, self).__init__)(*args, **kwargs)
        self.s3_bucket = s3_bucket
        self.gcs_bucket = gcs_bucket
        self.project_id = project_id
        self.aws_conn_id = aws_conn_id
        self.gcp_conn_id = gcp_conn_id
        self.delegate_to = delegate_to
        self.description = description
        self.schedule = schedule
        self.object_conditions = object_conditions
        self.transfer_options = transfer_options
        self.wait = wait
        self.timeout = timeout

    def execute(self, context):
        hook = GCPTransferServiceHook(gcp_conn_id=(self.gcp_conn_id), delegate_to=(self.delegate_to))
        body = self._create_body()
        TransferJobPreprocessor(body=body, aws_conn_id=(self.aws_conn_id), default_schedule=True).process_body()
        job = hook.create_transfer_job(body=body)
        if self.wait:
            hook.wait_for_transfer_job(job, timeout=(self.timeout))

    def _create_body(self):
        body = {DESCRIPTION: self.description, 
         STATUS: GcpTransferJobsStatus.ENABLED, 
         TRANSFER_SPEC: {AWS_S3_DATA_SOURCE: {BUCKET_NAME: self.s3_bucket}, 
                         GCS_DATA_SINK: {BUCKET_NAME: self.gcs_bucket}}}
        if self.project_id is not None:
            body[PROJECT_ID] = self.project_id
        if self.schedule is not None:
            body[SCHEDULE] = self.schedule
        if self.object_conditions is not None:
            body[TRANSFER_SPEC][OBJECT_CONDITIONS] = self.object_conditions
        if self.transfer_options is not None:
            body[TRANSFER_SPEC][TRANSFER_OPTIONS] = self.transfer_options
        return body


class GoogleCloudStorageToGoogleCloudStorageTransferOperator(BaseOperator):
    __doc__ = "\n    Copies objects from a bucket to another using the GCP Storage Transfer\n    Service.\n\n    .. warning::\n\n        This operator is NOT idempotent. If you run it many times, many transfer\n        jobs will be created in the Google Cloud Platform.\n\n    **Example**:\n\n    .. code-block:: python\n\n       gcs_to_gcs_transfer_op = GoogleCloudStorageToGoogleCloudStorageTransferOperator(\n            task_id='gcs_to_gcs_transfer_example',\n            source_bucket='my-source-bucket',\n            destination_bucket='my-destination-bucket',\n            project_id='my-gcp-project',\n            dag=my_dag)\n\n    :param source_bucket: The source Google cloud storage bucket where the\n         object is. (templated)\n    :type source_bucket: str\n    :param destination_bucket: The destination Google cloud storage bucket\n        where the object should be. (templated)\n    :type destination_bucket: str\n    :param project_id: The ID of the Google Cloud Platform Console project that\n        owns the job\n    :type project_id: str\n    :param gcp_conn_id: Optional connection ID to use when connecting to Google Cloud\n        Storage.\n    :type gcp_conn_id: str\n    :param delegate_to: The account to impersonate, if any.\n        For this to work, the service account making the request must have\n        domain-wide delegation enabled.\n    :type delegate_to: str\n    :param description: Optional transfer service job description\n    :type description: str\n    :param schedule: Optional transfer service schedule;\n        If not set, run transfer job once as soon as the operator runs\n        See:\n        https://cloud.google.com/storage-transfer/docs/reference/rest/v1/transferJobs.\n        With two additional improvements:\n\n        * dates they can be passed as :class:`datetime.date`\n        * times they can be passed as :class:`datetime.time`\n\n    :type schedule: dict\n    :param object_conditions: Optional transfer service object conditions; see\n        https://cloud.google.com/storage-transfer/docs/reference/rest/v1/TransferSpec#ObjectConditions\n    :type object_conditions: dict\n    :param transfer_options: Optional transfer service transfer options; see\n        https://cloud.google.com/storage-transfer/docs/reference/rest/v1/TransferSpec#TransferOptions\n    :type transfer_options: dict\n    :param wait: Wait for transfer to finish; defaults to `True`\n    :type wait: bool\n    :param timeout: Time to wait for the operation to end in seconds\n    :type timeout: int\n    "
    template_fields = ('gcp_conn_id', 'source_bucket', 'destination_bucket', 'description',
                       'object_conditions')
    ui_color = '#e09411'

    @apply_defaults
    def __init__(self, source_bucket, destination_bucket, project_id=None, gcp_conn_id='google_cloud_default', delegate_to=None, description=None, schedule=None, object_conditions=None, transfer_options=None, wait=True, timeout=None, *args, **kwargs):
        (super(GoogleCloudStorageToGoogleCloudStorageTransferOperator, self).__init__)(*args, **kwargs)
        self.source_bucket = source_bucket
        self.destination_bucket = destination_bucket
        self.project_id = project_id
        self.gcp_conn_id = gcp_conn_id
        self.delegate_to = delegate_to
        self.description = description
        self.schedule = schedule
        self.object_conditions = object_conditions
        self.transfer_options = transfer_options
        self.wait = wait
        self.timeout = timeout

    def execute(self, context):
        hook = GCPTransferServiceHook(gcp_conn_id=(self.gcp_conn_id), delegate_to=(self.delegate_to))
        body = self._create_body()
        TransferJobPreprocessor(body=body, default_schedule=True).process_body()
        job = hook.create_transfer_job(body=body)
        if self.wait:
            hook.wait_for_transfer_job(job, timeout=(self.timeout))

    def _create_body(self):
        body = {DESCRIPTION: self.description, 
         STATUS: GcpTransferJobsStatus.ENABLED, 
         TRANSFER_SPEC: {GCS_DATA_SOURCE: {BUCKET_NAME: self.source_bucket}, 
                         GCS_DATA_SINK: {BUCKET_NAME: self.destination_bucket}}}
        if self.project_id is not None:
            body[PROJECT_ID] = self.project_id
        if self.schedule is not None:
            body[SCHEDULE] = self.schedule
        if self.object_conditions is not None:
            body[TRANSFER_SPEC][OBJECT_CONDITIONS] = self.object_conditions
        if self.transfer_options is not None:
            body[TRANSFER_SPEC][TRANSFER_OPTIONS] = self.transfer_options
        return body