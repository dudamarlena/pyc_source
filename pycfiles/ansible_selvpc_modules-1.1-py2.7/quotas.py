# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/ansible/module_utils/selvpc_utils/quotas.py
# Compiled at: 2018-02-16 17:30:07
from selvpcclient.base import ParticleResponse
from ansible.module_utils.selvpc_utils import common, wrappers

@wrappers.create_object('quotas')
@common.check_project_id
def set_quotas(module, client, project_id, project_name, quotas):
    result, changed, msg = None, False, 'Project has already had such quotas'
    if common._check_quotas_changes(client, quotas, project_id):
        result = client.quotas.update(project_id, {'quotas': quotas})
        if isinstance(result, ParticleResponse):
            common.abort_particle_response_task(module, client, result, project_id, is_quotas=True)
        changed, msg = True, 'Quotas are set successfully'
    return (
     result, changed, msg)


@wrappers.get_object('quotas')
@common.check_project_id
def get_project_quotas(module, client, project_id, project_name, show_list=False):
    if not show_list:
        return client.quotas.get_project_quotas(project_id)
    return client.quotas.get_projects_quotas()