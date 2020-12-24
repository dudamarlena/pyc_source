# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kubeobject/service.py
# Compiled at: 2019-10-01 18:18:07
# Size of source mod 2**32: 945 bytes
from __future__ import annotations
from kubernetes import client

class Service:

    @classmethod
    def create(cls, name, namespace):
        """Creates a Service"""
        api = client.CoreV1Api()
        body = client.V1Service(metadata=client.V1ObjectMeta(name=name,
          namespace=namespace),
          spec=client.V1ServiceSpec(publish_not_ready_addresses=True,
          ports=[
         client.V1ServicePort(port=27017)]))
        return Service(name, namespace, api.create_namespaced_service(namespace, body))

    @classmethod
    def load(cls, name, namespace):
        api = client.CoreV1Api()
        return Service(name, namespace, api.read_namespaced_service(name, namespace))

    def __init__(self, name, namespace, backing_obj):
        self.name = name
        self.namespace = namespace
        self.backing_obj = backing_obj