# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/gcp_dlp_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 80088 bytes
__doc__ = '\nThis module contains various GCP Cloud DLP operators\nwhich allow you to perform basic operations using\nCloud DLP.\n'
from airflow.contrib.hooks.gcp_dlp_hook import CloudDLPHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class CloudDLPCancelDLPJobOperator(BaseOperator):
    """CloudDLPCancelDLPJobOperator"""
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
    """CloudDLPCreateDeidentifyTemplateOperator"""
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
    """CloudDLPCreateDLPJobOperator"""
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
    """CloudDLPCreateInspectTemplateOperator"""
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
    """CloudDLPCreateJobTriggerOperator"""
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
    """CloudDLPCreateStoredInfoTypeOperator"""
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
    """CloudDLPDeidentifyContentOperator"""
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
    """CloudDLPDeleteDeidentifyTemplateOperator"""
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
    """CloudDLPDeleteDlpJobOperator"""
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
    """CloudDLPDeleteInspectTemplateOperator"""
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
    """CloudDLPDeleteJobTriggerOperator"""
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
    """CloudDLPDeleteStoredInfoTypeOperator"""
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
    """CloudDLPGetDeidentifyTemplateOperator"""
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
    """CloudDLPGetDlpJobOperator"""
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
    """CloudDLPGetInspectTemplateOperator"""
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
    """CloudDLPGetJobTripperOperator"""
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
    """CloudDLPGetStoredInfoTypeOperator"""
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
    """CloudDLPInspectContentOperator"""
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
    """CloudDLPListDeidentifyTemplatesOperator"""
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
    """CloudDLPListDlpJobsOperator"""
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
    """CloudDLPListInfoTypesOperator"""
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
    """CloudDLPListInspectTemplatesOperator"""
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
    """CloudDLPListJobTriggersOperator"""
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
    """CloudDLPListStoredInfoTypesOperator"""
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
    """CloudDLPRedactImageOperator"""
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
    """CloudDLPReidentifyContentOperator"""
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
    """CloudDLPUpdateDeidentifyTemplateOperator"""
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
    """CloudDLPUpdateInspectTemplateOperator"""
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
    """CloudDLPUpdateJobTriggerOperator"""
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
    """CloudDLPUpdateStoredInfoTypeOperator"""
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