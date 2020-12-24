# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/ansible/module_utils/selvpc_utils/limits.py
# Compiled at: 2018-02-16 17:30:07
from ansible.module_utils.selvpc_utils import wrappers

@wrappers.get_object('quotas')
def get_domain_quotas(module, client):
    return client.quotas.get_domain_quotas()


@wrappers.get_object('quotas')
def get_free_domain_quotas(module, client):
    return client.quotas.get_free_domain_quotas()