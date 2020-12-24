# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/ansible/modules/selvpc/selvpc_users.py
# Compiled at: 2018-02-16 17:30:07
import os
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.selvpc_utils.common import _check_user_exists, get_user_by_name
from ansible.module_utils.selvpc_utils.users import create_user, delete_user, get_users, update_user
from ansible.modules.selvpc import custom_user_agent
from selvpcclient.client import Client, setup_http_client
DOCUMENTATION = '\n---\nmodule: selvpc_users\nshort_description: selvpc module for users management\ndescription:\n    - Add users\n    - Delete users\n    - Update username/password\n    - Get info about users\nversion_added: "2.3"\nauthor: Rutskiy Daniil (@rutskiy)\noptions:\n  token:\n    description:\n     - Selectel VPC API token.\n  state:\n    description:\n     - Indicate desired state\n    required: true\n    default: present\n    choices: [\'present\', \'absent\']\n  project_name:\n    description:\n    - Selectel VPC project name\n  project_id:\n    description:\n    - Selectel VPC project ID\n  username:\n    description:\n    - Name for new user in project\n  password:\n    description:\n    - Password for new user in project\n  new_username:\n    description:\n    - Option for username update\n  password:\n    description:\n    - Option for password update\n  user_id:\n    description:\n    - User ID\n  enabled:\n    description:\n    - User state\n    default: True\nrequirements:\n  - python-selvpcclient\nnote:\n  - For operations where \'project_id\' is needed you can use \'project_name\'\n  instead\n'
EXAMPLES = '\n# Create user\n- selvpc_users:\n    username: <username>\n    password: <password>\n'

def _system_state_change(module, client):
    state = module.params.get('state')
    if state == 'absent':
        user_id = module.params.get('user_id')
        return _check_user_exists(client, user_id)
    if state == 'present':
        username = module.params.get('username')
        password = module.params.get('password')
        new_username = module.params.get('new_username')
        new_password = module.params.get('new_password')
        user_id = module.params.get('user_id')
        if username and password:
            user = get_user_by_name(client, username)
            if not user:
                return True
        if user_id and (new_username or new_password) or new_username and new_password:
            return True
    return False


def main():
    module = AnsibleModule(argument_spec=dict(state=dict(choices=['present', 'absent'], default='present'), token=dict(type='str', no_log=True), username=dict(type='str'), password=dict(type='str', no_log=True), new_username=dict(type='str'), new_password=dict(type='str', no_log=True), user_id=dict(type='str'), enabled=dict(type='bool', default=True)), supports_check_mode=True)
    state = module.params.get('state')
    username = module.params.get('username')
    password = module.params.get('password')
    new_username = module.params.get('new_username')
    new_password = module.params.get('new_password')
    user_id = module.params.get('user_id')
    enabled = module.params.get('enabled')
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
    if state == 'absent' and user_id:
        delete_user(module, client, user_id)
    if state == 'present':
        if username and password:
            create_user(module, client, username, password, enabled)
        if user_id and (new_username or new_password) or new_username and new_password:
            update_user(module, client, user_id, new_username, new_password, enabled)
        get_users(module, client)
    module.fail_json(msg="No params for 'users' operations.")


if __name__ == '__main__':
    main()