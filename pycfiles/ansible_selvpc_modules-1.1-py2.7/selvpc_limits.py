# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/ansible/modules/selvpc/selvpc_limits.py
# Compiled at: 2018-02-16 17:30:07
import os
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.selvpc_utils.limits import get_domain_quotas, get_free_domain_quotas
from ansible.modules.selvpc import custom_user_agent
from selvpcclient.client import Client, setup_http_client
DOCUMENTATION = '\n---\nmodule: selvpc_limits\nshort_description: selvpc module for domain limits info\ndescription:\n    - Get info about domain limits\nversion_added: "2.3"\nauthor: Rutskiy Daniil (@rutskiy)\noptions:\n  token:\n    description:\n     - Selectel VPC API token.\n  state:\n    description:\n     - Indicate desired state\n    required: true\n    default: present\n    choices: [\'present\', \'absent\']\n  free:\n    description:\n    - Param for getting info about available resources\n    default: false\nrequirements:\n  - python-selvpcclient\n'
EXAMPLES = '\n# Get total amount of resources available to be allocated to projects\n- selvpc_limits:\n    state: present\n\n# Get amount of resources available to be allocated to projects\n- selvpc_limits:\n    free: True\n'

def main():
    module = AnsibleModule(argument_spec=dict(state=dict(choices=['present', 'absent'], default='present'), token=dict(type='str', no_log=True), free=dict(type='bool', default=False)), supports_check_mode=True)
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

    state = module.params.get('state')
    free = module.params.get('free')
    if module.check_mode:
        module.exit_json(changed=False)
    if state == 'present':
        if free:
            get_free_domain_quotas(module, client)
        get_domain_quotas(module, client)
    if state == 'absent':
        module.fail_json(msg="Wrong state for 'selvpc_limits' operations.")
    module.fail_json(msg="No params for 'selvpc_limits' operations.")


if __name__ == '__main__':
    main()