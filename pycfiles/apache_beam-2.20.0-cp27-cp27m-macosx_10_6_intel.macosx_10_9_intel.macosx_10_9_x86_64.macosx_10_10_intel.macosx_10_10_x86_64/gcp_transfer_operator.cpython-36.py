# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
    """GcpTransferServiceJobCreateOperator"""
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
    """GcpTransferServiceJobUpdateOperator"""
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
    """GcpTransferServiceJobDeleteOperator"""
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
    """GcpTransferServiceOperationGetOperator"""
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
    """GcpTransferServiceOperationsListOperator"""
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
    """GcpTransferServiceOperationPauseOperator"""
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
    """GcpTransferServiceOperationResumeOperator"""
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
    """GcpTransferServiceOperationCancelOperator"""
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
    """S3ToGoogleCloudStorageTransferOperator"""
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
    """GoogleCloudStorageToGoogleCloudStorageTransferOperator"""
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