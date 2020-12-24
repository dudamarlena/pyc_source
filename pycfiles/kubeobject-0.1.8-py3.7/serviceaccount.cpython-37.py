# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kubeobject/serviceaccount.py
# Compiled at: 2019-10-01 18:18:07
# Size of source mod 2**32: 727 bytes
from __future__ import annotations
from kubernetes import client

class ServiceAccount:

    @classmethod
    def create(cls, name, namespace):
        api = client.CoreV1Api()
        body = client.V1ServiceAccount(metadata=client.V1ObjectMeta(name=name, namespace=namespace))
        return ServiceAccount(name, namespace, api.create_namespaced_service_account(namespace, body=body))

    def __init__(self, name, namespace, backing_obj):
        self.name = name
        self.namespace = namespace
        self.backing_obj = backing_obj

    def delete(self):
        api = client.CoreV1Api()
        return api.delete_namespaced_service_account(self.name, self.namespace, client.V1DeleteOptions())