# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/ansible/modules/selvpc/selvpc_projects.py
# Compiled at: 2018-02-16 17:30:07
import os
from ansible.module_utils.basic import AnsibleModule
from selvpcclient.client import Client, setup_http_client
from ansible.modules.selvpc import custom_user_agent
from ansible.module_utils.selvpc_utils import common as c
from ansible.module_utils.selvpc_utils import projects as p
DOCUMENTATION = '\n---\nmodule: selvpc_projects\nshort_description: selvpc module for projects management\ndescription:\n    - Create/delete/update projects\n    - Get info about projects\nversion_added: "2.3"\nauthor: Rutskiy Daniil (@rutskiy)\noptions:\n  token:\n    description:\n     - Selectel VPC API token.\n  state:\n    description:\n     - Indicate desired state\n    required: true\n    default: present\n    choices: [\'present\', \'absent\']\n  list:\n    description:\n    - Option for getting list of desired objects (if possible)\n    default: false\n  project_name:\n    description:\n    - Selectel VPC project name\n  project_id:\n    description:\n    - Selectel VPC project ID\n  new_name:\n    description:\n    - Option for project name update\nrequirements:\n  - python-selvpcclient\nnote:\n    - For operations where \'project_id\' is needed you can use \'project_name\'\n    instead\n'
EXAMPLES = '\n# Create project:\n- selvpc_projects:\n    project_name: <project name>\n# Delete project\n- selvpc_projects:\n    state: absent\n    project_name: <project name>\n# Update project name\n- selvpc_projects:\n    project_name: <project name>\n    new_name: <new project name>\n'

def _system_state_change(module, client):
    state = module.params.get('state')
    if state == 'absent':
        project_id = module.params.get('project_id')
        if not project_id:
            project_name = module.params.get('project_name')
            project = c.get_project_by_name(client, project_name)
            if not project:
                return False
            project_id = project.id
        return c._check_project_exists(client, project_id)
    if state == 'present':
        project_id = module.params.get('project_id')
        if not project_id:
            project_name = module.params.get('project_name')
            project = c.get_project_by_name(client, project_name)
            new_name = module.params.get('new_name')
            if new_name and project:
                return True
    return False


def main():
    module = AnsibleModule(argument_spec=dict(state=dict(choices=['present', 'absent'], default='present'), token=dict(type='str', no_log=True), list=dict(type='bool', default=False), project_name=dict(type='str'), project_id=dict(type='str'), new_name=dict(type='str'), quotas=dict(type='dict')), supports_check_mode=True)
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

    if module.check_mode:
        module.exit_json(changed=_system_state_change(module, client))
    project_name = module.params.get('project_name')
    project_id = module.params.get('project_id')
    state = module.params.get('state')
    show_list = module.params.get('list')
    new_name = module.params.get('new_name')
    if state == 'absent' and (project_id or project_name):
        p.delete_project(module, client, project_id, project_name)
    if state == 'present':
        if new_name and (project_id or project_name):
            p.update_project(module, client, project_id, project_name, new_name)
        if project_name and not c.get_project_by_name(client, project_name):
            p.create_project(module, client, project_name)
        if (project_id or project_name) and not show_list or show_list:
            p.get_project(module, client, project_id, project_name, show_list=show_list)
    module.fail_json(msg="No params for 'selvpc_projects' operations.")


if __name__ == '__main__':
    main()