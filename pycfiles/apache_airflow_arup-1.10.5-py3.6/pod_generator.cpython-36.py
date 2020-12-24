# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/kubernetes/pod_generator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 5493 bytes
from airflow.contrib.kubernetes.pod import Pod, Port
from airflow.contrib.kubernetes.volume import Volume
from airflow.contrib.kubernetes.volume_mount import VolumeMount
import uuid

class PodGenerator:
    __doc__ = 'Contains Kubernetes Airflow Worker configuration logic'

    def __init__(self, kube_config=None):
        self.kube_config = kube_config
        self.ports = []
        self.volumes = []
        self.volume_mounts = []
        self.init_containers = []

    def add_init_container(self, name, image, security_context, init_environment, volume_mounts):
        """

        Adds an init container to the launched pod. useful for pre-

        Args:
            name (str):
            image (str):
            security_context (dict):
            init_environment (dict):
            volume_mounts (dict):

        Returns:

        """
        self.init_containers.append({'name':name, 
         'image':image, 
         'securityContext':security_context, 
         'env':init_environment, 
         'volumeMounts':volume_mounts})

    def _get_init_containers(self):
        return self.init_containers

    def add_port(self, port):
        """
        Adds a Port to the generator

        :param port: ports for generated pod
        :type port: airflow.contrib.kubernetes.pod.Port
        """
        self.ports.append({'name':port.name,  'containerPort':port.container_port})

    def add_volume(self, volume):
        """
        Adds a Volume to the generator

        :param volume: volume for generated pod
        :type volume: airflow.contrib.kubernetes.volume.Volume
        """
        self._add_volume(name=(volume.name), configs=(volume.configs))

    def _add_volume(self, name, configs):
        """

        Args:
            name (str):
            configs (dict): Configurations for the volume.
            Could be used to define PersistentVolumeClaim, ConfigMap, etc...

        Returns:

        """
        volume_map = {'name': name}
        for k, v in configs.items():
            volume_map[k] = v

        self.volumes.append(volume_map)

    def add_volume_with_configmap(self, name, config_map):
        self.volumes.append({'name':name, 
         'configMap':config_map})

    def _add_mount(self, name, mount_path, sub_path, read_only):
        """

        Args:
            name (str):
            mount_path (str):
            sub_path (str):
            read_only:

        Returns:

        """
        self.volume_mounts.append({'name':name, 
         'mountPath':mount_path, 
         'subPath':sub_path, 
         'readOnly':read_only})

    def add_mount(self, volume_mount):
        """
        Adds a VolumeMount to the generator

        :param volume_mount: volume for generated pod
        :type volume_mount: airflow.contrib.kubernetes.volume_mount.VolumeMount
        """
        self._add_mount(name=(volume_mount.name),
          mount_path=(volume_mount.mount_path),
          sub_path=(volume_mount.sub_path),
          read_only=(volume_mount.read_only))

    def _get_volumes_and_mounts(self):
        return (
         self.volumes, self.volume_mounts)

    def _get_image_pull_secrets(self):
        """Extracts any image pull secrets for fetching container(s)"""
        if not self.kube_config.image_pull_secrets:
            return []
        else:
            return self.kube_config.image_pull_secrets.split(',')

    def make_pod(self, namespace, image, pod_id, cmds, arguments, labels):
        volumes, volume_mounts = self._get_volumes_and_mounts()
        worker_init_container_spec = self._get_init_containers()
        return Pod(namespace=namespace,
          name=(pod_id + '-' + str(uuid.uuid4())[:8]),
          image=image,
          cmds=cmds,
          args=arguments,
          labels=labels,
          envs={},
          secrets=[],
          init_containers=worker_init_container_spec,
          ports=(self.ports),
          volumes=volumes,
          volume_mounts=volume_mounts,
          resources=None)