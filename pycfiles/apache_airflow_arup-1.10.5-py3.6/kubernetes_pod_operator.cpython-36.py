# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
    __doc__ = "\n    Execute a task in a Kubernetes Pod\n\n    :param image: Docker image you wish to launch. Defaults to dockerhub.io,\n        but fully qualified URLS will point to custom repositories\n    :type image: str\n    :param namespace: the namespace to run within kubernetes\n    :type namespace: str\n    :param cmds: entrypoint of the container. (templated)\n        The docker images's entrypoint is used if this is not provide.\n    :type cmds: list[str]\n    :param arguments: arguments of the entrypoint. (templated)\n        The docker image's CMD is used if this is not provided.\n    :type arguments: list[str]\n    :param image_pull_policy: Specify a policy to cache or always pull an image\n    :type image_pull_policy: str\n    :param image_pull_secrets: Any image pull secrets to be given to the pod.\n                               If more than one secret is required, provide a\n                               comma separated list: secret_a,secret_b\n    :type image_pull_secrets: str\n    :param ports: ports for launched pod\n    :type ports: list[airflow.contrib.kubernetes.pod.Port]\n    :param volume_mounts: volumeMounts for launched pod\n    :type volume_mounts: list[airflow.contrib.kubernetes.volume_mount.VolumeMount]\n    :param volumes: volumes for launched pod. Includes ConfigMaps and PersistentVolumes\n    :type volumes: list[airflow.contrib.kubernetes.volume.Volume]\n    :param labels: labels to apply to the Pod\n    :type labels: dict\n    :param startup_timeout_seconds: timeout in seconds to startup the pod\n    :type startup_timeout_seconds: int\n    :param name: name of the task you want to run,\n        will be used to generate a pod id\n    :type name: str\n    :param env_vars: Environment variables initialized in the container. (templated)\n    :type env_vars: dict\n    :param secrets: Kubernetes secrets to inject in the container,\n        They can be exposed as environment vars or files in a volume.\n    :type secrets: list[airflow.contrib.kubernetes.secret.Secret]\n    :param in_cluster: run kubernetes client with in_cluster configuration\n    :type in_cluster: bool\n    :param cluster_context: context that points to kubernetes cluster.\n        Ignored when in_cluster is True. If None, current-context is used.\n    :type cluster_context: str\n    :param get_logs: get the stdout of the container as logs of the tasks\n    :type get_logs: bool\n    :param annotations: non-identifying metadata you can attach to the Pod.\n                        Can be a large range of data, and can include characters\n                        that are not permitted by labels.\n    :type annotations: dict\n    :param resources: A dict containing a group of resources requests and limits\n    :type resources: dict\n    :param affinity: A dict containing a group of affinity scheduling rules\n    :type affinity: dict\n    :param node_selectors: A dict containing a group of scheduling rules\n    :type node_selectors: dict\n    :param config_file: The path to the Kubernetes config file\n    :type config_file: str\n    :param xcom_push: If xcom_push is True, the content of the file\n        /airflow/xcom/return.json in the container will also be pushed to an\n        XCom when the container completes.\n    :type xcom_push: bool\n    :param is_delete_operator_pod: What to do when the pod reaches its final\n        state, or the execution is interrupted.\n        If False (default): do nothing, If True: delete the pod\n    :type is_delete_operator_pod: bool\n    :param hostnetwork: If True enable host networking on the pod\n    :type hostnetwork: bool\n    :param tolerations: A list of kubernetes tolerations\n    :type tolerations: list tolerations\n    :param configmaps: A list of configmap names objects that we\n        want mount as env variables\n    :type configmaps: list[str]\n    :param pod_runtime_info_envs: environment variables about\n                                  pod runtime information (ip, namespace, nodeName, podName)\n    :type pod_runtime_info_envs: list[PodRuntimeEnv]\n    :param dnspolicy: Specify a dnspolicy for the pod\n    :type dnspolicy: str\n    "
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