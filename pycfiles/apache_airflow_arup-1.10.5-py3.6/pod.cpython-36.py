# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/kubernetes/pod.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 5533 bytes


class Resources:

    def __init__(self, request_memory=None, request_cpu=None, limit_memory=None, limit_cpu=None, limit_gpu=None):
        self.request_memory = request_memory
        self.request_cpu = request_cpu
        self.limit_memory = limit_memory
        self.limit_cpu = limit_cpu
        self.limit_gpu = limit_gpu

    def is_empty_resource_request(self):
        return not self.has_limits() and not self.has_requests()

    def has_limits(self):
        return self.limit_cpu is not None or self.limit_memory is not None or self.limit_gpu is not None

    def has_requests(self):
        return self.request_cpu is not None or self.request_memory is not None

    def __str__(self):
        return 'Request: [cpu: {}, memory: {}], Limit: [cpu: {}, memory: {}, gpu: {}]'.format(self.request_cpu, self.request_memory, self.limit_cpu, self.limit_memory, self.limit_gpu)


class Port:

    def __init__(self, name=None, container_port=None):
        self.name = name
        self.container_port = container_port


class Pod:
    __doc__ = '\n    Represents a kubernetes pod and manages execution of a single pod.\n    :param image: The docker image\n    :type image: str\n    :param envs: A dict containing the environment variables\n    :type envs: dict\n    :param cmds: The command to be run on the pod\n    :type cmds: list[str]\n    :param secrets: Secrets to be launched to the pod\n    :type secrets: list[airflow.contrib.kubernetes.secret.Secret]\n    :param result: The result that will be returned to the operator after\n        successful execution of the pod\n    :type result: any\n    :param image_pull_policy: Specify a policy to cache or always pull an image\n    :type image_pull_policy: str\n    :param image_pull_secrets: Any image pull secrets to be given to the pod.\n        If more than one secret is required, provide a comma separated list:\n        secret_a,secret_b\n    :type image_pull_secrets: str\n    :param affinity: A dict containing a group of affinity scheduling rules\n    :type affinity: dict\n    :param hostnetwork: If True enable host networking on the pod\n    :type hostnetwork: bool\n    :param tolerations: A list of kubernetes tolerations\n    :type tolerations: list\n    :param security_context: A dict containing the security context for the pod\n    :type security_context: dict\n    :param configmaps: A list containing names of configmaps object\n        mounting env variables to the pod\n    :type configmaps: list[str]\n    :param pod_runtime_info_envs: environment variables about\n                                  pod runtime information (ip, namespace, nodeName, podName)\n    :type pod_runtime_info_envs: list[PodRuntimeEnv]\n    :param dnspolicy: Specify a dnspolicy for the pod\n    :type dnspolicy: str\n    '

    def __init__(self, image, envs, cmds, args=None, secrets=None, labels=None, node_selectors=None, name=None, ports=None, volumes=None, volume_mounts=None, namespace='default', result=None, image_pull_policy='IfNotPresent', image_pull_secrets=None, init_containers=None, service_account_name=None, resources=None, annotations=None, affinity=None, hostnetwork=False, tolerations=None, security_context=None, configmaps=None, pod_runtime_info_envs=None, dnspolicy=None):
        self.image = image
        self.envs = envs or {}
        self.cmds = cmds
        self.args = args or []
        self.secrets = secrets or []
        self.result = result
        self.labels = labels or {}
        self.name = name
        self.ports = ports or []
        self.volumes = volumes or []
        self.volume_mounts = volume_mounts or []
        self.node_selectors = node_selectors or {}
        self.namespace = namespace
        self.image_pull_policy = image_pull_policy
        self.image_pull_secrets = image_pull_secrets
        self.init_containers = init_containers
        self.service_account_name = service_account_name
        self.resources = resources or Resources()
        self.annotations = annotations or {}
        self.affinity = affinity or {}
        self.hostnetwork = hostnetwork or False
        self.tolerations = tolerations or []
        self.security_context = security_context
        self.configmaps = configmaps or []
        self.pod_runtime_info_envs = pod_runtime_info_envs or []
        self.dnspolicy = dnspolicy