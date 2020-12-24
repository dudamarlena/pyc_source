# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/kubernetes_pod_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 10544 bytes
from airflow.exceptions import AirflowException
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.contrib.kubernetes import kube_client, pod_generator, pod_launcher
from airflow.contrib.kubernetes.pod import Resources
from airflow.utils.state import State

class KubernetesPodOperator(BaseOperator):
    """KubernetesPodOperator"""
    template_fields = ('cmds', 'arguments', 'env_vars', 'config_file')

    def execute(self, context):
        try:
            client = kube_client.get_kube_client(in_cluster=(self.in_cluster), cluster_context=(self.cluster_context),
              config_file=(self.config_file))
            gen = pod_generator.PodGenerator()
            for port in self.ports:
                gen.add_port(port)

            for mount in self.volume_mounts:
                gen.add_mount(mount)

            for volume in self.volumes:
                gen.add_volume(volume)

            pod = gen.make_pod(namespace=(self.namespace),
              image=(self.image),
              pod_id=(self.name),
              cmds=(self.cmds),
              arguments=(self.arguments),
              labels=(self.labels))
            pod.service_account_name = self.service_account_name
            pod.secrets = self.secrets
            pod.envs = self.env_vars
            pod.image_pull_policy = self.image_pull_policy
            pod.image_pull_secrets = self.image_pull_secrets
            pod.annotations = self.annotations
            pod.resources = self.resources
            pod.affinity = self.affinity
            pod.node_selectors = self.node_selectors
            pod.hostnetwork = self.hostnetwork
            pod.tolerations = self.tolerations
            pod.configmaps = self.configmaps
            pod.security_context = self.security_context
            pod.pod_runtime_info_envs = self.pod_runtime_info_envs
            pod.dnspolicy = self.dnspolicy
            launcher = pod_launcher.PodLauncher(kube_client=client, extract_xcom=(self.xcom_push))
            try:
                final_state, result = launcher.run_pod(pod,
                  startup_timeout=(self.startup_timeout_seconds),
                  get_logs=(self.get_logs))
            finally:
                if self.is_delete_operator_pod:
                    launcher.delete_pod(pod)

            if final_state != State.SUCCESS:
                raise AirflowException('Pod returned a failure: {state}'.format(state=final_state))
            if self.xcom_push:
                return result
        except AirflowException as ex:
            raise AirflowException('Pod Launching failed: {error}'.format(error=ex))

    def _set_resources(self, resources):
        inputResource = Resources()
        if resources:
            for item in resources.keys():
                setattr(inputResource, item, resources[item])

        return inputResource

    @apply_defaults
    def __init__(self, namespace, image, name, cmds=None, arguments=None, ports=None, volume_mounts=None, volumes=None, env_vars=None, secrets=None, in_cluster=False, cluster_context=None, labels=None, startup_timeout_seconds=120, get_logs=True, image_pull_policy='IfNotPresent', annotations=None, resources=None, affinity=None, config_file=None, xcom_push=False, node_selectors=None, image_pull_secrets=None, service_account_name='default', is_delete_operator_pod=False, hostnetwork=False, tolerations=None, configmaps=None, security_context=None, pod_runtime_info_envs=None, dnspolicy=None, *args, **kwargs):
        (super(KubernetesPodOperator, self).__init__)(*args, **kwargs)
        self.image = image
        self.namespace = namespace
        self.cmds = cmds or []
        self.arguments = arguments or []
        self.labels = labels or {}
        self.startup_timeout_seconds = startup_timeout_seconds
        self.name = name
        self.env_vars = env_vars or {}
        self.ports = ports or []
        self.volume_mounts = volume_mounts or []
        self.volumes = volumes or []
        self.secrets = secrets or []
        self.in_cluster = in_cluster
        self.cluster_context = cluster_context
        self.get_logs = get_logs
        self.image_pull_policy = image_pull_policy
        self.node_selectors = node_selectors or {}
        self.annotations = annotations or {}
        self.affinity = affinity or {}
        self.xcom_push = xcom_push
        self.resources = self._set_resources(resources)
        self.config_file = config_file
        self.image_pull_secrets = image_pull_secrets
        self.service_account_name = service_account_name
        self.is_delete_operator_pod = is_delete_operator_pod
        self.hostnetwork = hostnetwork
        self.tolerations = tolerations or []
        self.configmaps = configmaps or []
        self.security_context = security_context or {}
        self.pod_runtime_info_envs = pod_runtime_info_envs or []
        self.dnspolicy = dnspolicy