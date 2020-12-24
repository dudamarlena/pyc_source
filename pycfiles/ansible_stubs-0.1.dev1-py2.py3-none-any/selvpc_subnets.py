# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/ansible/modules/selvpc/selvpc_subnets.py
# Compiled at: 2018-02-16 17:30:07
import os
from ansible.module_utils.basic import AnsibleModule
from selvpcclient.client import Client, setup_http_client
from ansible.modules.selvpc import custom_user_agent
from ansible.module_utils.selvpc_utils import common as c
from ansible.module_utils.selvpc_utils import subnets as s
DOCUMENTATION = '\n---\nmodule: selvpc_subnets\nshort_description: selvpc module for subnets management\ndescription:\n    - Create subnets\n    - Delete subnets\n    - Get info about subnets\nversion_added: "2.3"\nauthor: Rutskiy Daniil (@rutskiy)\noptions:\n  token:\n    description:\n     - Selectel VPC API token.\n  state:\n    description:\n     - Indicate desired state\n    required: true\n    default: present\n    choices: [\'present\', \'absent\']\n  list:\n    description:\n    - Option for getting list of desired objects (if possible)\n    default: false\n  project_name:\n    description:\n    - Selectel VPC project name\n  project_id:\n    description:\n    - Selectel VPC project ID\n  subnets:\n    description:\n    - Array of subnets [{\'region\': <region>, \'quantity\': <quantity>,\n    \'type\': <type>, \'prefix_length\': <prefix length>}]\n  subnet_id:\n    description:\n    - Subnet ID\n  force:\n    description:\n    - if \'true\' allows to delete "ACTIVE" subnet if it\'s needed\n    default: false\nrequirements:\n  - python-selvpcclient\nnote:\n    - For operations where \'project_id\' is needed you can use \'project_name\'\n    instead\n'
EXAMPLES = '\n# Describe state with 2 subnets in ru-1 region and 1 in ru-2\n- selvpc_subnets:\n      project_id: <project id>\n      subnets:\n      - region: ru-1\n        quantity: 2\n        type: <type>\n        prefix_length: <prefix length>\n      - region: ru-2\n        quantity: 1\n        type: <type>\n        prefix_length: <prefix length>\n# Delete all subnets\n- selvpc_subnets:\n    project_name: <project name>\n    licenses:\n    - region: ru-1\n      quantity: 0\n      type: <type>\n      prefix_length: <prefix length>\n    - region: ru-2\n      quantity: 0\n      type: <type>\n      prefix_length: <prefix length>\n    force: True\n# Delete specific subnets\n- selvpc_licenses:\n    state: absent\n    subnet_id: <subnet id>\n# Get info about all subnets\n- selvpc_subnets:\n    list: True\n# Get info about specific subnet\n- selvpc_subnets:\n    subnet_id: <subnet id>\n'

def _check_subnet_exists(client, subnet_id):
    try:
        client.subnets.show(subnet_id)
    except Exception:
        return False

    return True


def _system_state_change(module, client):
    state = module.params.get('state')
    if state == 'absent':
        subnet_id = module.params.get('subnet_id')
        if subnet_id:
            return _check_subnet_exists(client, subnet_id)
    if state == 'present':
        subnets = module.params.get('subnets')
        project_name = module.params.get('project_name')
        project_id = module.params.get('project_id')
        force = module.params.get('force')
        if not c._check_valid_quantity(subnets):
            return False
        if (project_name or project_id) and subnets:
            if not project_id:
                project = c.get_project_by_name(client, project_name)
                if not project:
                    return False
                project_id = project.id
            parsed_subnets = s.parse_subnets_to_add(subnets)
            actual_subnets = s.get_project_subnets_quantity(client, project_id)
            to_add, to_del = c.compare_existed_and_needed_objects(actual_subnets, parsed_subnets, force)
            if to_add or to_del:
                return True
            return False
    return False


def main():
    module = AnsibleModule(argument_spec=dict(state=dict(choices=['present', 'absent'], default='present'), token=dict(type='str', no_log=True), list=dict(type='bool', default=False), project_id=dict(type='str'), subnets=dict(type='list'), subnet_id=dict(type='str'), project_name=dict(type='str'), force=dict(type='bool', default=False)), supports_check_mode=True)
    project_id = module.params.get('project_id')
    state = module.params.get('state')
    show_list = module.params.get('list')
    subnet_id = module.params.get('subnet_id')
    subnets = module.params.get('subnets')
    project_name = module.params.get('project_name')
    force = module.params.get('force')
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
    if state == 'absent' and subnet_id:
        s.delete_subnet(module, client, subnet_id)
    if state == 'present':
        if subnets and (project_id or project_name):
            s.add_subnets(module, client, project_id, project_name, subnets, force)
        if subnet_id and not show_list or show_list:
            s.get_subnets(module, client, subnet_id, show_list=show_list)
    module.fail_json(msg="No params for 'subnets' operations.")


if __name__ == '__main__':
    main()