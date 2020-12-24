# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/ansible/modules/selvpc/selvpc_roles.py
# Compiled at: 2018-02-16 17:30:07
import os
from ansible.module_utils.basic import AnsibleModule
from selvpcclient.client import Client, setup_http_client
from ansible.modules.selvpc import custom_user_agent
from ansible.module_utils.selvpc_utils import common as c
from ansible.module_utils.selvpc_utils import roles as r
DOCUMENTATION = '\n---\nmodule: selvpc_roles\nshort_description: selvpc module for roles management\ndescription:\n    - Add roles to project\n    - Delete roles\n    - Get info about roles\nversion_added: "2.3"\nauthor: Rutskiy Daniil (@rutskiy)\noptions:\n  token:\n    description:\n     - Selectel VPC API token.\n  state:\n    description:\n     - Indicate desired state\n    required: true\n    default: present\n    choices: [\'present\', \'absent\']\n  list:\n    description:\n    - Option for getting list of desired objects (if possible)\n    default: false\n  project_name:\n    description:\n    - Selectel VPC project name\n  project_id:\n    description:\n    - Selectel VPC project ID\n  roles:\n    description:\n    - Array of roles [{\'project_id\': <project_id>, \'user_id\': <user_id>}]\n  user_id:\n    description:\n    - User ID\nrequirements:\n  - python-selvpcclient\n'
EXAMPLES = '\n# Add role to project\n- selvpc_roles:\n    user_id: <user id>\n    project_id: <project id>\n# Delete role\n- selvpc_roles:\n    state: absent\n    user_id: <user id>\n    project_id: <project id>\n# Add few users at once\n- selvpc_roles:\n    roles:\n      - project_id: <project id>\n        user_id: <user id>\n      - project_id: <project id>\n        user_id: <user id>\n'

def _system_state_change(module, client):
    state = module.params.get('state')
    project_id = module.params.get('project_id')
    user_id = module.params.get('user_id')
    roles = module.params.get('roles')
    project_name = module.params.get('project_name')
    if state == 'absent':
        if not project_id:
            project = c.get_project_by_name(client, project_name)
            if not project:
                return False
            project_id = project.id
        return c._check_user_role(client, project_id, user_id)
    if state == 'present':
        if (project_id or project_name) and user_id:
            if not project_id:
                project = c.get_project_by_name(client, project_name)
                if not project:
                    return False
                project_id = project.id
            if c._check_user_role(client, project_id, user_id):
                return False
            return True
        if c._check_project_roles(client, roles):
            return True
    return False


def main():
    module = AnsibleModule(argument_spec=dict(state=dict(choices=['present', 'absent'], default='present'), token=dict(type='str', no_log=True), project_id=dict(type='str'), user_id=dict(type='str'), roles=dict(type='list'), project_name=dict(type='str')), supports_check_mode=True)
    project_id = module.params.get('project_id')
    state = module.params.get('state')
    user_id = module.params.get('user_id')
    roles = module.params.get('roles')
    project_name = module.params.get('project_name')
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
    if state == 'absent' and (project_id or project_name) and user_id:
        r.delete_role(module, client, project_id, project_name, user_id)
    if state == 'present':
        if user_id and (project_id or project_name):
            r.add_role(module, client, project_id, project_name, user_id)
        if roles:
            r.add_bulk_roles(module, client, roles)
        if user_id:
            r.get_user_roles(module, client, user_id)
        if project_id or project_name:
            r.get_project_roles(module, client, project_id, project_name)
    module.fail_json(msg="No params for 'roles' operations.")


if __name__ == '__main__':
    main()