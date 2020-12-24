# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/dataproc_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 50223 bytes
"""
This module contains Google Dataproc operators.
"""
import ntpath, os, re, time, uuid
from datetime import timedelta
from airflow.contrib.hooks.gcp_dataproc_hook import DataProcHook
from airflow.contrib.hooks.gcs_hook import GoogleCloudStorageHook
from airflow.exceptions import AirflowException
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.version import version
from airflow.utils import timezone

class DataprocOperationBaseOperator(BaseOperator):
    __doc__ = 'The base class for operators that poll on a Dataproc Operation.'

    @apply_defaults
    def __init__(self, project_id, region='global', gcp_conn_id='google_cloud_default', delegate_to=None, *args, **kwargs):
        (super(DataprocOperationBaseOperator, self).__init__)(*args, **kwargs)
        self.gcp_conn_id = gcp_conn_id
        self.delegate_to = delegate_to
        self.project_id = project_id
        self.region = region
        self.hook = DataProcHook(gcp_conn_id=(self.gcp_conn_id),
          delegate_to=(self.delegate_to),
          api_version='v1beta2')

    def execute(self, context):
        self.hook.wait(self.start())

    def start(self, context):
        raise AirflowException('Please submit an operation')


class DataprocClusterCreateOperator(DataprocOperationBaseOperator):
    __doc__ = "\n    Create a new cluster on Google Cloud Dataproc. The operator will wait until the\n    creation is successful or an error occurs in the creation process.\n\n    The parameters allow to configure the cluster. Please refer to\n\n    https://cloud.google.com/dataproc/docs/reference/rest/v1/projects.regions.clusters\n\n    for a detailed explanation on the different parameters. Most of the configuration\n    parameters detailed in the link are available as a parameter to this operator.\n\n    :param cluster_name: The name of the DataProc cluster to create. (templated)\n    :type cluster_name: str\n    :param project_id: The ID of the google cloud project in which\n        to create the cluster. (templated)\n    :type project_id: str\n    :param num_workers: The # of workers to spin up. If set to zero will\n        spin up cluster in a single node mode\n    :type num_workers: int\n    :param storage_bucket: The storage bucket to use, setting to None lets dataproc\n        generate a custom one for you\n    :type storage_bucket: str\n    :param init_actions_uris: List of GCS uri's containing\n        dataproc initialization scripts\n    :type init_actions_uris: list[str]\n    :param init_action_timeout: Amount of time executable scripts in\n        init_actions_uris has to complete\n    :type init_action_timeout: str\n    :param metadata: dict of key-value google compute engine metadata entries\n        to add to all instances\n    :type metadata: dict\n    :param image_version: the version of software inside the Dataproc cluster\n    :type image_version: str\n    :param custom_image: custom Dataproc image for more info see\n        https://cloud.google.com/dataproc/docs/guides/dataproc-images\n    :type custom_image: str\n    :param autoscaling_policy: The autoscaling policy used by the cluster. Only resource names\n        including projectid and location (region) are valid. Example:\n        ``projects/[projectId]/locations/[dataproc_region]/autoscalingPolicies/[policy_id]``\n    :type autoscaling_policy: str\n    :param properties: dict of properties to set on\n        config files (e.g. spark-defaults.conf), see\n        https://cloud.google.com/dataproc/docs/reference/rest/v1/projects.regions.clusters#SoftwareConfig\n    :type properties: dict\n    :param num_masters: The # of master nodes to spin up\n    :type num_masters: int\n    :param master_machine_type: Compute engine machine type to use for the master node\n    :type master_machine_type: str\n    :param master_disk_type: Type of the boot disk for the master node\n        (default is ``pd-standard``).\n        Valid values: ``pd-ssd`` (Persistent Disk Solid State Drive) or\n        ``pd-standard`` (Persistent Disk Hard Disk Drive).\n    :type master_disk_type: str\n    :param master_disk_size: Disk size for the master node\n    :type master_disk_size: int\n    :param worker_machine_type: Compute engine machine type to use for the worker nodes\n    :type worker_machine_type: str\n    :param worker_disk_type: Type of the boot disk for the worker node\n        (default is ``pd-standard``).\n        Valid values: ``pd-ssd`` (Persistent Disk Solid State Drive) or\n        ``pd-standard`` (Persistent Disk Hard Disk Drive).\n    :type worker_disk_type: str\n    :param worker_disk_size: Disk size for the worker nodes\n    :type worker_disk_size: int\n    :param num_preemptible_workers: The # of preemptible worker nodes to spin up\n    :type num_preemptible_workers: int\n    :param labels: dict of labels to add to the cluster\n    :type labels: dict\n    :param zone: The zone where the cluster will be located. Set to None to auto-zone. (templated)\n    :type zone: str\n    :param network_uri: The network uri to be used for machine communication, cannot be\n        specified with subnetwork_uri\n    :type network_uri: str\n    :param subnetwork_uri: The subnetwork uri to be used for machine communication,\n        cannot be specified with network_uri\n    :type subnetwork_uri: str\n    :param internal_ip_only: If true, all instances in the cluster will only\n        have internal IP addresses. This can only be enabled for subnetwork\n        enabled networks\n    :type internal_ip_only: bool\n    :param tags: The GCE tags to add to all instances\n    :type tags: list[str]\n    :param region: leave as 'global', might become relevant in the future. (templated)\n    :type region: str\n    :param gcp_conn_id: The connection ID to use connecting to Google Cloud Platform.\n    :type gcp_conn_id: str\n    :param delegate_to: The account to impersonate, if any.\n        For this to work, the service account making the request must have domain-wide\n        delegation enabled.\n    :type delegate_to: str\n    :param service_account: The service account of the dataproc instances.\n    :type service_account: str\n    :param service_account_scopes: The URIs of service account scopes to be included.\n    :type service_account_scopes: list[str]\n    :param idle_delete_ttl: The longest duration that cluster would keep alive while\n        staying idle. Passing this threshold will cause cluster to be auto-deleted.\n        A duration in seconds.\n    :type idle_delete_ttl: int\n    :param auto_delete_time:  The time when cluster will be auto-deleted.\n    :type auto_delete_time: datetime.datetime\n    :param auto_delete_ttl: The life duration of cluster, the cluster will be\n        auto-deleted at the end of this duration.\n        A duration in seconds. (If auto_delete_time is set this parameter will be ignored)\n    :type auto_delete_ttl: int\n    :param customer_managed_key: The customer-managed key used for disk encryption\n        ``projects/[PROJECT_STORING_KEYS]/locations/[LOCATION]/keyRings/[KEY_RING_NAME]/cryptoKeys/[KEY_NAME]`` # noqa # pylint: disable=line-too-long\n    :type customer_managed_key: str\n    "
    template_fields = [
     'cluster_name', 'project_id', 'zone', 'region']

    @apply_defaults
    def __init__(self, project_id, cluster_name, num_workers, zone=None, network_uri=None, subnetwork_uri=None, internal_ip_only=None, tags=None, storage_bucket=None, init_actions_uris=None, init_action_timeout='10m', metadata=None, custom_image=None, image_version=None, autoscaling_policy=None, properties=None, num_masters=1, master_machine_type='n1-standard-4', master_disk_type='pd-standard', master_disk_size=500, worker_machine_type='n1-standard-4', worker_disk_type='pd-standard', worker_disk_size=500, num_preemptible_workers=0, labels=None, region='global', service_account=None, service_account_scopes=None, idle_delete_ttl=None, auto_delete_time=None, auto_delete_ttl=None, customer_managed_key=None, *args, **kwargs):
        (super(DataprocClusterCreateOperator, self).__init__)(args, project_id=project_id, region=region, **kwargs)
        self.cluster_name = cluster_name
        self.num_masters = num_masters
        self.num_workers = num_workers
        self.num_preemptible_workers = num_preemptible_workers
        self.storage_bucket = storage_bucket
        self.init_actions_uris = init_actions_uris
        self.init_action_timeout = init_action_timeout
        self.metadata = metadata
        self.custom_image = custom_image
        self.image_version = image_version
        self.properties = properties or dict()
        self.master_machine_type = master_machine_type
        self.master_disk_type = master_disk_type
        self.master_disk_size = master_disk_size
        self.autoscaling_policy = autoscaling_policy
        self.worker_machine_type = worker_machine_type
        self.worker_disk_type = worker_disk_type
        self.worker_disk_size = worker_disk_size
        self.labels = labels
        self.zone = zone
        self.network_uri = network_uri
        self.subnetwork_uri = subnetwork_uri
        self.internal_ip_only = internal_ip_only
        self.tags = tags
        self.service_account = service_account
        self.service_account_scopes = service_account_scopes
        self.idle_delete_ttl = idle_delete_ttl
        self.auto_delete_time = auto_delete_time
        self.auto_delete_ttl = auto_delete_ttl
        self.customer_managed_key = customer_managed_key
        self.single_node = num_workers == 0
        assert not (self.custom_image and self.image_version), "custom_image and image_version can't be both set"
        if not not self.single_node:
            if not (self.single_node and self.num_preemptible_workers == 0):
                raise AssertionError('num_workers == 0 means single node mode - no preemptibles allowed')

    def _get_init_action_timeout(self):
        match = re.match('^(\\d+)(s|m)$', self.init_action_timeout)
        if match:
            if match.group(2) == 's':
                return self.init_action_timeout
            if match.group(2) == 'm':
                val = float(match.group(1))
                return '{}s'.format(timedelta(minutes=val).seconds)
        raise AirflowException('DataprocClusterCreateOperator init_action_timeout should be expressed in minutes or seconds. i.e. 10m, 30s')

    def _build_gce_cluster_config(self, cluster_data):
        if self.zone:
            zone_uri = 'https://www.googleapis.com/compute/v1/projects/{}/zones/{}'.format(self.project_id, self.zone)
            cluster_data['config']['gceClusterConfig']['zoneUri'] = zone_uri
        else:
            if self.metadata:
                cluster_data['config']['gceClusterConfig']['metadata'] = self.metadata
            else:
                if self.network_uri:
                    cluster_data['config']['gceClusterConfig']['networkUri'] = self.network_uri
                else:
                    if self.subnetwork_uri:
                        cluster_data['config']['gceClusterConfig']['subnetworkUri'] = self.subnetwork_uri
                    if self.internal_ip_only:
                        if not self.subnetwork_uri:
                            raise AirflowException('Set internal_ip_only to true only when you pass a subnetwork_uri.')
                        cluster_data['config']['gceClusterConfig']['internalIpOnly'] = True
                    if self.tags:
                        cluster_data['config']['gceClusterConfig']['tags'] = self.tags
                if self.service_account:
                    cluster_data['config']['gceClusterConfig']['serviceAccount'] = self.service_account
            if self.service_account_scopes:
                cluster_data['config']['gceClusterConfig']['serviceAccountScopes'] = self.service_account_scopes
        return cluster_data

    def _build_lifecycle_config(self, cluster_data):
        if self.idle_delete_ttl:
            cluster_data['config']['lifecycleConfig']['idleDeleteTtl'] = '{}s'.format(self.idle_delete_ttl)
        if self.auto_delete_time:
            utc_auto_delete_time = timezone.convert_to_utc(self.auto_delete_time)
            cluster_data['config']['lifecycleConfig']['autoDeleteTime'] = utc_auto_delete_time.format('%Y-%m-%dT%H:%M:%S.%fZ', formatter='classic')
        else:
            if self.auto_delete_ttl:
                cluster_data['config']['lifecycleConfig']['autoDeleteTtl'] = '{}s'.format(self.auto_delete_ttl)
        return cluster_data

    def _build_cluster_data(self):
        if self.zone:
            master_type_uri = 'https://www.googleapis.com/compute/v1/projects/{}/zones/{}/machineTypes/{}'.format(self.project_id, self.zone, self.master_machine_type)
            worker_type_uri = 'https://www.googleapis.com/compute/v1/projects/{}/zones/{}/machineTypes/{}'.format(self.project_id, self.zone, self.worker_machine_type)
        else:
            master_type_uri = self.master_machine_type
            worker_type_uri = self.worker_machine_type
        cluster_data = {'projectId':self.project_id, 
         'clusterName':self.cluster_name, 
         'config':{'gceClusterConfig':{},  'masterConfig':{'numInstances':self.num_masters, 
           'machineTypeUri':master_type_uri, 
           'diskConfig':{'bootDiskType':self.master_disk_type, 
            'bootDiskSizeGb':self.master_disk_size}}, 
          'workerConfig':{'numInstances':self.num_workers, 
           'machineTypeUri':worker_type_uri, 
           'diskConfig':{'bootDiskType':self.worker_disk_type, 
            'bootDiskSizeGb':self.worker_disk_size}}, 
          'secondaryWorkerConfig':{},  'softwareConfig':{},  'lifecycleConfig':{},  'encryptionConfig':{},  'autoscalingConfig':{}}}
        if self.num_preemptible_workers > 0:
            cluster_data['config']['secondaryWorkerConfig'] = {'numInstances':self.num_preemptible_workers,  'machineTypeUri':worker_type_uri, 
             'diskConfig':{'bootDiskType':self.worker_disk_type, 
              'bootDiskSizeGb':self.worker_disk_size}, 
             'isPreemptible':True}
        cluster_data['labels'] = self.labels or {}
        cluster_data['labels'].update({'airflow-version': 'v' + version.replace('.', '-').replace('+', '-')})
        if self.storage_bucket:
            cluster_data['config']['configBucket'] = self.storage_bucket
        if self.image_version:
            cluster_data['config']['softwareConfig']['imageVersion'] = self.image_version
        else:
            if self.custom_image:
                custom_image_url = 'https://www.googleapis.com/compute/beta/projects/{}/global/images/{}'.format(self.project_id, self.custom_image)
                cluster_data['config']['masterConfig']['imageUri'] = custom_image_url
                if not self.single_node:
                    cluster_data['config']['workerConfig']['imageUri'] = custom_image_url
        cluster_data = self._build_gce_cluster_config(cluster_data)
        if self.single_node:
            self.properties['dataproc:dataproc.allow.zero.workers'] = 'true'
        if self.properties:
            cluster_data['config']['softwareConfig']['properties'] = self.properties
        cluster_data = self._build_lifecycle_config(cluster_data)
        if self.init_actions_uris:
            init_actions_dict = [{'executableFile':uri,  'executionTimeout':self._get_init_action_timeout()} for uri in self.init_actions_uris]
            cluster_data['config']['initializationActions'] = init_actions_dict
        if self.customer_managed_key:
            cluster_data['config']['encryptionConfig'] = {'gcePdKmsKeyName': self.customer_managed_key}
        if self.autoscaling_policy:
            cluster_data['config']['autoscalingConfig'] = {'policyUri': self.autoscaling_policy}
        return cluster_data

    def start(self):
        """
        Create a new cluster on Google Cloud Dataproc.
        """
        self.log.info('Creating cluster: %s', self.cluster_name)
        cluster_data = self._build_cluster_data()
        return self.hook.get_conn().projects().regions().clusters().create(projectId=(self.project_id),
          region=(self.region),
          body=cluster_data,
          requestId=(str(uuid.uuid4()))).execute()


class DataprocClusterScaleOperator(DataprocOperationBaseOperator):
    __doc__ = "\n    Scale, up or down, a cluster on Google Cloud Dataproc.\n    The operator will wait until the cluster is re-scaled.\n\n    **Example**: ::\n\n        t1 = DataprocClusterScaleOperator(\n                task_id='dataproc_scale',\n                project_id='my-project',\n                cluster_name='cluster-1',\n                num_workers=10,\n                num_preemptible_workers=10,\n                graceful_decommission_timeout='1h',\n                dag=dag)\n\n    .. seealso::\n        For more detail on about scaling clusters have a look at the reference:\n        https://cloud.google.com/dataproc/docs/concepts/configuring-clusters/scaling-clusters\n\n    :param cluster_name: The name of the cluster to scale. (templated)\n    :type cluster_name: str\n    :param project_id: The ID of the google cloud project in which\n        the cluster runs. (templated)\n    :type project_id: str\n    :param region: The region for the dataproc cluster. (templated)\n    :type region: str\n    :param gcp_conn_id: The connection ID to use connecting to Google Cloud Platform.\n    :type gcp_conn_id: str\n    :param num_workers: The new number of workers\n    :type num_workers: int\n    :param num_preemptible_workers: The new number of preemptible workers\n    :type num_preemptible_workers: int\n    :param graceful_decommission_timeout: Timeout for graceful YARN decomissioning.\n        Maximum value is 1d\n    :type graceful_decommission_timeout: str\n    :param delegate_to: The account to impersonate, if any.\n        For this to work, the service account making the request must have domain-wide\n        delegation enabled.\n    :type delegate_to: str\n    "
    template_fields = [
     'cluster_name', 'project_id', 'region']

    @apply_defaults
    def __init__(self, cluster_name, project_id, region='global', num_workers=2, num_preemptible_workers=0, graceful_decommission_timeout=None, *args, **kwargs):
        (super(DataprocClusterScaleOperator, self).__init__)(args, project_id=project_id, region=region, **kwargs)
        self.cluster_name = cluster_name
        self.num_workers = num_workers
        self.num_preemptible_workers = num_preemptible_workers
        self.optional_arguments = {}
        if graceful_decommission_timeout:
            self.optional_arguments['gracefulDecommissionTimeout'] = self._get_graceful_decommission_timeout(graceful_decommission_timeout)

    def _build_scale_cluster_data(self):
        scale_data = {'config': {'workerConfig':{'numInstances': self.num_workers}, 
                    'secondaryWorkerConfig':{'numInstances': self.num_preemptible_workers}}}
        return scale_data

    @staticmethod
    def _get_graceful_decommission_timeout(timeout):
        match = re.match('^(\\d+)(s|m|h|d)$', timeout)
        if match:
            if match.group(2) == 's':
                return timeout
            else:
                if match.group(2) == 'm':
                    val = float(match.group(1))
                    return '{}s'.format(timedelta(minutes=val).seconds)
                if match.group(2) == 'h':
                    val = float(match.group(1))
                    return '{}s'.format(timedelta(hours=val).seconds)
                if match.group(2) == 'd':
                    val = float(match.group(1))
                    return '{}s'.format(timedelta(days=val).seconds)
        raise AirflowException('DataprocClusterScaleOperator  should be expressed in day, hours, minutes or seconds.  i.e. 1d, 4h, 10m, 30s')

    def start(self):
        """
        Scale, up or down, a cluster on Google Cloud Dataproc.
        """
        self.log.info('Scaling cluster: %s', self.cluster_name)
        update_mask = 'config.worker_config.num_instances,config.secondary_worker_config.num_instances'
        scaling_cluster_data = self._build_scale_cluster_data()
        return (self.hook.get_conn().projects().regions().clusters().patch)(projectId=self.project_id, 
         region=self.region, 
         clusterName=self.cluster_name, 
         updateMask=update_mask, 
         body=scaling_cluster_data, 
         requestId=str(uuid.uuid4()), **self.optional_arguments).execute()


class DataprocClusterDeleteOperator(DataprocOperationBaseOperator):
    __doc__ = "\n    Delete a cluster on Google Cloud Dataproc. The operator will wait until the\n    cluster is destroyed.\n\n    :param cluster_name: The name of the cluster to delete. (templated)\n    :type cluster_name: str\n    :param project_id: The ID of the google cloud project in which\n        the cluster runs. (templated)\n    :type project_id: str\n    :param region: leave as 'global', might become relevant in the future. (templated)\n    :type region: str\n    :param gcp_conn_id: The connection ID to use connecting to Google Cloud Platform.\n    :type gcp_conn_id: str\n    :param delegate_to: The account to impersonate, if any.\n        For this to work, the service account making the request must have domain-wide\n        delegation enabled.\n    :type delegate_to: str\n    "
    template_fields = [
     'cluster_name', 'project_id', 'region']

    @apply_defaults
    def __init__(self, cluster_name, project_id, region='global', *args, **kwargs):
        (super(DataprocClusterDeleteOperator, self).__init__)(args, project_id=project_id, region=region, **kwargs)
        self.cluster_name = cluster_name

    def start(self):
        """
        Delete a cluster on Google Cloud Dataproc.
        """
        self.log.info('Deleting cluster: %s in %s', self.cluster_name, self.region)
        return self.hook.get_conn().projects().regions().clusters().delete(projectId=(self.project_id),
          region=(self.region),
          clusterName=(self.cluster_name),
          requestId=(str(uuid.uuid4()))).execute()


class DataProcJobBaseOperator(BaseOperator):
    __doc__ = '\n    The base class for operators that launch job on DataProc.\n\n    :param job_name: The job name used in the DataProc cluster. This name by default\n        is the task_id appended with the execution data, but can be templated. The\n        name will always be appended with a random number to avoid name clashes.\n    :type job_name: str\n    :param cluster_name: The name of the DataProc cluster.\n    :type cluster_name: str\n    :param dataproc_properties: Map for the Hive properties. Ideal to put in\n        default arguments (templated)\n    :type dataproc_properties: dict\n    :param dataproc_jars: HCFS URIs of jar files to add to the CLASSPATH of the Hive server and Hadoop\n        MapReduce (MR) tasks. Can contain Hive SerDes and UDFs. (templated)\n    :type dataproc_jars: list\n    :param gcp_conn_id: The connection ID to use connecting to Google Cloud Platform.\n    :type gcp_conn_id: str\n    :param delegate_to: The account to impersonate, if any.\n        For this to work, the service account making the request must have domain-wide\n        delegation enabled.\n    :type delegate_to: str\n    :param labels: The labels to associate with this job. Label keys must contain 1 to 63 characters,\n        and must conform to RFC 1035. Label values may be empty, but, if present, must contain 1 to 63\n        characters, and must conform to RFC 1035. No more than 32 labels can be associated with a job.\n    :type labels: dict\n    :param region: The specified region where the dataproc cluster is created.\n    :type region: str\n    :param job_error_states: Job states that should be considered error states.\n        Any states in this set will result in an error being raised and failure of the\n        task. Eg, if the ``CANCELLED`` state should also be considered a task failure,\n        pass in ``{\'ERROR\', \'CANCELLED\'}``. Possible values are currently only\n        ``\'ERROR\'`` and ``\'CANCELLED\'``, but could change in the future. Defaults to\n        ``{\'ERROR\'}``.\n    :type job_error_states: set\n    :var dataproc_job_id: The actual "jobId" as submitted to the Dataproc API.\n        This is useful for identifying or linking to the job in the Google Cloud Console\n        Dataproc UI, as the actual "jobId" submitted to the Dataproc API is appended with\n        an 8 character random string.\n    :vartype dataproc_job_id: str\n    '
    job_type = ''

    @apply_defaults
    def __init__(self, job_name='{{task.task_id}}_{{ds_nodash}}', cluster_name='cluster-1', dataproc_properties=None, dataproc_jars=None, gcp_conn_id='google_cloud_default', delegate_to=None, labels=None, region='global', job_error_states=None, *args, **kwargs):
        (super(DataProcJobBaseOperator, self).__init__)(*args, **kwargs)
        self.gcp_conn_id = gcp_conn_id
        self.delegate_to = delegate_to
        self.labels = labels
        self.job_name = job_name
        self.cluster_name = cluster_name
        self.dataproc_properties = dataproc_properties
        self.dataproc_jars = dataproc_jars
        self.region = region
        self.job_error_states = job_error_states if job_error_states is not None else {'ERROR'}
        self.hook = DataProcHook(gcp_conn_id=gcp_conn_id, delegate_to=delegate_to)
        self.job_template = None
        self.job = None
        self.dataproc_job_id = None

    def create_job_template(self):
        """
        Initialize `self.job_template` with default values
        """
        self.job_template = self.hook.create_job_template(self.task_id, self.cluster_name, self.job_type, self.dataproc_properties)
        self.job_template.set_job_name(self.job_name)
        self.job_template.add_jar_file_uris(self.dataproc_jars)
        self.job_template.add_labels(self.labels)

    def execute(self, context):
        """
        Build `self.job` based on the job template, and submit it.
        :raises AirflowException if no template has been initialized (see create_job_template)
        """
        if self.job_template:
            self.job = self.job_template.build()
            self.dataproc_job_id = self.job['job']['reference']['jobId']
            self.hook.submit(self.hook.project_id, self.job, self.region, self.job_error_states)
        else:
            raise AirflowException('Create a job template before')

    def on_kill(self):
        """
        Callback called when the operator is killed.
        Cancel any running job.
        """
        if self.dataproc_job_id:
            self.hook.cancel(self.hook.project_id, self.dataproc_job_id, self.region)


class DataProcPigOperator(DataProcJobBaseOperator):
    __doc__ = "\n    Start a Pig query Job on a Cloud DataProc cluster. The parameters of the operation\n    will be passed to the cluster.\n\n    It's a good practice to define dataproc_* parameters in the default_args of the dag\n    like the cluster name and UDFs.\n\n    .. code-block:: python\n\n        default_args = {\n            'cluster_name': 'cluster-1',\n            'dataproc_pig_jars': [\n                'gs://example/udf/jar/datafu/1.2.0/datafu.jar',\n                'gs://example/udf/jar/gpig/1.2/gpig.jar'\n            ]\n        }\n\n    You can pass a pig script as string or file reference. Use variables to pass on\n    variables for the pig script to be resolved on the cluster or use the parameters to\n    be resolved in the script as template parameters.\n\n    **Example**: ::\n\n        t1 = DataProcPigOperator(\n                task_id='dataproc_pig',\n                query='a_pig_script.pig',\n                variables={'out': 'gs://example/output/{{ds}}'},\n                dag=dag)\n\n    .. seealso::\n        For more detail on about job submission have a look at the reference:\n        https://cloud.google.com/dataproc/reference/rest/v1/projects.regions.jobs\n\n    :param query: The query or reference to the query\n        file (pg or pig extension). (templated)\n    :type query: str\n    :param query_uri: The HCFS URI of the script that contains the Pig queries.\n    :type query_uri: str\n    :param variables: Map of named parameters for the query. (templated)\n    :type variables: dict\n    :param dataproc_pig_properties: Map for the Pig properties. Ideal to put in\n        default arguments (templated)\n    :type dataproc_pig_properties: dict\n    :param dataproc_pig_jars: HCFS URIs of jar files to add to the CLASSPATH of the Pig Client and Hadoop\n        MapReduce (MR) tasks. Can contain Pig UDFs. (templated)\n    :type dataproc_pig_jars: list\n    "
    template_fields = ['query', 'variables', 'job_name', 'cluster_name', 'region',
     'dataproc_jars', 'dataproc_properties']
    template_ext = ('.pg', '.pig')
    ui_color = '#0273d4'
    job_type = 'pigJob'

    @apply_defaults
    def __init__(self, query=None, query_uri=None, variables=None, dataproc_pig_properties=None, dataproc_pig_jars=None, *args, **kwargs):
        (super(DataProcPigOperator, self).__init__)(args, dataproc_properties=dataproc_pig_properties, 
         dataproc_jars=dataproc_pig_jars, **kwargs)
        self.query = query
        self.query_uri = query_uri
        self.variables = variables

    def execute(self, context):
        self.create_job_template()
        if self.query is None:
            self.job_template.add_query_uri(self.query_uri)
        else:
            self.job_template.add_query(self.query)
        self.job_template.add_variables(self.variables)
        super(DataProcPigOperator, self).execute(context)


class DataProcHiveOperator(DataProcJobBaseOperator):
    __doc__ = '\n    Start a Hive query Job on a Cloud DataProc cluster.\n\n    :param query: The query or reference to the query file (q extension).\n    :type query: str\n    :param query_uri: The HCFS URI of the script that contains the Hive queries.\n    :type query_uri: str\n    :param variables: Map of named parameters for the query.\n    :type variables: dict\n    :param dataproc_hive_properties: Map for the Pig properties. Ideal to put in\n        default arguments  (templated)\n    :type dataproc_hive_properties: dict\n    :param dataproc_hive_jars: HCFS URIs of jar files to add to the CLASSPATH of the Hive server and Hadoop\n        MapReduce (MR) tasks. Can contain Hive SerDes and UDFs. (templated)\n    :type dataproc_hive_jars: list\n    '
    template_fields = ['query', 'variables', 'job_name', 'cluster_name', 'region',
     'dataproc_jars', 'dataproc_properties']
    template_ext = ('.q', '.hql')
    ui_color = '#0273d4'
    job_type = 'hiveJob'

    @apply_defaults
    def __init__(self, query=None, query_uri=None, variables=None, dataproc_hive_properties=None, dataproc_hive_jars=None, *args, **kwargs):
        (super(DataProcHiveOperator, self).__init__)(args, dataproc_properties=dataproc_hive_properties, 
         dataproc_jars=dataproc_hive_jars, **kwargs)
        self.query = query
        self.query_uri = query_uri
        self.variables = variables
        if self.query is not None:
            if self.query_uri is not None:
                raise AirflowException('Only one of `query` and `query_uri` can be passed.')

    def execute(self, context):
        self.create_job_template()
        if self.query is None:
            self.job_template.add_query_uri(self.query_uri)
        else:
            self.job_template.add_query(self.query)
        self.job_template.add_variables(self.variables)
        super(DataProcHiveOperator, self).execute(context)


class DataProcSparkSqlOperator(DataProcJobBaseOperator):
    __doc__ = '\n    Start a Spark SQL query Job on a Cloud DataProc cluster.\n\n    :param query: The query or reference to the query file (q extension). (templated)\n    :type query: str\n    :param query_uri: The HCFS URI of the script that contains the SQL queries.\n    :type query_uri: str\n    :param variables: Map of named parameters for the query. (templated)\n    :type variables: dict\n    :param dataproc_spark_properties: Map for the Pig properties. Ideal to put in\n        default arguments  (templated)\n    :type dataproc_spark_properties: dict\n    :param dataproc_spark_jars: HCFS URIs of jar files to be added to the Spark CLASSPATH. (templated)\n    :type dataproc_spark_jars: list\n    '
    template_fields = ['query', 'variables', 'job_name', 'cluster_name', 'region',
     'dataproc_jars', 'dataproc_properties']
    template_ext = ('.q', )
    ui_color = '#0273d4'
    job_type = 'sparkSqlJob'

    @apply_defaults
    def __init__(self, query=None, query_uri=None, variables=None, dataproc_spark_properties=None, dataproc_spark_jars=None, *args, **kwargs):
        (super(DataProcSparkSqlOperator, self).__init__)(args, dataproc_properties=dataproc_spark_properties, 
         dataproc_jars=dataproc_spark_jars, **kwargs)
        self.query = query
        self.query_uri = query_uri
        self.variables = variables
        if self.query is not None:
            if self.query_uri is not None:
                raise AirflowException('Only one of `query` and `query_uri` can be passed.')

    def execute(self, context):
        self.create_job_template()
        if self.query is None:
            self.job_template.add_query_uri(self.query_uri)
        else:
            self.job_template.add_query(self.query)
        self.job_template.add_variables(self.variables)
        super(DataProcSparkSqlOperator, self).execute(context)


class DataProcSparkOperator(DataProcJobBaseOperator):
    __doc__ = '\n    Start a Spark Job on a Cloud DataProc cluster.\n\n    :param main_jar: The HCFS URI of the jar file that contains the main class\n        (use this or the main_class, not both together).\n    :type main_jar: str\n    :param main_class: Name of the job class. (use this or the main_jar, not both\n        together).\n    :type main_class: str\n    :param arguments: Arguments for the job. (templated)\n    :type arguments: list\n    :param archives: List of archived files that will be unpacked in the work\n        directory. Should be stored in Cloud Storage.\n    :type archives: list\n    :param files: List of files to be copied to the working directory\n    :type files: list\n    :param dataproc_spark_properties: Map for the Pig properties. Ideal to put in\n        default arguments  (templated)\n    :type dataproc_spark_properties: dict\n    :param dataproc_spark_jars: HCFS URIs of files to be copied to the working directory of Spark drivers\n        and distributed tasks. Useful for naively parallel tasks. (templated)\n    :type dataproc_spark_jars: list\n    '
    template_fields = [
     'arguments', 'job_name', 'cluster_name', 'region',
     'dataproc_jars', 'dataproc_properties']
    ui_color = '#0273d4'
    job_type = 'sparkJob'

    @apply_defaults
    def __init__(self, main_jar=None, main_class=None, arguments=None, archives=None, files=None, dataproc_spark_properties=None, dataproc_spark_jars=None, *args, **kwargs):
        (super(DataProcSparkOperator, self).__init__)(args, dataproc_properties=dataproc_spark_properties, 
         dataproc_jars=dataproc_spark_jars, **kwargs)
        self.main_jar = main_jar
        self.main_class = main_class
        self.arguments = arguments
        self.archives = archives
        self.files = files

    def execute(self, context):
        self.create_job_template()
        self.job_template.set_main(self.main_jar, self.main_class)
        self.job_template.add_args(self.arguments)
        self.job_template.add_archive_uris(self.archives)
        self.job_template.add_file_uris(self.files)
        super(DataProcSparkOperator, self).execute(context)


class DataProcHadoopOperator(DataProcJobBaseOperator):
    __doc__ = '\n    Start a Hadoop Job on a Cloud DataProc cluster.\n\n    :param main_jar: The HCFS URI of the jar file containing the main class\n        (use this or the main_class, not both together).\n    :type main_jar: str\n    :param main_class: Name of the job class. (use this or the main_jar, not both\n        together).\n    :type main_class: str\n    :param arguments: Arguments for the job. (templated)\n    :type arguments: list\n    :param archives: List of archived files that will be unpacked in the work\n        directory. Should be stored in Cloud Storage.\n    :type archives: list\n    :param files: List of files to be copied to the working directory\n    :type files: list\n    :param dataproc_hadoop_properties: Map for the Pig properties. Ideal to put in\n        default arguments (tempplated)\n    :type dataproc_hadoop_properties: dict\n    :param dataproc_hadoop_jars: Jar file URIs to add to the CLASSPATHs of the Hadoop driver and\n        tasks. (templated)\n    :type dataproc_hadoop_jars: list\n    '
    template_fields = [
     'arguments', 'job_name', 'cluster_name',
     'region', 'dataproc_jars', 'dataproc_properties']
    ui_color = '#0273d4'
    job_type = 'hadoopJob'

    @apply_defaults
    def __init__(self, main_jar=None, main_class=None, arguments=None, archives=None, files=None, dataproc_hadoop_properties=None, dataproc_hadoop_jars=None, *args, **kwargs):
        (super(DataProcHadoopOperator, self).__init__)(args, dataproc_properties=dataproc_hadoop_properties, 
         dataproc_jars=dataproc_hadoop_jars, **kwargs)
        self.main_jar = main_jar
        self.main_class = main_class
        self.arguments = arguments
        self.archives = archives
        self.files = files

    def execute(self, context):
        self.create_job_template()
        self.job_template.set_main(self.main_jar, self.main_class)
        self.job_template.add_args(self.arguments)
        self.job_template.add_archive_uris(self.archives)
        self.job_template.add_file_uris(self.files)
        super(DataProcHadoopOperator, self).execute(context)


class DataProcPySparkOperator(DataProcJobBaseOperator):
    __doc__ = '\n    Start a PySpark Job on a Cloud DataProc cluster.\n\n    :param main: [Required] The Hadoop Compatible Filesystem (HCFS) URI of the main\n            Python file to use as the driver. Must be a .py file.\n    :type main: str\n    :param arguments: Arguments for the job. (templated)\n    :type arguments: list\n    :param archives: List of archived files that will be unpacked in the work\n        directory. Should be stored in Cloud Storage.\n    :type archives: list\n    :param files: List of files to be copied to the working directory\n    :type files: list\n    :param pyfiles: List of Python files to pass to the PySpark framework.\n        Supported file types: .py, .egg, and .zip\n    :type pyfiles: list\n    :param dataproc_pyspark_properties: Map for the Pig properties. Ideal to put in\n        default arguments (templated)\n    :type dataproc_pyspark_properties: dict\n    :param dataproc_pyspark_jars: HCFS URIs of jar files to add to the CLASSPATHs of the Python\n        driver and tasks. (templated)\n    :type dataproc_pyspark_jars: list\n    '
    template_fields = [
     'arguments', 'job_name', 'cluster_name',
     'region', 'dataproc_jars', 'dataproc_properties']
    ui_color = '#0273d4'
    job_type = 'pysparkJob'

    @staticmethod
    def _generate_temp_filename(filename):
        date = time.strftime('%Y%m%d%H%M%S')
        return '{}_{}_{}'.format(date, str(uuid.uuid4())[:8], ntpath.basename(filename))

    def _upload_file_temp(self, bucket, local_file):
        """
        Upload a local file to a Google Cloud Storage bucket.
        """
        temp_filename = self._generate_temp_filename(local_file)
        if not bucket:
            raise AirflowException("If you want Airflow to upload the local file to a temporary bucket, set the 'temp_bucket' key in the connection string")
        self.log.info('Uploading %s to %s', local_file, temp_filename)
        GoogleCloudStorageHook(google_cloud_storage_conn_id=(self.gcp_conn_id)).upload(bucket_name=bucket,
          object_name=temp_filename,
          mime_type='application/x-python',
          filename=local_file)
        return 'gs://{}/{}'.format(bucket, temp_filename)

    @apply_defaults
    def __init__(self, main, arguments=None, archives=None, pyfiles=None, files=None, dataproc_pyspark_properties=None, dataproc_pyspark_jars=None, *args, **kwargs):
        (super(DataProcPySparkOperator, self).__init__)(args, dataproc_properties=dataproc_pyspark_properties, 
         dataproc_jars=dataproc_pyspark_jars, **kwargs)
        self.main = main
        self.arguments = arguments
        self.archives = archives
        self.files = files
        self.pyfiles = pyfiles

    def execute(self, context):
        self.create_job_template()
        if os.path.isfile(self.main):
            cluster_info = self.hook.get_cluster(project_id=(self.hook.project_id),
              region=(self.region),
              cluster_name=(self.cluster_name))
            bucket = cluster_info['config']['configBucket']
            self.main = self._upload_file_temp(bucket, self.main)
        self.job_template.set_python_main(self.main)
        self.job_template.add_args(self.arguments)
        self.job_template.add_archive_uris(self.archives)
        self.job_template.add_file_uris(self.files)
        self.job_template.add_python_file_uris(self.pyfiles)
        super(DataProcPySparkOperator, self).execute(context)


class DataprocWorkflowTemplateInstantiateOperator(DataprocOperationBaseOperator):
    __doc__ = "\n    Instantiate a WorkflowTemplate on Google Cloud Dataproc. The operator will wait\n    until the WorkflowTemplate is finished executing.\n\n    .. seealso::\n        Please refer to:\n        https://cloud.google.com/dataproc/docs/reference/rest/v1beta2/projects.regions.workflowTemplates/instantiate\n\n    :param template_id: The id of the template. (templated)\n    :type template_id: str\n    :param project_id: The ID of the google cloud project in which\n        the template runs\n    :type project_id: str\n    :param region: leave as 'global', might become relevant in the future\n    :type region: str\n    :param gcp_conn_id: The connection ID to use connecting to Google Cloud Platform.\n    :type gcp_conn_id: str\n    :param delegate_to: The account to impersonate, if any.\n        For this to work, the service account making the request must have domain-wide\n        delegation enabled.\n    :type delegate_to: str\n    "
    template_fields = [
     'template_id']

    @apply_defaults
    def __init__(self, template_id, *args, **kwargs):
        (super(DataprocWorkflowTemplateInstantiateOperator, self).__init__)(*args, **kwargs)
        self.template_id = template_id

    def start(self):
        """
        Instantiate a WorkflowTemplate on Google Cloud Dataproc.
        """
        self.log.info('Instantiating Template: %s', self.template_id)
        return self.hook.get_conn().projects().regions().workflowTemplates().instantiate(name=('projects/%s/regions/%s/workflowTemplates/%s' % (
         self.project_id, self.region, self.template_id)),
          body={'requestId': str(uuid.uuid4())}).execute()


class DataprocWorkflowTemplateInstantiateInlineOperator(DataprocOperationBaseOperator):
    __doc__ = "\n    Instantiate a WorkflowTemplate Inline on Google Cloud Dataproc. The operator will\n    wait until the WorkflowTemplate is finished executing.\n\n    .. seealso::\n        Please refer to:\n        https://cloud.google.com/dataproc/docs/reference/rest/v1beta2/projects.regions.workflowTemplates/instantiateInline\n\n    :param template: The template contents. (templated)\n    :type template: map\n    :param project_id: The ID of the google cloud project in which\n        the template runs\n    :type project_id: str\n    :param region: leave as 'global', might become relevant in the future\n    :type region: str\n    :param gcp_conn_id: The connection ID to use connecting to Google Cloud Platform.\n    :type gcp_conn_id: str\n    :param delegate_to: The account to impersonate, if any.\n        For this to work, the service account making the request must have domain-wide\n        delegation enabled.\n    :type delegate_to: str\n    "
    template_fields = [
     'template']

    @apply_defaults
    def __init__(self, template, *args, **kwargs):
        (super(DataprocWorkflowTemplateInstantiateInlineOperator, self).__init__)(*args, **kwargs)
        self.template = template

    def start(self):
        """
        Instantiate a WorkflowTemplate Inline on Google Cloud Dataproc.
        """
        self.log.info('Instantiating Inline Template')
        return self.hook.get_conn().projects().regions().workflowTemplates().instantiateInline(parent=('projects/%s/regions/%s' % (self.project_id, self.region)),
          requestId=(str(uuid.uuid4())),
          body=(self.template)).execute()