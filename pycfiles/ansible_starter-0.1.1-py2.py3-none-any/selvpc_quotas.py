# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/ansible/modules/selvpc/selvpc_quotas.py
# Compiled at: 2018-02-16 17:30:07
import os
from ansible.module_utils.basic import AnsibleModule
from selvpcclient.client import Client, setup_http_client
from ansible.modules.selvpc import custom_user_agent
from ansible.module_utils.selvpc_utils import common as c
from ansible.module_utils.selvpc_utils import quotas as q
DOCUMENTATION = '\n---\nmodule: selvpc_quotas\nshort_description: selvpc module for project quotas management\ndescription:\n    - Set/update quotas\n    - Get info about project quotas\nversion_added: "2.3"\nauthor: Rutskiy Daniil (@rutskiy)\noptions:\n  token:\n    description:\n     - Selectel VPC API token.\n  state:\n    description:\n     - Indicate desired state\n    required: true\n    default: present\n    choices: [\'present\', \'absent\']\n  list:\n    description:\n    - Option for getting list of desired objects (if possible)\n    default: false\n  project_name:\n    description:\n    - Selectel VPC project name\n  project_id:\n    description:\n    - Selectel VPC project ID\n  quotas:\n    description:\n    - Project quotas\nrequirements:\n  - python-selvpcclient\nnote:\n    - For operations where \'project_id\' is needed you can use \'project_name\'\n    instead\n'
EXAMPLES = '\n# Set quotas on project\n- selvpc_quotas:\n    project_name: <project name>\n    quotas:\n        compute_cores:\n         - region: ru-1\n           zone: ru-1a\n           value: 10\n        compute_ram:\n         - region: ru-1\n           zone: ru-1a\n           value: 1024\n        volume_gigabytes_fast:\n         - region: ru-1\n           zone: ru-1a\n           value: 100\n# Get specified project quotas\n- selvpc_quotas:\n    project_name: <project name>\n# Get quotas info for all domain projects\n- selvpc_quotas:\n    list: True\n'

def _system_state_change(module, client):
    state = module.params.get('state')
    if state == 'present':
        project_id = module.params.get('project_id')
        quotas = module.params.get('quotas')
        if not project_id and quotas:
            project_name = module.params.get('project_name')
            project = c.get_project_by_name(client, project_name)
            if project:
                project_id = project.id
        if quotas and project_id:
            return c._check_quotas_changes(client, quotas, project_id)
    return False


def main():
    module = AnsibleModule(argument_spec=dict(state=dict(choices=['present', 'absent'], default='present'), token=dict(type='str', no_log=True), list=dict(type='bool', default=False), project_name=dict(type='str'), project_id=dict(type='str'), quotas=dict(type='dict')), supports_check_mode=True)
    if module.params['token']:
        token = module.params['token']
    else:
        token = os.environ.get('SEL_TOKEN')
    url = os.environ.get('SEL_URL')
    try:
        http_client = setup_http_client(url, api_token=token, custom_headers=custom_user_agent)
        client = Client(http_client)
    except Exception:
        module.fail_json(msg='No token given')

    project_name = module.params.get('project_name')
    project_id = module.params.get('project_id')
    state = module.params.get('state')
    show_list = module.params.get('list')
    quotas = module.params.get('quotas')
    if module.check_mode:
        module.exit_json(changed=_system_state_change(module, client))
    if state == 'present':
        if quotas and (project_id or project_name):
            q.set_quotas(module, client, project_id, project_name, quotas)
        if (project_id or project_name) and not show_list or show_list:
            q.get_project_quotas(module, client, project_id, project_name, show_list=show_list)
    if state == 'absent':
        module.fail_json(msg="Wrong state for 'selvpc_quotas' operations.")
    module.fail_json(msg="No params for 'selvpc_quotas' operations.")


if __name__ == '__main__':
    main()