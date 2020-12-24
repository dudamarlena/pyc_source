# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/ansible/module_utils/selvpc_utils/limits.py
# Compiled at: 2018-02-16 17:30:07
from ansible.module_utils.selvpc_utils import wrappers

@wrappers.get_object('quotas')
def get_domain_quotas(module, client):
    return client.quotas.get_domain_quotas()


@wrappers.get_object('quotas')
def get_free_domain_quotas(module, client):
    return client.quotas.get_free_domain_quotas()