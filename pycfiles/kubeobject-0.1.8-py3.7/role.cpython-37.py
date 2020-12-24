# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kubeobject/role.py
# Compiled at: 2019-10-01 18:18:07
# Size of source mod 2**32: 2066 bytes
from __future__ import annotations
from .serviceaccount import ServiceAccount
from kubernetes import client

class Role:

    @classmethod
    def create(cls, name, namespace, rules):
        api = client.RbacAuthorizationV1Api()
        body = client.V1Role(metadata=client.V1ObjectMeta(name=name, namespace=namespace),
          rules=rules)
        return Role(name, namespace, api.create_namespaced_role(namespace, body))

    def __init__(self, name, namespace, backing_obj):
        self.name = name
        self.namespace = namespace
        self.backing_obj = backing_obj


class RoleBinding:

    @classmethod
    def create(cls, name, namespace, role: 'Role', service_account: 'ServiceAccount'):
        api = client.RbacAuthorizationV1Api()
        role_ref = client.V1RoleRef(api_group='rbac.authorization.k8s.io',
          kind='Role',
          name=(role.name))
        subjects = [
         client.V1Subject(kind='ServiceAccount',
           name=(service_account.name),
           namespace=(service_account.namespace))]
        body = client.V1RoleBinding(metadata=client.V1ObjectMeta(name=name, namespace=namespace),
          role_ref=role_ref,
          subjects=subjects)
        return Role(name, namespace, api.create_namespaced_role_binding(namespace, body))

    def __init__(self, name, namespace, backing_obj):
        self.name = name
        self.namespace = namespace
        self.backing_obj = backing_obj


def build_rules_from_yaml(doc):
    rules = []
    for rule in doc['rules']:
        api_groups = rule.get('apiGroups', [''])
        resources = rule.get('resources', [''])
        verbs = rule.get('verbs', [''])
        rules.append(client.V1PolicyRule(api_groups=api_groups,
          resources=resources,
          verbs=verbs))

    return rules