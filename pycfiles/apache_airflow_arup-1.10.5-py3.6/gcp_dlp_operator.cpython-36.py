# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/gcp_dlp_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 80088 bytes
"""
This module contains various GCP Cloud DLP operators
which allow you to perform basic operations using
Cloud DLP.
"""
from airflow.contrib.hooks.gcp_dlp_hook import CloudDLPHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class CloudDLPCancelDLPJobOperator(BaseOperator):
    __doc__ = '\n    Starts asynchronous cancellation on a long-running DlpJob.\n\n    :param dlp_job_id: ID of the DLP job resource to be cancelled.\n    :type dlp_job_id: str\n    :param project_id: (Optional) Google Cloud Platform project ID where the\n        DLP Instance exists. If set to None or missing, the default project_id\n        from the GCP connection is used.\n    :type project_id: str\n    :param retry: (Optional) A retry object used to retry requests.\n        If None is specified, requests will not be retried.\n    :type retry: google.api_core.retry.Retry\n    :param timeout: (Optional) The amount of time, in seconds, to wait for the request\n        to complete. Note that if retry is specified, the timeout applies to each\n        individual attempt.\n    :type timeout: float\n    :param metadata: (Optional) Additional metadata that is provided to the method.\n    :type metadata: sequence[tuple[str, str]]]\n    :param gcp_conn_id: (Optional) The connection ID used to connect to Google Cloud Platform.\n    :type gcp_conn_id: str\n    '
    template_fields = ('dlp_job_id', 'project_id', 'gcp_conn_id')

    @apply_defaults
    def __init__(self, dlp_job_id, project_id=None, retry=None, timeout=None, metadata=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(CloudDLPCancelDLPJobOperator, self).__init__)(*args, **kwargs)
        self.dlp_job_id = dlp_job_id
        self.project_id = project_id
        self.retry = retry
        self.timeout = timeout
        self.metadata = metadata
        self.gcp_conn_id = gcp_conn_id

    def execute(self, context):
        hook = CloudDLPHook(gcp_conn_id=(self.gcp_conn_id))
        hook.cancel_dlp_job(dlp_job_id=(self.dlp_job_id),
          project_id=(self.project_id),
          retry=(self.retry),
          timeout=(self.timeout),
          metadata=(self.metadata))


class CloudDLPCreateDeidentifyTemplateOperator(BaseOperator):
    __doc__ = '\n    Creates a DeidentifyTemplate for re-using frequently used configuration for\n    de-identifying content, images, and storage.\n\n    :param organization_id: (Optional) The organization ID. Required to set this\n        field if parent resource is an organzation.\n    :type organization_id: str\n    :param project_id: (Optional) Google Cloud Platform project ID where the\n        DLP Instance exists. Only set this field if the parent resource is\n        a project instead of an organzation.\n    :type project_id: str\n    :param deidentify_template: (Optional) The DeidentifyTemplate to create.\n    :type deidentify_template: dict or google.cloud.dlp_v2.types.DeidentifyTemplate\n    :param template_id: (Optional) The template ID.\n    :type template_id: str\n    :param retry: (Optional) A retry object used to retry requests.\n        If None is specified, requests will not be retried.\n    :type retry: google.api_core.retry.Retry\n    :param timeout: (Optional) The amount of time, in seconds, to wait for the request\n        to complete. Note that if retry is specified, the timeout applies to each\n        individual attempt.\n    :type timeout: float\n    :param metadata: (Optional) Additional metadata that is provided to the method.\n    :type metadata: sequence[tuple[str, str]]]\n    :param gcp_conn_id: (Optional) The connection ID used to connect to Google Cloud Platform.\n    :type gcp_conn_id: str\n    :rtype: google.cloud.dlp_v2.types.DeidentifyTemplate\n    '
    template_fields = ('organization_id', 'project_id', 'deidentify_template', 'template_id',
                       'gcp_conn_id')

    @apply_defaults
    def __init__(self, organization_id=None, project_id=None, deidentify_template=None, template_id=None, retry=None, timeout=None, metadata=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(CloudDLPCreateDeidentifyTemplateOperator, self).__init__)(*args, **kwargs)
        self.organization_id = organization_id
        self.project_id = project_id
        self.deidentify_template = deidentify_template
        self.template_id = template_id
        self.retry = retry
        self.timeout = timeout
        self.metadata = metadata
        self.gcp_conn_id = gcp_conn_id

    def execute(self, context):
        hook = CloudDLPHook(gcp_conn_id=(self.gcp_conn_id))
        return hook.create_deidentify_template(organization_id=(self.organization_id),
          project_id=(self.project_id),
          deidentify_template=(self.deidentify_template),
          template_id=(self.template_id),
          retry=(self.retry),
          timeout=(self.timeout),
          metadata=(self.metadata))


class CloudDLPCreateDLPJobOperator(BaseOperator):
    __doc__ = '\n    Creates a new job to inspect storage or calculate risk metrics.\n\n    :param project_id: (Optional) Google Cloud Platform project ID where the\n        DLP Instance exists. If set to None or missing, the default\n        project_id from the GCP connection is used.\n    :type project_id: str\n    :param inspect_job: (Optional) The configuration for the inspect job.\n    :type inspect_job: dict or google.cloud.dlp_v2.types.InspectJobConfig\n    :param risk_job: (Optional) The configuration for the risk job.\n    :type risk_job: dict or google.cloud.dlp_v2.types.RiskAnalysisJobConfig\n    :param job_id: (Optional) The job ID.\n    :type job_id: str\n    :param retry: (Optional) A retry object used to retry requests.\n        If None is specified, requests will not be retried.\n    :type retry: google.api_core.retry.Retry\n    :param timeout: (Optional) The amount of time, in seconds, to wait for the request\n        to complete. Note that if retry is specified, the timeout applies to each\n        individual attempt.\n    :type timeout: float\n    :param metadata: (Optional) Additional metadata that is provided to the method.\n    :type metadata: sequence[tuple[str, str]]]\n    :param wait_until_finished: (Optional) If true, it will keep polling the job state\n        until it is set to DONE.\n    :type wait_until_finished: bool\n    :param gcp_conn_id: (Optional) The connection ID used to connect to Google Cloud Platform.\n    :type gcp_conn_id: str\n    :rtype: google.cloud.dlp_v2.types.DlpJob\n    '
    template_fields = ('project_id', 'inspect_job', 'risk_job', 'job_id', 'gcp_conn_id')

    @apply_defaults
    def __init__(self, project_id=None, inspect_job=None, risk_job=None, job_id=None, retry=None, timeout=None, metadata=None, wait_until_finished=True, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(CloudDLPCreateDLPJobOperator, self).__init__)(*args, **kwargs)
        self.project_id = project_id
        self.inspect_job = inspect_job
        self.risk_job = risk_job
        self.job_id = job_id
        self.retry = retry
        self.timeout = timeout
        self.metadata = metadata
        self.wait_until_finished = wait_until_finished
        self.gcp_conn_id = gcp_conn_id

    def execute(self, context):
        hook = CloudDLPHook(gcp_conn_id=(self.gcp_conn_id))
        return hook.create_dlp_job(project_id=(self.project_id),
          inspect_job=(self.inspect_job),
          risk_job=(self.risk_job),
          job_id=(self.job_id),
          retry=(self.retry),
          timeout=(self.timeout),
          metadata=(self.metadata),
          wait_until_finished=(self.wait_until_finished))


class CloudDLPCreateInspectTemplateOperator(BaseOperator):
    __doc__ = '\n    Creates an InspectTemplate for re-using frequently used configuration for\n    inspecting content, images, and storage.\n\n    :param organization_id: (Optional) The organization ID. Required to set this\n        field if parent resource is an organzation.\n    :type organization_id: str\n    :param project_id: (Optional) Google Cloud Platform project ID where the\n        DLP Instance exists. Only set this field if the parent resource is\n        a project instead of an organzation.\n    :type project_id: str\n    :param inspect_template: (Optional) The InspectTemplate to create.\n    :type inspect_template: dict or google.cloud.dlp_v2.types.InspectTemplate\n    :param template_id: (Optional) The template ID.\n    :type template_id: str\n    :param retry: (Optional) A retry object used to retry requests.\n        If None is specified, requests will not be retried.\n    :type retry: google.api_core.retry.Retry\n    :param timeout: (Optional) The amount of time, in seconds, to wait for the request\n        to complete. Note that if retry is specified, the timeout applies to each\n        individual attempt.\n    :type timeout: float\n    :param metadata: (Optional) Additional metadata that is provided to the method.\n    :type metadata: sequence[tuple[str, str]]]\n    :param gcp_conn_id: (Optional) The connection ID used to connect to Google Cloud Platform.\n    :type gcp_conn_id: str\n    :rtype: google.cloud.dlp_v2.types.InspectTemplate\n    '
    template_fields = ('organization_id', 'project_id', 'inspect_template', 'template_id',
                       'gcp_conn_id')

    @apply_defaults
    def __init__(self, organization_id=None, project_id=None, inspect_template=None, template_id=None, retry=None, timeout=None, metadata=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(CloudDLPCreateInspectTemplateOperator, self).__init__)(*args, **kwargs)
        self.organization_id = organization_id
        self.project_id = project_id
        self.inspect_template = inspect_template
        self.template_id = template_id
        self.retry = retry
        self.timeout = timeout
        self.metadata = metadata
        self.gcp_conn_id = gcp_conn_id

    def execute(self, context):
        hook = CloudDLPHook(gcp_conn_id=(self.gcp_conn_id))
        return hook.create_inspect_template(organization_id=(self.organization_id),
          project_id=(self.project_id),
          inspect_template=(self.inspect_template),
          template_id=(self.template_id),
          retry=(self.retry),
          timeout=(self.timeout),
          metadata=(self.metadata))


class CloudDLPCreateJobTriggerOperator(BaseOperator):
    __doc__ = '\n    Creates a job trigger to run DLP actions such as scanning storage for sensitive\n    information on a set schedule.\n\n    :param project_id: (Optional) Google Cloud Platform project ID where the\n        DLP Instance exists. If set to None or missing, the default\n        project_id from the GCP connection is used.\n    :type project_id: str\n    :param job_trigger: (Optional) The JobTrigger to create.\n    :type job_trigger: dict or google.cloud.dlp_v2.types.JobTrigger\n    :param trigger_id: (Optional) The JobTrigger ID.\n    :type trigger_id: str\n    :param retry: (Optional) A retry object used to retry requests.\n        If None is specified, requests will not be retried.\n    :type retry: google.api_core.retry.Retry\n    :param timeout: (Optional) The amount of time, in seconds, to wait for the request\n        to complete. Note that if retry is specified, the timeout applies to each\n        individual attempt.\n    :type timeout: float\n    :param metadata: (Optional) Additional metadata that is provided to the method.\n    :type metadata: sequence[tuple[str, str]]]\n    :param gcp_conn_id: (Optional) The connection ID used to connect to Google Cloud Platform.\n    :type gcp_conn_id: str\n    :rtype: google.cloud.dlp_v2.types.JobTrigger\n    '
    template_fields = ('project_id', 'job_trigger', 'trigger_id', 'gcp_conn_id')

    @apply_defaults
    def __init__(self, project_id=None, job_trigger=None, trigger_id=None, retry=None, timeout=None, metadata=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(CloudDLPCreateJobTriggerOperator, self).__init__)(*args, **kwargs)
        self.project_id = project_id
        self.job_trigger = job_trigger
        self.trigger_id = trigger_id
        self.retry = retry
        self.timeout = timeout
        self.metadata = metadata
        self.gcp_conn_id = gcp_conn_id

    def execute(self, context):
        hook = CloudDLPHook(gcp_conn_id=(self.gcp_conn_id))
        return hook.create_job_trigger(project_id=(self.project_id),
          job_trigger=(self.job_trigger),
          trigger_id=(self.trigger_id),
          retry=(self.retry),
          timeout=(self.timeout),
          metadata=(self.metadata))


class CloudDLPCreateStoredInfoTypeOperator(BaseOperator):
    __doc__ = '\n    Creates a pre-built stored infoType to be used for inspection.\n\n    :param organization_id: (Optional) The organization ID. Required to set this\n        field if parent resource is an organzation.\n    :type organization_id: str\n    :param project_id: (Optional) Google Cloud Platform project ID where the\n        DLP Instance exists. Only set this field if the parent resource is\n        a project instead of an organzation.\n    :type project_id: str\n    :param config: (Optional) The config for the StoredInfoType.\n    :type config: dict or google.cloud.dlp_v2.types.StoredInfoTypeConfig\n    :param stored_info_type_id: (Optional) The StoredInfoType ID.\n    :type stored_info_type_id: str\n    :param retry: (Optional) A retry object used to retry requests.\n        If None is specified, requests will not be retried.\n    :type retry: google.api_core.retry.Retry\n    :param timeout: (Optional) The amount of time, in seconds, to wait for the request\n        to complete. Note that if retry is specified, the timeout applies to each\n        individual attempt.\n    :type timeout: float\n    :param metadata: (Optional) Additional metadata that is provided to the method.\n    :type metadata: sequence[tuple[str, str]]]\n    :param gcp_conn_id: (Optional) The connection ID used to connect to Google Cloud Platform.\n    :type gcp_conn_id: str\n    :rtype: google.cloud.dlp_v2.types.StoredInfoType\n    '
    template_fields = ('organization_id', 'project_id', 'config', 'stored_info_type_id',
                       'gcp_conn_id')

    @apply_defaults
    def __init__(self, organization_id=None, project_id=None, config=None, stored_info_type_id=None, retry=None, timeout=None, metadata=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(CloudDLPCreateStoredInfoTypeOperator, self).__init__)(*args, **kwargs)
        self.organization_id = organization_id
        self.project_id = project_id
        self.config = config
        self.stored_info_type_id = stored_info_type_id
        self.retry = retry
        self.timeout = timeout
        self.metadata = metadata
        self.gcp_conn_id = gcp_conn_id

    def execute(self, context):
        hook = CloudDLPHook(gcp_conn_id=(self.gcp_conn_id))
        return hook.create_stored_info_type(organization_id=(self.organization_id),
          project_id=(self.project_id),
          config=(self.config),
          stored_info_type_id=(self.stored_info_type_id),
          retry=(self.retry),
          timeout=(self.timeout),
          metadata=(self.metadata))


class CloudDLPDeidentifyContentOperator(BaseOperator):
    __doc__ = '\n    De-identifies potentially sensitive info from a ContentItem. This method has limits\n    on input size and output size.\n\n    :param project_id: (Optional) Google Cloud Platform project ID where the\n        DLP Instance exists. If set to None or missing, the default\n        project_id from the GCP connection is used.\n    :type project_id: str\n    :param deidentify_config: (Optional) Configuration for the de-identification of the\n        content item. Items specified here will override the template referenced by the\n        deidentify_template_name argument.\n    :type deidentify_config: dict or google.cloud.dlp_v2.types.DeidentifyConfig\n    :param inspect_config: (Optional) Configuration for the inspector. Items specified\n        here will override the template referenced by the inspect_template_name argument.\n    :type inspect_config: dict or google.cloud.dlp_v2.types.InspectConfig\n    :param item: (Optional) The item to de-identify. Will be treated as text.\n    :type item: dict or google.cloud.dlp_v2.types.ContentItem\n    :param inspect_template_name: (Optional) Optional template to use. Any configuration\n        directly specified in inspect_config will override those set in the template.\n    :type inspect_template_name: str\n    :param deidentify_template_name: (Optional) Optional template to use. Any\n        configuration directly specified in deidentify_config will override those set\n        in the template.\n    :type deidentify_template_name: str\n    :param retry: (Optional) A retry object used to retry requests.\n        If None is specified, requests will not be retried.\n    :type retry: google.api_core.retry.Retry\n    :param timeout: (Optional) The amount of time, in seconds, to wait for the request\n        to complete. Note that if retry is specified, the timeout applies to each\n        individual attempt.\n    :type timeout: float\n    :param metadata: (Optional) Additional metadata that is provided to the method.\n    :type metadata: sequence[tuple[str, str]]]\n    :param gcp_conn_id: (Optional) The connection ID used to connect to Google Cloud Platform.\n    :type gcp_conn_id: str\n    :rtype: google.cloud.dlp_v2.types.DeidentifyContentResponse\n    '
    template_fields = ('project_id', 'deidentify_config', 'inspect_config', 'item',
                       'inspect_template_name', 'deidentify_template_name', 'gcp_conn_id')

    @apply_defaults
    def __init__(self, project_id=None, deidentify_config=None, inspect_config=None, item=None, inspect_template_name=None, deidentify_template_name=None, retry=None, timeout=None, metadata=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(CloudDLPDeidentifyContentOperator, self).__init__)(*args, **kwargs)
        self.project_id = project_id
        self.deidentify_config = deidentify_config
        self.inspect_config = inspect_config
        self.item = item
        self.inspect_template_name = inspect_template_name
        self.deidentify_template_name = deidentify_template_name
        self.retry = retry
        self.timeout = timeout
        self.metadata = metadata
        self.gcp_conn_id = gcp_conn_id

    def execute(self, context):
        hook = CloudDLPHook(gcp_conn_id=(self.gcp_conn_id))
        return hook.deidentify_content(project_id=(self.project_id),
          deidentify_config=(self.deidentify_config),
          inspect_config=(self.inspect_config),
          item=(self.item),
          inspect_template_name=(self.inspect_template_name),
          deidentify_template_name=(self.deidentify_template_name),
          retry=(self.retry),
          timeout=(self.timeout),
          metadata=(self.metadata))


class CloudDLPDeleteDeidentifyTemplateOperator(BaseOperator):
    __doc__ = '\n    Deletes a DeidentifyTemplate.\n\n    :param template_id: The ID of deidentify template to be deleted.\n    :type template_id: str\n    :param organization_id: (Optional) The organization ID. Required to set this\n        field if parent resource is an organzation.\n    :type organization_id: str\n    :param project_id: (Optional) Google Cloud Platform project ID where the\n        DLP Instance exists. Only set this field if the parent resource is\n        a project instead of an organzation.\n    :type project_id: str\n    :param retry: (Optional) A retry object used to retry requests.\n        If None is specified, requests will not be retried.\n    :type retry: google.api_core.retry.Retry\n    :param timeout: (Optional) The amount of time, in seconds, to wait for the request\n        to complete. Note that if retry is specified, the timeout applies to each\n        individual attempt.\n    :type timeout: float\n    :param metadata: (Optional) Additional metadata that is provided to the method.\n    :type metadata: sequence[tuple[str, str]]]\n    :param gcp_conn_id: (Optional) The connection ID used to connect to Google Cloud Platform.\n    :type gcp_conn_id: str\n    '
    template_fields = ('template_id', 'organization_id', 'project_id', 'gcp_conn_id')

    @apply_defaults
    def __init__(self, template_id, organization_id=None, project_id=None, retry=None, timeout=None, metadata=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(CloudDLPDeleteDeidentifyTemplateOperator, self).__init__)(*args, **kwargs)
        self.template_id = template_id
        self.organization_id = organization_id
        self.project_id = project_id
        self.retry = retry
        self.timeout = timeout
        self.metadata = metadata
        self.gcp_conn_id = gcp_conn_id

    def execute(self, context):
        hook = CloudDLPHook(gcp_conn_id=(self.gcp_conn_id))
        hook.delete_deidentify_template(template_id=(self.template_id),
          organization_id=(self.organization_id),
          project_id=(self.project_id),
          retry=(self.retry),
          timeout=(self.timeout),
          metadata=(self.metadata))


class CloudDLPDeleteDlpJobOperator(BaseOperator):
    __doc__ = '\n    Deletes a long-running DlpJob. This method indicates that the client is no longer\n    interested in the DlpJob result. The job will be cancelled if possible.\n\n    :param dlp_job_id: The ID of the DLP job resource to be cancelled.\n    :type dlp_job_id: str\n    :param project_id: (Optional) Google Cloud Platform project ID where the\n        DLP Instance exists. If set to None or missing, the default\n        project_id from the GCP connection is used.\n    :type project_id: str\n    :param retry: (Optional) A retry object used to retry requests.\n        If None is specified, requests will not be retried.\n    :type retry: google.api_core.retry.Retry\n    :param timeout: (Optional) The amount of time, in seconds, to wait for the request\n        to complete. Note that if retry is specified, the timeout applies to each\n        individual attempt.\n    :type timeout: float\n    :param metadata: (Optional) Additional metadata that is provided to the method.\n    :type metadata: sequence[tuple[str, str]]]\n    :param gcp_conn_id: (Optional) The connection ID used to connect to Google Cloud Platform.\n    :type gcp_conn_id: str\n    '
    template_fields = ('dlp_job_id', 'project_id', 'gcp_conn_id')

    @apply_defaults
    def __init__(self, dlp_job_id, project_id=None, retry=None, timeout=None, metadata=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(CloudDLPDeleteDlpJobOperator, self).__init__)(*args, **kwargs)
        self.dlp_job_id = dlp_job_id
        self.project_id = project_id
        self.retry = retry
        self.timeout = timeout
        self.metadata = metadata
        self.gcp_conn_id = gcp_conn_id

    def execute(self, context):
        hook = CloudDLPHook(gcp_conn_id=(self.gcp_conn_id))
        hook.delete_dlp_job(dlp_job_id=(self.dlp_job_id),
          project_id=(self.project_id),
          retry=(self.retry),
          timeout=(self.timeout),
          metadata=(self.metadata))


class CloudDLPDeleteInspectTemplateOperator(BaseOperator):
    __doc__ = '\n    Deletes an InspectTemplate.\n\n    :param template_id: The ID of the inspect template to be deleted.\n    :type template_id: str\n    :param organization_id: (Optional) The organization ID. Required to set this\n        field if parent resource is an organzation.\n    :type organization_id: str\n    :param project_id: (Optional) Google Cloud Platform project ID where the\n        DLP Instance exists. Only set this field if the parent resource is\n        a project instead of an organzation.\n    :type project_id: str\n    :param retry: (Optional) A retry object used to retry requests.\n        If None is specified, requests will not be retried.\n    :type retry: google.api_core.retry.Retry\n    :param timeout: (Optional) The amount of time, in seconds, to wait for the request\n        to complete. Note that if retry is specified, the timeout applies to each\n        individual attempt.\n    :type timeout: float\n    :param metadata: (Optional) Additional metadata that is provided to the method.\n    :type metadata: sequence[tuple[str, str]]]\n    :param gcp_conn_id: (Optional) The connection ID used to connect to Google Cloud Platform.\n    :type gcp_conn_id: str\n    '
    template_fields = ('template_id', 'organization_id', 'project_id', 'gcp_conn_id')

    @apply_defaults
    def __init__(self, template_id, organization_id=None, project_id=None, retry=None, timeout=None, metadata=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(CloudDLPDeleteInspectTemplateOperator, self).__init__)(*args, **kwargs)
        self.template_id = template_id
        self.organization_id = organization_id
        self.project_id = project_id
        self.retry = retry
        self.timeout = timeout
        self.metadata = metadata
        self.gcp_conn_id = gcp_conn_id

    def execute(self, context):
        hook = CloudDLPHook(gcp_conn_id=(self.gcp_conn_id))
        hook.delete_inspect_template(template_id=(self.template_id),
          organization_id=(self.organization_id),
          project_id=(self.project_id),
          retry=(self.retry),
          timeout=(self.timeout),
          metadata=(self.metadata))


class CloudDLPDeleteJobTriggerOperator(BaseOperator):
    __doc__ = '\n    Deletes a job trigger.\n\n    :param job_trigger_id: The ID of the DLP job trigger to be deleted.\n    :type job_trigger_id: str\n    :param project_id: (Optional) Google Cloud Platform project ID where the\n        DLP Instance exists. If set to None or missing, the default\n        project_id from the GCP connection is used.\n    :type project_id: str\n    :param retry: (Optional) A retry object used to retry requests.\n        If None is specified, requests will not be retried.\n    :type retry: google.api_core.retry.Retry\n    :param timeout: (Optional) The amount of time, in seconds, to wait for the request\n        to complete. Note that if retry is specified, the timeout applies to each\n        individual attempt.\n    :type timeout: float\n    :param metadata: (Optional) Additional metadata that is provided to the method.\n    :type metadata: sequence[tuple[str, str]]]\n    :param gcp_conn_id: (Optional) The connection ID used to connect to Google Cloud Platform.\n    :type gcp_conn_id: str\n    '
    template_fields = ('job_trigger_id', 'project_id', 'gcp_conn_id')

    @apply_defaults
    def __init__(self, job_trigger_id, project_id=None, retry=None, timeout=None, metadata=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(CloudDLPDeleteJobTriggerOperator, self).__init__)(*args, **kwargs)
        self.job_trigger_id = job_trigger_id
        self.project_id = project_id
        self.retry = retry
        self.timeout = timeout
        self.metadata = metadata
        self.gcp_conn_id = gcp_conn_id

    def execute(self, context):
        hook = CloudDLPHook(gcp_conn_id=(self.gcp_conn_id))
        hook.delete_job_trigger(job_trigger_id=(self.job_trigger_id),
          project_id=(self.project_id),
          retry=(self.retry),
          timeout=(self.timeout),
          metadata=(self.metadata))


class CloudDLPDeleteStoredInfoTypeOperator(BaseOperator):
    __doc__ = '\n    Deletes a stored infoType.\n\n    :param stored_info_type_id: The ID of the stored info type to be deleted.\n    :type stored_info_type_id: str\n    :param organization_id: (Optional) The organization ID. Required to set this\n        field if parent resource is an organzation.\n    :type organization_id: str\n    :param project_id: (Optional) Google Cloud Platform project ID where the\n        DLP Instance exists. Only set this field if the parent resource is\n        a project instead of an organzation.\n    :type project_id: str\n    :param retry: (Optional) A retry object used to retry requests.\n        If None is specified, requests will not be retried.\n    :type retry: google.api_core.retry.Retry\n    :param timeout: (Optional) The amount of time, in seconds, to wait for the request\n        to complete. Note that if retry is specified, the timeout applies to each\n        individual attempt.\n    :type timeout: float\n    :param metadata: (Optional) Additional metadata that is provided to the method.\n    :type metadata: sequence[tuple[str, str]]]\n    :param gcp_conn_id: (Optional) The connection ID used to connect to Google Cloud Platform.\n    :type gcp_conn_id: str\n    '
    template_fields = ('stored_info_type_id', 'organization_id', 'project_id', 'gcp_conn_id')

    @apply_defaults
    def __init__(self, stored_info_type_id, organization_id=None, project_id=None, retry=None, timeout=None, metadata=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(CloudDLPDeleteStoredInfoTypeOperator, self).__init__)(*args, **kwargs)
        self.stored_info_type_id = stored_info_type_id
        self.organization_id = organization_id
        self.project_id = project_id
        self.retry = retry
        self.timeout = timeout
        self.metadata = metadata
        self.gcp_conn_id = gcp_conn_id

    def execute(self, context):
        hook = CloudDLPHook(gcp_conn_id=(self.gcp_conn_id))
        hook.delete_stored_info_type(stored_info_type_id=(self.stored_info_type_id),
          organization_id=(self.organization_id),
          project_id=(self.project_id),
          retry=(self.retry),
          timeout=(self.timeout),
          metadata=(self.metadata))


class CloudDLPGetDeidentifyTemplateOperator(BaseOperator):
    __doc__ = '\n    Gets a DeidentifyTemplate.\n\n    :param template_id: The ID of deidentify template to be read.\n    :type template_id: str\n    :param organization_id: (Optional) The organization ID. Required to set this\n        field if parent resource is an organzation.\n    :type organization_id: str\n    :param project_id: (Optional) Google Cloud Platform project ID where the\n        DLP Instance exists. Only set this field if the parent resource is\n        a project instead of an organzation.\n    :type project_id: str\n    :param retry: (Optional) A retry object used to retry requests.\n        If None is specified, requests will not be retried.\n    :type retry: google.api_core.retry.Retry\n    :param timeout: (Optional) The amount of time, in seconds, to wait for the request\n        to complete. Note that if retry is specified, the timeout applies to each\n        individual attempt.\n    :type timeout: float\n    :param metadata: (Optional) Additional metadata that is provided to the method.\n    :type metadata: sequence[tuple[str, str]]]\n    :param gcp_conn_id: (Optional) The connection ID used to connect to Google Cloud Platform.\n    :type gcp_conn_id: str\n    :rtype: google.cloud.dlp_v2.types.DeidentifyTemplate\n    '
    template_fields = ('template_id', 'organization_id', 'project_id', 'gcp_conn_id')

    @apply_defaults
    def __init__(self, template_id, organization_id=None, project_id=None, retry=None, timeout=None, metadata=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(CloudDLPGetDeidentifyTemplateOperator, self).__init__)(*args, **kwargs)
        self.template_id = template_id
        self.organization_id = organization_id
        self.project_id = project_id
        self.retry = retry
        self.timeout = timeout
        self.metadata = metadata
        self.gcp_conn_id = gcp_conn_id

    def execute(self, context):
        hook = CloudDLPHook(gcp_conn_id=(self.gcp_conn_id))
        return hook.get_deidentify_template(template_id=(self.template_id),
          organization_id=(self.organization_id),
          project_id=(self.project_id),
          retry=(self.retry),
          timeout=(self.timeout),
          metadata=(self.metadata))


class CloudDLPGetDlpJobOperator(BaseOperator):
    __doc__ = '\n    Gets the latest state of a long-running DlpJob.\n\n    :param dlp_job_id: The ID of the DLP job resource to be read.\n    :type dlp_job_id: str\n    :param project_id: (Optional) Google Cloud Platform project ID where the\n        DLP Instance exists. If set to None or missing, the default\n        project_id from the GCP connection is used.\n    :type project_id: str\n    :param retry: (Optional) A retry object used to retry requests.\n        If None is specified, requests will not be retried.\n    :type retry: google.api_core.retry.Retry\n    :param timeout: (Optional) The amount of time, in seconds, to wait for the request\n        to complete. Note that if retry is specified, the timeout applies to each\n        individual attempt.\n    :type timeout: float\n    :param metadata: (Optional) Additional metadata that is provided to the method.\n    :type metadata: sequence[tuple[str, str]]]\n    :param gcp_conn_id: (Optional) The connection ID used to connect to Google Cloud Platform.\n    :type gcp_conn_id: str\n    :rtype: google.cloud.dlp_v2.types.DlpJob\n    '
    template_fields = ('dlp_job_id', 'project_id', 'gcp_conn_id')

    @apply_defaults
    def __init__(self, dlp_job_id, project_id=None, retry=None, timeout=None, metadata=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(CloudDLPGetDlpJobOperator, self).__init__)(*args, **kwargs)
        self.dlp_job_id = dlp_job_id
        self.project_id = project_id
        self.retry = retry
        self.timeout = timeout
        self.metadata = metadata
        self.gcp_conn_id = gcp_conn_id

    def execute(self, context):
        hook = CloudDLPHook(gcp_conn_id=(self.gcp_conn_id))
        return hook.get_dlp_job(dlp_job_id=(self.dlp_job_id),
          project_id=(self.project_id),
          retry=(self.retry),
          timeout=(self.timeout),
          metadata=(self.metadata))


class CloudDLPGetInspectTemplateOperator(BaseOperator):
    __doc__ = '\n    Gets an InspectTemplate.\n\n    :param template_id: The ID of inspect template to be read.\n    :type template_id: str\n    :param organization_id: (Optional) The organization ID. Required to set this\n        field if parent resource is an organzation.\n    :type organization_id: str\n    :param project_id: (Optional) Google Cloud Platform project ID where the\n        DLP Instance exists. Only set this field if the parent resource is\n        a project instead of an organzation.\n    :type project_id: str\n    :param retry: (Optional) A retry object used to retry requests.\n        If None is specified, requests will not be retried.\n    :type retry: google.api_core.retry.Retry\n    :param timeout: (Optional) The amount of time, in seconds, to wait for the request\n        to complete. Note that if retry is specified, the timeout applies to each\n        individual attempt.\n    :type timeout: float\n    :param metadata: (Optional) Additional metadata that is provided to the method.\n    :type metadata: sequence[tuple[str, str]]]\n    :param gcp_conn_id: (Optional) The connection ID used to connect to Google Cloud Platform.\n    :type gcp_conn_id: str\n    :rtype: google.cloud.dlp_v2.types.InspectTemplate\n    '
    template_fields = ('template_id', 'organization_id', 'project_id', 'gcp_conn_id')

    @apply_defaults
    def __init__(self, template_id, organization_id=None, project_id=None, retry=None, timeout=None, metadata=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(CloudDLPGetInspectTemplateOperator, self).__init__)(*args, **kwargs)
        self.template_id = template_id
        self.organization_id = organization_id
        self.project_id = project_id
        self.retry = retry
        self.timeout = timeout
        self.metadata = metadata
        self.gcp_conn_id = gcp_conn_id

    def execute(self, context):
        hook = CloudDLPHook(gcp_conn_id=(self.gcp_conn_id))
        return hook.get_inspect_template(template_id=(self.template_id),
          organization_id=(self.organization_id),
          project_id=(self.project_id),
          retry=(self.retry),
          timeout=(self.timeout),
          metadata=(self.metadata))


class CloudDLPGetJobTripperOperator(BaseOperator):
    __doc__ = '\n    Gets a job trigger.\n\n    :param job_trigger_id: The ID of the DLP job trigger to be read.\n    :type job_trigger_id: str\n    :param project_id: (Optional) Google Cloud Platform project ID where the\n        DLP Instance exists. If set to None or missing, the default\n        project_id from the GCP connection is used.\n    :type project_id: str\n    :param retry: (Optional) A retry object used to retry requests.\n        If None is specified, requests will not be retried.\n    :type retry: google.api_core.retry.Retry\n    :param timeout: (Optional) The amount of time, in seconds, to wait for the request\n        to complete. Note that if retry is specified, the timeout applies to each\n        individual attempt.\n    :type timeout: float\n    :param metadata: (Optional) Additional metadata that is provided to the method.\n    :type metadata: sequence[tuple[str, str]]]\n    :param gcp_conn_id: (Optional) The connection ID used to connect to Google Cloud Platform.\n    :type gcp_conn_id: str\n    :rtype: google.cloud.dlp_v2.types.JobTrigger\n    '
    template_fields = ('job_trigger_id', 'project_id', 'gcp_conn_id')

    @apply_defaults
    def __init__(self, job_trigger_id, project_id=None, retry=None, timeout=None, metadata=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(CloudDLPGetJobTripperOperator, self).__init__)(*args, **kwargs)
        self.job_trigger_id = job_trigger_id
        self.project_id = project_id
        self.retry = retry
        self.timeout = timeout
        self.metadata = metadata
        self.gcp_conn_id = gcp_conn_id

    def execute(self, context):
        hook = CloudDLPHook(gcp_conn_id=(self.gcp_conn_id))
        return hook.get_job_trigger(job_trigger_id=(self.job_trigger_id),
          project_id=(self.project_id),
          retry=(self.retry),
          timeout=(self.timeout),
          metadata=(self.metadata))


class CloudDLPGetStoredInfoTypeOperator(BaseOperator):
    __doc__ = '\n    Gets a stored infoType.\n\n    :param stored_info_type_id: The ID of the stored info type to be read.\n    :type stored_info_type_id: str\n    :param organization_id: (Optional) The organization ID. Required to set this\n        field if parent resource is an organzation.\n    :type organization_id: str\n    :param project_id: (Optional) Google Cloud Platform project ID where the\n        DLP Instance exists. Only set this field if the parent resource is\n        a project instead of an organzation.\n    :type project_id: str\n    :param retry: (Optional) A retry object used to retry requests.\n        If None is specified, requests will not be retried.\n    :type retry: google.api_core.retry.Retry\n    :param timeout: (Optional) The amount of time, in seconds, to wait for the request\n        to complete. Note that if retry is specified, the timeout applies to each\n        individual attempt.\n    :type timeout: float\n    :param metadata: (Optional) Additional metadata that is provided to the method.\n    :type metadata: sequence[tuple[str, str]]]\n    :param gcp_conn_id: (Optional) The connection ID used to connect to Google Cloud Platform.\n    :type gcp_conn_id: str\n    :rtype: google.cloud.dlp_v2.types.StoredInfoType\n    '
    template_fields = ('stored_info_type_id', 'organization_id', 'project_id', 'gcp_conn_id')

    @apply_defaults
    def __init__(self, stored_info_type_id, organization_id=None, project_id=None, retry=None, timeout=None, metadata=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(CloudDLPGetStoredInfoTypeOperator, self).__init__)(*args, **kwargs)
        self.stored_info_type_id = stored_info_type_id
        self.organization_id = organization_id
        self.project_id = project_id
        self.retry = retry
        self.timeout = timeout
        self.metadata = metadata
        self.gcp_conn_id = gcp_conn_id

    def execute(self, context):
        hook = CloudDLPHook(gcp_conn_id=(self.gcp_conn_id))
        return hook.get_stored_info_type(stored_info_type_id=(self.stored_info_type_id),
          organization_id=(self.organization_id),
          project_id=(self.project_id),
          retry=(self.retry),
          timeout=(self.timeout),
          metadata=(self.metadata))


class CloudDLPInspectContentOperator(BaseOperator):
    __doc__ = '\n    Finds potentially sensitive info in content. This method has limits on\n    input size, processing time, and output size.\n\n    :param project_id: (Optional) Google Cloud Platform project ID where the\n        DLP Instance exists. If set to None or missing, the default\n        project_id from the GCP connection is used.\n    :type project_id: str\n    :param inspect_config: (Optional) Configuration for the inspector. Items specified\n        here will override the template referenced by the inspect_template_name argument.\n    :type inspect_config: dict or google.cloud.dlp_v2.types.InspectConfig\n    :param item: (Optional) The item to de-identify. Will be treated as text.\n    :type item: dict or google.cloud.dlp_v2.types.ContentItem\n    :param inspect_template_name: (Optional) Optional template to use. Any configuration\n        directly specified in inspect_config will override those set in the template.\n    :type inspect_template_name: str\n    :param retry: (Optional) A retry object used to retry requests.\n        If None is specified, requests will not be retried.\n    :type retry: google.api_core.retry.Retry\n    :param timeout: (Optional) The amount of time, in seconds, to wait for the request\n        to complete. Note that if retry is specified, the timeout applies to each\n        individual attempt.\n    :type timeout: float\n    :param metadata: (Optional) Additional metadata that is provided to the method.\n    :type metadata: sequence[tuple[str, str]]]\n    :param gcp_conn_id: (Optional) The connection ID used to connect to Google Cloud Platform.\n    :type gcp_conn_id: str\n    :rtype: google.cloud.tasks_v2.types.InspectContentResponse\n    '
    template_fields = ('project_id', 'inspect_config', 'item', 'inspect_template_name',
                       'gcp_conn_id')

    @apply_defaults
    def __init__(self, project_id=None, inspect_config=None, item=None, inspect_template_name=None, retry=None, timeout=None, metadata=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(CloudDLPInspectContentOperator, self).__init__)(*args, **kwargs)
        self.project_id = project_id
        self.inspect_config = inspect_config
        self.item = item
        self.inspect_template_name = inspect_template_name
        self.retry = retry
        self.timeout = timeout
        self.metadata = metadata
        self.gcp_conn_id = gcp_conn_id

    def execute(self, context):
        hook = CloudDLPHook(gcp_conn_id=(self.gcp_conn_id))
        return hook.inspect_content(project_id=(self.project_id),
          inspect_config=(self.inspect_config),
          item=(self.item),
          inspect_template_name=(self.inspect_template_name),
          retry=(self.retry),
          timeout=(self.timeout),
          metadata=(self.metadata))


class CloudDLPListDeidentifyTemplatesOperator(BaseOperator):
    __doc__ = '\n    Lists DeidentifyTemplates.\n\n    :param organization_id: (Optional) The organization ID. Required to set this\n        field if parent resource is an organzation.\n    :type organization_id: str\n    :param project_id: (Optional) Google Cloud Platform project ID where the\n        DLP Instance exists. Only set this field if the parent resource is\n        a project instead of an organzation.\n    :type project_id: str\n    :param page_size: (Optional) The maximum number of resources contained in the\n        underlying API response.\n    :type page_size: int\n    :param order_by: (Optional) Optional comma separated list of fields to order by,\n        followed by asc or desc postfix.\n    :type order_by: str\n    :param retry: (Optional) A retry object used to retry requests.\n        If None is specified, requests will not be retried.\n    :type retry: google.api_core.retry.Retry\n    :param timeout: (Optional) The amount of time, in seconds, to wait for the request\n        to complete. Note that if retry is specified, the timeout applies to each\n        individual attempt.\n    :type timeout: float\n    :param metadata: (Optional) Additional metadata that is provided to the method.\n    :type metadata: sequence[tuple[str, str]]]\n    :param gcp_conn_id: (Optional) The connection ID used to connect to Google Cloud Platform.\n    :type gcp_conn_id: str\n    :rtype: list[google.cloud.dlp_v2.types.DeidentifyTemplate]\n    '
    template_fields = ('organization_id', 'project_id', 'gcp_conn_id')

    @apply_defaults
    def __init__(self, organization_id=None, project_id=None, page_size=None, order_by=None, retry=None, timeout=None, metadata=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(CloudDLPListDeidentifyTemplatesOperator, self).__init__)(*args, **kwargs)
        self.organization_id = organization_id
        self.project_id = project_id
        self.page_size = page_size
        self.order_by = order_by
        self.retry = retry
        self.timeout = timeout
        self.metadata = metadata
        self.gcp_conn_id = gcp_conn_id

    def execute(self, context):
        hook = CloudDLPHook(gcp_conn_id=(self.gcp_conn_id))
        return hook.list_deidentify_templates(organization_id=(self.organization_id),
          project_id=(self.project_id),
          page_size=(self.page_size),
          order_by=(self.order_by),
          retry=(self.retry),
          timeout=(self.timeout),
          metadata=(self.metadata))


class CloudDLPListDlpJobsOperator(BaseOperator):
    __doc__ = '\n    Lists DlpJobs that match the specified filter in the request.\n\n    :param project_id: (Optional) Google Cloud Platform project ID where the\n        DLP Instance exists. If set to None or missing, the default\n        project_id from the GCP connection is used.\n    :type project_id: str\n    :param results_filter: (Optional) Filter used to specify a subset of results.\n    :type results_filter: str\n    :param page_size: (Optional) The maximum number of resources contained in the\n        underlying API response.\n    :type page_size: int\n    :param job_type: (Optional) The type of job.\n    :type job_type: str\n    :param order_by: (Optional) Optional comma separated list of fields to order by,\n        followed by asc or desc postfix.\n    :type order_by: str\n    :param retry: (Optional) A retry object used to retry requests.\n        If None is specified, requests will not be retried.\n    :type retry: google.api_core.retry.Retry\n    :param timeout: (Optional) The amount of time, in seconds, to wait for the request\n        to complete. Note that if retry is specified, the timeout applies to each\n        individual attempt.\n    :type timeout: float\n    :param metadata: (Optional) Additional metadata that is provided to the method.\n    :type metadata: sequence[tuple[str, str]]]\n    :param gcp_conn_id: (Optional) The connection ID used to connect to Google Cloud Platform.\n    :type gcp_conn_id: str\n    :rtype: list[google.cloud.dlp_v2.types.DlpJob]\n    '
    template_fields = ('project_id', 'gcp_conn_id')

    @apply_defaults
    def __init__(self, project_id=None, results_filter=None, page_size=None, job_type=None, order_by=None, retry=None, timeout=None, metadata=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(CloudDLPListDlpJobsOperator, self).__init__)(*args, **kwargs)
        self.project_id = project_id
        self.results_filter = results_filter
        self.page_size = page_size
        self.job_type = job_type
        self.order_by = order_by
        self.retry = retry
        self.timeout = timeout
        self.metadata = metadata
        self.gcp_conn_id = gcp_conn_id

    def execute(self, context):
        hook = CloudDLPHook(gcp_conn_id=(self.gcp_conn_id))
        return hook.list_dlp_jobs(project_id=(self.project_id),
          results_filter=(self.results_filter),
          page_size=(self.page_size),
          job_type=(self.job_type),
          order_by=(self.order_by),
          retry=(self.retry),
          timeout=(self.timeout),
          metadata=(self.metadata))


class CloudDLPListInfoTypesOperator(BaseOperator):
    __doc__ = '\n    Returns a list of the sensitive information types that the DLP API supports.\n\n    :param language_code: (Optional) Optional BCP-47 language code for localized infoType\n        friendly names. If omitted, or if localized strings are not available, en-US\n        strings will be returned.\n    :type language_code: str\n    :param results_filter: (Optional) Filter used to specify a subset of results.\n    :type results_filter: str\n    :param retry: (Optional) A retry object used to retry requests.\n        If None is specified, requests will not be retried.\n    :type retry: google.api_core.retry.Retry\n    :param timeout: (Optional) The amount of time, in seconds, to wait for the request\n        to complete. Note that if retry is specified, the timeout applies to each\n        individual attempt.\n    :type timeout: float\n    :param metadata: (Optional) Additional metadata that is provided to the method.\n    :type metadata: sequence[tuple[str, str]]]\n    :param gcp_conn_id: (Optional) The connection ID used to connect to Google Cloud Platform.\n    :type gcp_conn_id: str\n    :rtype: ListInfoTypesResponse\n    '
    template_fields = ('language_code', 'gcp_conn_id')

    @apply_defaults
    def __init__(self, language_code=None, results_filter=None, retry=None, timeout=None, metadata=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(CloudDLPListInfoTypesOperator, self).__init__)(*args, **kwargs)
        self.language_code = language_code
        self.results_filter = results_filter
        self.retry = retry
        self.timeout = timeout
        self.metadata = metadata
        self.gcp_conn_id = gcp_conn_id

    def execute(self, context):
        hook = CloudDLPHook(gcp_conn_id=(self.gcp_conn_id))
        return hook.list_info_types(language_code=(self.language_code),
          results_filter=(self.results_filter),
          retry=(self.retry),
          timeout=(self.timeout),
          metadata=(self.metadata))


class CloudDLPListInspectTemplatesOperator(BaseOperator):
    __doc__ = '\n    Lists InspectTemplates.\n\n    :param organization_id: (Optional) The organization ID. Required to set this\n        field if parent resource is an organzation.\n    :type organization_id: str\n    :param project_id: (Optional) Google Cloud Platform project ID where the\n        DLP Instance exists. Only set this field if the parent resource is\n        a project instead of an organzation.\n    :type project_id: str\n    :param page_size: (Optional) The maximum number of resources contained in the\n        underlying API response.\n    :type page_size: int\n    :param order_by: (Optional) Optional comma separated list of fields to order by,\n        followed by asc or desc postfix.\n    :type order_by: str\n    :param retry: (Optional) A retry object used to retry requests.\n        If None is specified, requests will not be retried.\n    :type retry: google.api_core.retry.Retry\n    :param timeout: (Optional) The amount of time, in seconds, to wait for the request\n        to complete. Note that if retry is specified, the timeout applies to each\n        individual attempt.\n    :type timeout: float\n    :param metadata: (Optional) Additional metadata that is provided to the method.\n    :type metadata: sequence[tuple[str, str]]]\n    :param gcp_conn_id: (Optional) The connection ID used to connect to Google Cloud Platform.\n    :type gcp_conn_id: str\n    :rtype: list[google.cloud.dlp_v2.types.InspectTemplate]\n    '
    template_fields = ('organization_id', 'project_id', 'gcp_conn_id')

    @apply_defaults
    def __init__(self, organization_id=None, project_id=None, page_size=None, order_by=None, retry=None, timeout=None, metadata=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(CloudDLPListInspectTemplatesOperator, self).__init__)(*args, **kwargs)
        self.organization_id = organization_id
        self.project_id = project_id
        self.page_size = page_size
        self.order_by = order_by
        self.retry = retry
        self.timeout = timeout
        self.metadata = metadata
        self.gcp_conn_id = gcp_conn_id

    def execute(self, context):
        hook = CloudDLPHook(gcp_conn_id=(self.gcp_conn_id))
        return hook.list_inspect_templates(organization_id=(self.organization_id),
          project_id=(self.project_id),
          page_size=(self.page_size),
          order_by=(self.order_by),
          retry=(self.retry),
          timeout=(self.timeout),
          metadata=(self.metadata))


class CloudDLPListJobTriggersOperator(BaseOperator):
    __doc__ = '\n    Lists job triggers.\n\n    :param project_id: (Optional) Google Cloud Platform project ID where the\n        DLP Instance exists. If set to None or missing, the default\n        project_id from the GCP connection is used.\n    :type project_id: str\n    :param page_size: (Optional) The maximum number of resources contained in the\n        underlying API response.\n    :type page_size: int\n    :param order_by: (Optional) Optional comma separated list of fields to order by,\n        followed by asc or desc postfix.\n    :type order_by: str\n    :param results_filter: (Optional) Filter used to specify a subset of results.\n    :type results_filter: str\n    :param retry: (Optional) A retry object used to retry requests.\n        If None is specified, requests will not be retried.\n    :type retry: google.api_core.retry.Retry\n    :param timeout: (Optional) The amount of time, in seconds, to wait for the request\n        to complete. Note that if retry is specified, the timeout applies to each\n        individual attempt.\n    :type timeout: float\n    :param metadata: (Optional) Additional metadata that is provided to the method.\n    :type metadata: sequence[tuple[str, str]]]\n    :param gcp_conn_id: (Optional) The connection ID used to connect to Google Cloud Platform.\n    :type gcp_conn_id: str\n    :rtype: list[google.cloud.dlp_v2.types.JobTrigger]\n    '
    template_fields = ('project_id', 'gcp_conn_id')

    @apply_defaults
    def __init__(self, project_id=None, page_size=None, order_by=None, results_filter=None, retry=None, timeout=None, metadata=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(CloudDLPListJobTriggersOperator, self).__init__)(*args, **kwargs)
        self.project_id = project_id
        self.page_size = page_size
        self.order_by = order_by
        self.results_filter = results_filter
        self.retry = retry
        self.timeout = timeout
        self.metadata = metadata
        self.gcp_conn_id = gcp_conn_id

    def execute(self, context):
        hook = CloudDLPHook(gcp_conn_id=(self.gcp_conn_id))
        return hook.list_job_triggers(project_id=(self.project_id),
          page_size=(self.page_size),
          order_by=(self.order_by),
          results_filter=(self.results_filter),
          retry=(self.retry),
          timeout=(self.timeout),
          metadata=(self.metadata))


class CloudDLPListStoredInfoTypesOperator(BaseOperator):
    __doc__ = '\n    Lists stored infoTypes.\n\n    :param organization_id: (Optional) The organization ID. Required to set this\n        field if parent resource is an organzation.\n    :type organization_id: str\n    :param project_id: (Optional) Google Cloud Platform project ID where the\n        DLP Instance exists. Only set this field if the parent resource is\n        a project instead of an organzation.\n    :type project_id: str\n    :param page_size: (Optional) The maximum number of resources contained in the\n        underlying API response.\n    :type page_size: int\n    :param order_by: (Optional) Optional comma separated list of fields to order by,\n        followed by asc or desc postfix.\n    :type order_by: str\n    :param retry: (Optional) A retry object used to retry requests.\n        If None is specified, requests will not be retried.\n    :type retry: google.api_core.retry.Retry\n    :param timeout: (Optional) The amount of time, in seconds, to wait for the request\n        to complete. Note that if retry is specified, the timeout applies to each\n        individual attempt.\n    :type timeout: float\n    :param metadata: (Optional) Additional metadata that is provided to the method.\n    :type metadata: sequence[tuple[str, str]]]\n    :param gcp_conn_id: (Optional) The connection ID used to connect to Google Cloud Platform.\n    :type gcp_conn_id: str\n    :rtype: list[google.cloud.dlp_v2.types.StoredInfoType]\n    '
    template_fields = ('organization_id', 'project_id', 'gcp_conn_id')

    @apply_defaults
    def __init__(self, organization_id=None, project_id=None, page_size=None, order_by=None, retry=None, timeout=None, metadata=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(CloudDLPListStoredInfoTypesOperator, self).__init__)(*args, **kwargs)
        self.organization_id = organization_id
        self.project_id = project_id
        self.page_size = page_size
        self.order_by = order_by
        self.retry = retry
        self.timeout = timeout
        self.metadata = metadata
        self.gcp_conn_id = gcp_conn_id

    def execute(self, context):
        hook = CloudDLPHook(gcp_conn_id=(self.gcp_conn_id))
        return hook.list_stored_info_types(organization_id=(self.organization_id),
          project_id=(self.project_id),
          page_size=(self.page_size),
          order_by=(self.order_by),
          retry=(self.retry),
          timeout=(self.timeout),
          metadata=(self.metadata))


class CloudDLPRedactImageOperator(BaseOperator):
    __doc__ = '\n    Redacts potentially sensitive info from an image. This method has limits on\n    input size, processing time, and output size.\n\n    :param project_id: (Optional) Google Cloud Platform project ID where the\n        DLP Instance exists. If set to None or missing, the default\n        project_id from the GCP connection is used.\n    :type project_id: str\n    :param inspect_config: (Optional) Configuration for the inspector. Items specified\n        here will override the template referenced by the inspect_template_name argument.\n    :type inspect_config: dict or google.cloud.dlp_v2.types.InspectConfig\n    :param image_redaction_configs: (Optional) The configuration for specifying what\n        content to redact from images.\n    :type image_redaction_configs: list[dict] or list[google.cloud.dlp_v2.types.ImageRedactionConfig]\n    :param include_findings: (Optional) Whether the response should include findings\n        along with the redacted image.\n    :type include_findings: bool\n    :param byte_item: (Optional) The content must be PNG, JPEG, SVG or BMP.\n    :type byte_item: dict or google.cloud.dlp_v2.types.ByteContentItem\n    :param retry: (Optional) A retry object used to retry requests.\n        If None is specified, requests will not be retried.\n    :type retry: google.api_core.retry.Retry\n    :param timeout: (Optional) The amount of time, in seconds, to wait for the request\n        to complete. Note that if retry is specified, the timeout applies to each\n        individual attempt.\n    :type timeout: float\n    :param metadata: (Optional) Additional metadata that is provided to the method.\n    :type metadata: sequence[tuple[str, str]]]\n    :param gcp_conn_id: (Optional) The connection ID used to connect to Google Cloud Platform.\n    :type gcp_conn_id: str\n    :rtype: google.cloud.dlp_v2.types.RedactImageResponse\n    '
    template_fields = ('project_id', 'inspect_config', 'image_redaction_configs', 'include_findings',
                       'byte_item', 'gcp_conn_id')

    @apply_defaults
    def __init__(self, project_id=None, inspect_config=None, image_redaction_configs=None, include_findings=None, byte_item=None, retry=None, timeout=None, metadata=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(CloudDLPRedactImageOperator, self).__init__)(*args, **kwargs)
        self.project_id = project_id
        self.inspect_config = inspect_config
        self.image_redaction_configs = image_redaction_configs
        self.include_findings = include_findings
        self.byte_item = byte_item
        self.retry = retry
        self.timeout = timeout
        self.metadata = metadata
        self.gcp_conn_id = gcp_conn_id

    def execute(self, context):
        hook = CloudDLPHook(gcp_conn_id=(self.gcp_conn_id))
        return hook.redact_image(project_id=(self.project_id),
          inspect_config=(self.inspect_config),
          image_redaction_configs=(self.image_redaction_configs),
          include_findings=(self.include_findings),
          byte_item=(self.byte_item),
          retry=(self.retry),
          timeout=(self.timeout),
          metadata=(self.metadata))


class CloudDLPReidentifyContentOperator(BaseOperator):
    __doc__ = '\n    Re-identifies content that has been de-identified.\n\n    :param project_id: (Optional) Google Cloud Platform project ID where the\n        DLP Instance exists. If set to None or missing, the default\n        project_id from the GCP connection is used.\n    :type project_id: str\n    :param reidentify_config: (Optional) Configuration for the re-identification of\n        the content item.\n    :type reidentify_config: dict or google.cloud.dlp_v2.types.DeidentifyConfig\n    :param inspect_config: (Optional) Configuration for the inspector.\n    :type inspect_config: dict or google.cloud.dlp_v2.types.InspectConfig\n    :param item: (Optional) The item to re-identify. Will be treated as text.\n    :type item: dict or google.cloud.dlp_v2.types.ContentItem\n    :param inspect_template_name: (Optional) Optional template to use. Any configuration\n        directly specified in inspect_config will override those set in the template.\n    :type inspect_template_name: str\n    :param reidentify_template_name: (Optional) Optional template to use. References an\n        instance of DeidentifyTemplate. Any configuration directly specified in\n        reidentify_config or inspect_config will override those set in the template.\n    :type reidentify_template_name: str\n    :param retry: (Optional) A retry object used to retry requests.\n        If None is specified, requests will not be retried.\n    :type retry: google.api_core.retry.Retry\n    :param timeout: (Optional) The amount of time, in seconds, to wait for the request\n        to complete. Note that if retry is specified, the timeout applies to each\n        individual attempt.\n    :type timeout: float\n    :param metadata: (Optional) Additional metadata that is provided to the method.\n    :type metadata: sequence[tuple[str, str]]]\n    :param gcp_conn_id: (Optional) The connection ID used to connect to Google Cloud Platform.\n    :type gcp_conn_id: str\n    :rtype: google.cloud.dlp_v2.types.ReidentifyContentResponse\n    '
    template_fields = ('project_id', 'reidentify_config', 'inspect_config', 'item',
                       'inspect_template_name', 'reidentify_template_name', 'gcp_conn_id')

    @apply_defaults
    def __init__(self, project_id=None, reidentify_config=None, inspect_config=None, item=None, inspect_template_name=None, reidentify_template_name=None, retry=None, timeout=None, metadata=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(CloudDLPReidentifyContentOperator, self).__init__)(*args, **kwargs)
        self.project_id = project_id
        self.reidentify_config = reidentify_config
        self.inspect_config = inspect_config
        self.item = item
        self.inspect_template_name = inspect_template_name
        self.reidentify_template_name = reidentify_template_name
        self.retry = retry
        self.timeout = timeout
        self.metadata = metadata
        self.gcp_conn_id = gcp_conn_id

    def execute(self, context):
        hook = CloudDLPHook(gcp_conn_id=(self.gcp_conn_id))
        return hook.reidentify_content(project_id=(self.project_id),
          reidentify_config=(self.reidentify_config),
          inspect_config=(self.inspect_config),
          item=(self.item),
          inspect_template_name=(self.inspect_template_name),
          reidentify_template_name=(self.reidentify_template_name),
          retry=(self.retry),
          timeout=(self.timeout),
          metadata=(self.metadata))


class CloudDLPUpdateDeidentifyTemplateOperator(BaseOperator):
    __doc__ = '\n    Updates the DeidentifyTemplate.\n\n    :param template_id: The ID of deidentify template to be updated.\n    :type template_id: str\n    :param organization_id: (Optional) The organization ID. Required to set this\n        field if parent resource is an organzation.\n    :type organization_id: str\n    :param project_id: (Optional) Google Cloud Platform project ID where the\n        DLP Instance exists. Only set this field if the parent resource is\n        a project instead of an organzation.\n    :type project_id: str\n    :param deidentify_template: New DeidentifyTemplate value.\n    :type deidentify_template: dict or google.cloud.dlp_v2.types.DeidentifyTemplate\n    :param update_mask: Mask to control which fields get updated.\n    :type update_mask: dict or google.cloud.dlp_v2.types.FieldMask\n    :param retry: (Optional) A retry object used to retry requests.\n        If None is specified, requests will not be retried.\n    :type retry: google.api_core.retry.Retry\n    :param timeout: (Optional) The amount of time, in seconds, to wait for the request\n        to complete. Note that if retry is specified, the timeout applies to each\n        individual attempt.\n    :type timeout: float\n    :param metadata: (Optional) Additional metadata that is provided to the method.\n    :type metadata: sequence[tuple[str, str]]]\n    :param gcp_conn_id: (Optional) The connection ID used to connect to Google Cloud Platform.\n    :type gcp_conn_id: str\n    :rtype: google.cloud.dlp_v2.types.DeidentifyTemplate\n    '
    template_fields = ('template_id', 'organization_id', 'project_id', 'deidentify_template',
                       'update_mask', 'gcp_conn_id')

    @apply_defaults
    def __init__(self, template_id, organization_id=None, project_id=None, deidentify_template=None, update_mask=None, retry=None, timeout=None, metadata=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(CloudDLPUpdateDeidentifyTemplateOperator, self).__init__)(*args, **kwargs)
        self.template_id = template_id
        self.organization_id = organization_id
        self.project_id = project_id
        self.deidentify_template = deidentify_template
        self.update_mask = update_mask
        self.retry = retry
        self.timeout = timeout
        self.metadata = metadata
        self.gcp_conn_id = gcp_conn_id

    def execute(self, context):
        hook = CloudDLPHook(gcp_conn_id=(self.gcp_conn_id))
        return hook.update_deidentify_template(template_id=(self.template_id),
          organization_id=(self.organization_id),
          project_id=(self.project_id),
          deidentify_template=(self.deidentify_template),
          update_mask=(self.update_mask),
          retry=(self.retry),
          timeout=(self.timeout),
          metadata=(self.metadata))


class CloudDLPUpdateInspectTemplateOperator(BaseOperator):
    __doc__ = '\n    Updates the InspectTemplate.\n\n    :param template_id: The ID of the inspect template to be updated.\n    :type template_id: str\n    :param organization_id: (Optional) The organization ID. Required to set this\n        field if parent resource is an organzation.\n    :type organization_id: str\n    :param project_id: (Optional) Google Cloud Platform project ID where the\n        DLP Instance exists. Only set this field if the parent resource is\n        a project instead of an organzation.\n    :type project_id: str\n    :param inspect_template: New InspectTemplate value.\n    :type inspect_template: dict or google.cloud.dlp_v2.types.InspectTemplate\n    :param update_mask: Mask to control which fields get updated.\n    :type update_mask: dict or google.cloud.dlp_v2.types.FieldMask\n    :param retry: (Optional) A retry object used to retry requests.\n        If None is specified, requests will not be retried.\n    :type retry: google.api_core.retry.Retry\n    :param timeout: (Optional) The amount of time, in seconds, to wait for the request\n        to complete. Note that if retry is specified, the timeout applies to each\n        individual attempt.\n    :type timeout: float\n    :param metadata: (Optional) Additional metadata that is provided to the method.\n    :type metadata: sequence[tuple[str, str]]]\n    :param gcp_conn_id: (Optional) The connection ID used to connect to Google Cloud Platform.\n    :type gcp_conn_id: str\n    :rtype: google.cloud.dlp_v2.types.InspectTemplate\n    '
    template_fields = ('template_id', 'organization_id', 'project_id', 'inspect_template',
                       'update_mask', 'gcp_conn_id')

    @apply_defaults
    def __init__(self, template_id, organization_id=None, project_id=None, inspect_template=None, update_mask=None, retry=None, timeout=None, metadata=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(CloudDLPUpdateInspectTemplateOperator, self).__init__)(*args, **kwargs)
        self.template_id = template_id
        self.organization_id = organization_id
        self.project_id = project_id
        self.inspect_template = inspect_template
        self.update_mask = update_mask
        self.retry = retry
        self.timeout = timeout
        self.metadata = metadata
        self.gcp_conn_id = gcp_conn_id

    def execute(self, context):
        hook = CloudDLPHook(gcp_conn_id=(self.gcp_conn_id))
        return hook.update_inspect_template(template_id=(self.template_id),
          organization_id=(self.organization_id),
          project_id=(self.project_id),
          inspect_template=(self.inspect_template),
          update_mask=(self.update_mask),
          retry=(self.retry),
          timeout=(self.timeout),
          metadata=(self.metadata))


class CloudDLPUpdateJobTriggerOperator(BaseOperator):
    __doc__ = '\n    Updates a job trigger.\n\n    :param job_trigger_id: The ID of the DLP job trigger to be updated.\n    :type job_trigger_id: str\n    :param project_id: (Optional) Google Cloud Platform project ID where the\n        DLP Instance exists. If set to None or missing, the default\n        project_id from the GCP connection is used.\n    :type project_id: str\n    :param job_trigger: New JobTrigger value.\n    :type job_trigger: dict or google.cloud.dlp_v2.types.JobTrigger\n    :param update_mask: Mask to control which fields get updated.\n    :type update_mask: dict or google.cloud.dlp_v2.types.FieldMask\n    :param retry: (Optional) A retry object used to retry requests.\n        If None is specified, requests will not be retried.\n    :type retry: google.api_core.retry.Retry\n    :param timeout: (Optional) The amount of time, in seconds, to wait for the request\n        to complete. Note that if retry is specified, the timeout applies to each\n        individual attempt.\n    :type timeout: float\n    :param metadata: (Optional) Additional metadata that is provided to the method.\n    :type metadata: sequence[tuple[str, str]]]\n    :param gcp_conn_id: (Optional) The connection ID used to connect to Google Cloud Platform.\n    :type gcp_conn_id: str\n    :rtype: google.cloud.dlp_v2.types.InspectTemplate\n    '
    template_fields = ('job_trigger_id', 'project_id', 'job_trigger', 'update_mask',
                       'gcp_conn_id')

    @apply_defaults
    def __init__(self, job_trigger_id, project_id=None, job_trigger=None, update_mask=None, retry=None, timeout=None, metadata=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(CloudDLPUpdateJobTriggerOperator, self).__init__)(*args, **kwargs)
        self.job_trigger_id = job_trigger_id
        self.project_id = project_id
        self.job_trigger = job_trigger
        self.update_mask = update_mask
        self.retry = retry
        self.timeout = timeout
        self.metadata = metadata
        self.gcp_conn_id = gcp_conn_id

    def execute(self, context):
        hook = CloudDLPHook(gcp_conn_id=(self.gcp_conn_id))
        return hook.update_job_trigger(job_trigger_id=(self.job_trigger_id),
          project_id=(self.project_id),
          job_trigger=(self.job_trigger),
          update_mask=(self.update_mask),
          retry=(self.retry),
          timeout=(self.timeout),
          metadata=(self.metadata))


class CloudDLPUpdateStoredInfoTypeOperator(BaseOperator):
    __doc__ = '\n    Updates the stored infoType by creating a new version.\n\n    :param stored_info_type_id: The ID of the stored info type to be updated.\n    :type stored_info_type_id: str\n    :param organization_id: (Optional) The organization ID. Required to set this\n        field if parent resource is an organisation.\n    :type organization_id: str\n    :param project_id: (Optional) Google Cloud Platform project ID where the\n        DLP Instance exists. Only set this field if the parent resource is\n        a project instead of an organisation.\n    :type project_id: str\n    :param config: Updated configuration for the storedInfoType. If not provided, a new\n        version of the storedInfoType will be created with the existing configuration.\n    :type config: dict or google.cloud.dlp_v2.types.StoredInfoTypeConfig\n    :param update_mask: Mask to control which fields get updated.\n    :type update_mask: dict or google.cloud.dlp_v2.types.FieldMask\n    :param retry: (Optional) A retry object used to retry requests.\n        If None is specified, requests will not be retried.\n    :type retry: google.api_core.retry.Retry\n    :param timeout: (Optional) The amount of time, in seconds, to wait for the request\n        to complete. Note that if retry is specified, the timeout applies to each\n        individual attempt.\n    :type timeout: float\n    :param metadata: (Optional) Additional metadata that is provided to the method.\n    :type metadata: sequence[tuple[str, str]]]\n    :param gcp_conn_id: (Optional) The connection ID used to connect to Google Cloud Platform.\n    :type gcp_conn_id: str\n    :rtype: google.cloud.dlp_v2.types.StoredInfoType\n    '
    template_fields = ('stored_info_type_id', 'organization_id', 'project_id', 'config',
                       'update_mask', 'gcp_conn_id')

    @apply_defaults
    def __init__(self, stored_info_type_id, organization_id=None, project_id=None, config=None, update_mask=None, retry=None, timeout=None, metadata=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(CloudDLPUpdateStoredInfoTypeOperator, self).__init__)(*args, **kwargs)
        self.stored_info_type_id = stored_info_type_id
        self.organization_id = organization_id
        self.project_id = project_id
        self.config = config
        self.update_mask = update_mask
        self.retry = retry
        self.timeout = timeout
        self.metadata = metadata
        self.gcp_conn_id = gcp_conn_id

    def execute(self, context):
        hook = CloudDLPHook(gcp_conn_id=(self.gcp_conn_id))
        return hook.update_stored_info_type(stored_info_type_id=(self.stored_info_type_id),
          organization_id=(self.organization_id),
          project_id=(self.project_id),
          config=(self.config),
          update_mask=(self.update_mask),
          retry=(self.retry),
          timeout=(self.timeout),
          metadata=(self.metadata))