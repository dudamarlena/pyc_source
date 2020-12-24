# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/ansible/modules/selvpc/selvpc_tokens.py
# Compiled at: 2018-02-16 17:30:07
import os
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.selvpc_utils.common import _check_project_exists, get_project_by_name
from ansible.modules.selvpc import custom_user_agent
from selvpcclient.client import Client, setup_http_client
from selvpcclient.exceptions.base import ClientException
DOCUMENTATION = '\n---\nmodule: selvpc_tokens\nshort_description: selvpc module for tokens management\ndescription:\n    - Add tokens\nversion_added: "2.3"\nauthor: Rutskiy Daniil (@rutskiy)\noptions:\n  token:\n    description:\n     - Selectel VPC API token.\n  state:\n    description:\n     - Indicate desired state\n    required: true\n    default: present\n    choices: [\'present\', \'absent\']\n  project_name:\n    description:\n    - Selectel VPC project name\n  project_id:\n    description:\n    - Selectel VPC project ID\nrequirements:\n  - python-selvpcclient\nnote:\n  - For operations where \'project_id\' is needed you can use \'project_name\'\n  instead\n'
EXAMPLES = '\n# Create reseller token for project\n- selvpc_tokens:\n    project_id: <Project ID>\n'

def _system_state_change(module, client):
    state = module.params.get('state')
    if state == 'present':
        project_id = module.params.get('project_id')
        if not project_id:
            project_name = module.params.get('project_name')
            project = get_project_by_name(client, project_name)
            if not project:
                return False
        return _check_project_exists(client, project_id)
    return False


def main():
    module = AnsibleModule(argument_spec=dict(state=dict(choices=['present', 'absent'], default='present'), token=dict(type='str', no_log=True), project_id=dict(type='str'), project_name=dict(type='str')), supports_check_mode=True)
    project_id = module.params.get('project_id')
    state = module.params.get('state')
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
    if state == 'present' and (project_id or project_name):
        try:
            if not project_id:
                project = get_project_by_name(client, project_name)
                if not project:
                    raise ClientException(message='No such project')
                project_id = project.id
            client.tokens.create(project_id)
        except ClientException as exp:
            module.fail_json(msg=str(exp))

        module.exit_json(changed=True, result='Token has been created')
    elif state == 'absent' and project_id:
        module.fail_json(msg="Wrong 'state' for 'tokens' operations.")
    module.fail_json(msg="No params for 'tokens' operations.")


if __name__ == '__main__':
    main()