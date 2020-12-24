# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/kubernetes/kubernetes_request_factory/pod_request_factory.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4561 bytes
import yaml
from airflow.contrib.kubernetes.pod import Pod
from airflow.contrib.kubernetes.kubernetes_request_factory.kubernetes_request_factory import KubernetesRequestFactory

class SimplePodRequestFactory(KubernetesRequestFactory):
    __doc__ = '\n    Request generator for a simple pod.\n    '
    _yaml = 'apiVersion: v1\nkind: Pod\nmetadata:\n  name: name\nspec:\n  containers:\n    - name: base\n      image: airflow-worker:latest\n      command: ["/usr/local/airflow/entrypoint.sh", "/bin/bash sleep 25"]\n  restartPolicy: Never\n    '

    def __init__(self):
        pass

    def create(self, pod):
        req = yaml.safe_load(self._yaml)
        self.extract_name(pod, req)
        self.extract_labels(pod, req)
        self.extract_image(pod, req)
        self.extract_image_pull_policy(pod, req)
        self.extract_cmds(pod, req)
        self.extract_args(pod, req)
        self.extract_node_selector(pod, req)
        self.extract_env_and_secrets(pod, req)
        self.extract_volume_secrets(pod, req)
        self.attach_ports(pod, req)
        self.attach_volumes(pod, req)
        self.attach_volume_mounts(pod, req)
        self.extract_resources(pod, req)
        self.extract_service_account_name(pod, req)
        self.extract_init_containers(pod, req)
        self.extract_image_pull_secrets(pod, req)
        self.extract_annotations(pod, req)
        self.extract_affinity(pod, req)
        self.extract_hostnetwork(pod, req)
        self.extract_tolerations(pod, req)
        self.extract_security_context(pod, req)
        self.extract_dnspolicy(pod, req)
        return req


class ExtractXcomPodRequestFactory(KubernetesRequestFactory):
    __doc__ = '\n    Request generator for a pod with sidecar container.\n    '
    XCOM_MOUNT_PATH = '/airflow/xcom'
    SIDECAR_CONTAINER_NAME = 'airflow-xcom-sidecar'
    _yaml = 'apiVersion: v1\nkind: Pod\nmetadata:\n  name: name\nspec:\n  volumes:\n    - name: xcom\n      emptyDir: {{}}\n  containers:\n    - name: base\n      image: airflow-worker:latest\n      command: ["/usr/local/airflow/entrypoint.sh", "/bin/bash sleep 25"]\n      volumeMounts:\n        - name: xcom\n          mountPath: {xcomMountPath}\n    - name: {sidecarContainerName}\n      image: python:3.5-alpine\n      command:\n        - python\n        - -c\n        - |\n            import time\n            while True:\n                try:\n                    time.sleep(3600)\n                except KeyboardInterrupt:\n                    exit(0)\n      volumeMounts:\n        - name: xcom\n          mountPath: {xcomMountPath}\n  restartPolicy: Never\n    '.format(xcomMountPath=XCOM_MOUNT_PATH, sidecarContainerName=SIDECAR_CONTAINER_NAME)

    def __init__(self):
        pass

    def create(self, pod):
        req = yaml.safe_load(self._yaml)
        self.extract_name(pod, req)
        self.extract_labels(pod, req)
        self.extract_image(pod, req)
        self.extract_image_pull_policy(pod, req)
        self.extract_cmds(pod, req)
        self.extract_args(pod, req)
        self.extract_node_selector(pod, req)
        self.extract_env_and_secrets(pod, req)
        self.extract_volume_secrets(pod, req)
        self.attach_ports(pod, req)
        self.attach_volumes(pod, req)
        self.attach_volume_mounts(pod, req)
        self.extract_resources(pod, req)
        self.extract_service_account_name(pod, req)
        self.extract_init_containers(pod, req)
        self.extract_image_pull_secrets(pod, req)
        self.extract_annotations(pod, req)
        self.extract_affinity(pod, req)
        self.extract_hostnetwork(pod, req)
        self.extract_tolerations(pod, req)
        self.extract_security_context(pod, req)
        self.extract_dnspolicy(pod, req)
        return req