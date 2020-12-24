# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/ansible/modules/selvpc/selvpc_capabilities.py
# Compiled at: 2018-02-16 17:30:07
import os
from ansible.module_utils.basic import AnsibleModule
from ansible.modules.selvpc import custom_user_agent
from selvpcclient.client import Client, setup_http_client
from selvpcclient.exceptions.base import ClientException
DOCUMENTATION = '\n---\nmodule: selvpc_capabilities\nshort_description: get possible values of different variables\ndescription:\n    - Get info about possible values\nversion_added: "2.3"\nauthor: Rutskiy Daniil (@rutskiy)\noptions:\n  token:\n    description:\n     - Selectel VPC API token.\n  state:\n    description:\n     - Indicate desired state\n    required: true\n    default: present\n    choices: [\'present\', \'absent\']\nrequirements:\n  - python-selvpcclient\n'
EXAMPLES = '\n# Get info about capabilities\n- selvpc_capabilities:\n      state: present\n'

def main():
    module = AnsibleModule(argument_spec=dict(state=dict(choices=['present', 'absent'], default='present'), token=dict(type='str', no_log=True)), supports_check_mode=True)
    state = module.params.get('state')
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
        module.exit_json(changed=False)
    if state == 'present':
        try:
            result = client.capabilities.get()
        except ClientException as exp:
            module.fail_json(msg=str(exp))

        module.exit_json(result=result._info)
    module.fail_json(msg="Wrong 'state' param for 'capabilities' operation.")


if __name__ == '__main__':
    main()