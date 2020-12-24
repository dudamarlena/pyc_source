# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kubeobject/deployment.py
# Compiled at: 2019-10-01 18:18:07
# Size of source mod 2**32: 1669 bytes
from __future__ import annotations
from .serviceaccount import ServiceAccount
from kubernetes import client

class Deployment:
    __doc__ = 'This is a super simple Deployment wrapper. The only reason it is here it is because I will use it\n    to deploy the MongoDB Kubernetes Operator.\n    '

    @classmethod
    def create(cls, name, namespace, service_account: 'ServiceAccount', container_image, env) -> 'Deployment':
        api = client.AppsV1Api()
        spec = client.V1DeploymentSpec(replicas=1,
          selector=client.V1LabelSelector(match_labels={'app': name}),
          template=client.V1PodTemplateSpec(metadata=client.V1ObjectMeta(labels={'app': name}),
          spec=client.V1PodSpec(service_account_name=(service_account.name),
          containers=[
         client.V1Container(name=name,
           image=container_image,
           image_pull_policy='IfNotPresent',
           env=env)])))
        body = client.V1Deployment(metadata=client.V1ObjectMeta(name=name,
          namespace=namespace),
          spec=spec)
        return Deployment(name, namespace, api.create_namespaced_deployment(namespace, body))

    def __init__(self, name, namespace, backing_obj):
        self.name = name
        self.namespace = namespace
        self.backing_obj = backing_obj