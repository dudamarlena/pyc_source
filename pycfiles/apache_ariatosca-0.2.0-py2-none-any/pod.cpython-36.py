# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
    """Pod"""

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