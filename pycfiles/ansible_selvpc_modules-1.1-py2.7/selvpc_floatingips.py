# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/ansible/modules/selvpc/selvpc_floatingips.py
# Compiled at: 2018-02-16 17:30:07
import os
from ansible.module_utils.basic import AnsibleModule
from ansible.modules.selvpc import custom_user_agent
from selvpcclient.client import Client, setup_http_client
from ansible.module_utils.selvpc_utils import common as c
from ansible.module_utils.selvpc_utils import floatingips as f
DOCUMENTATION = '\n---\nmodule: selvpc_floatingips\nshort_description: selvpc module for floating ips management\ndescription:\n    - Create floating ips\n    - Delete floating ips\n    - Get info about floating ips\nversion_added: "2.3"\nauthor: Rutskiy Daniil (@rutskiy)\noptions:\n  token:\n    description:\n     - Selectel VPC API token.\n  state:\n    description:\n     - Indicate desired state\n    required: true\n    default: present\n    choices: [\'present\', \'absent\']\n  list:\n    description:\n    - Option for getting list of desired objects (if possible)\n    default: false\n  project_name:\n    description:\n    - Selectel VPC project name\n  project_id:\n    description:\n    - Selectel VPC project ID\n  floatingip:\n    description:\n    - Floating ip "XXX.XXX.XXX.XXX"\n  floatingips:\n    description:\n    - Array of floating IPs [{\'region\': <region>, \'quantity\': <quantity>}]\n  floatingip_id:\n    description:\n    - Floating IP ID\n  force:\n    description:\n    - if \'true\' allows to delete "ACTIVE" floating ips if it\'s needed\n    default: false\nrequirements:\n  - python-selvpcclient\nnote:\n    - For operations where \'project_id\' is needed you can use \'project_name\'\n    instead\n'
EXAMPLES = '\n# Describe state with 2 ips in ru-1 region and 1 in ru-2\n- selvpc_floatingips:\n      project_id: <project id>\n      floatingips:\n      - region: ru-1\n        quantity: 2\n      - region: ru-2\n        quantity: 1\n# Delete all ips\n- selvpc_floatingips:\n    project_name: <project name>\n    floatingips:\n    - region: ru-1\n      quantity: 0\n    - region: ru-2\n      quantity: 0\n    force: True\n# Delete specific ip\n- selvpc_floatingips:\n    state: absent\n    floatingip_id: <floating ip id>\n# Delete floating ip by ip\n- selvpc_floatingip:\n    state: absent\n    floatingip: 79.183.144.19\n# Get info about all ips\n- selvpc_floatingips:\n    list: True\n# Get info about specific ip\n- selvpc_floatingips:\n    floatingip_id: <floating ip id>\n'

def _check_floatingip_exists(client, floatingip_id):
    try:
        client.floatingips.show(floatingip_id)
    except Exception:
        return False

    return True


def _system_state_change(module, client):
    state = module.params.get('state')
    if state == 'absent':
        floatingip_id = module.params.get('floatingip_id')
        floatingip = module.params.get('floatingip')
        if floatingip_id:
            return _check_floatingip_exists(client, floatingip_id)
        if floatingip and c._check_valid_ip(floatingip):
            if c.get_floatingip_by_ip(client, floatingip):
                return True
            return False
    if state == 'present':
        floatingips = module.params.get('floatingips')
        project_name = module.params.get('project_name')
        project_id = module.params.get('floatingip_id')
        force = module.params.get('force')
        if not c._check_valid_quantity(floatingips):
            return False
        if (project_name or project_id) and floatingips:
            if not project_id:
                project = c.get_project_by_name(client, project_name)
                if not project:
                    return False
                project_id = project.id
            parsed_ips = f.parse_floatingips_to_add(floatingips)
            actual_ips = f.get_project_ips_quantity(client, project_id)
            to_add, to_del = c.compare_existed_and_needed_objects(actual_ips, parsed_ips, force)
            if to_add or to_del:
                return True
            return False
    return False


def main():
    module = AnsibleModule(argument_spec=dict(state=dict(choices=['present', 'absent'], default='present'), token=dict(type='str', no_log=True), list=dict(type='bool', default=False), project_id=dict(type='str'), floatingips=dict(type='list'), floatingip_id=dict(type='str'), project_name=dict(type='str'), floatingip=dict(type='str'), force=dict(type='bool', default=False)), supports_check_mode=True)
    project_id = module.params.get('project_id')
    state = module.params.get('state')
    show_list = module.params.get('list')
    floatingips = module.params.get('floatingips')
    floatingip_id = module.params.get('floatingip_id')
    project_name = module.params.get('project_name')
    floatingip = module.params.get('floatingip')
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
    if state == 'absent' and (floatingip_id or floatingip):
        f.delete_floatingip(module, client, floatingip_id, floatingip)
    if state == 'present':
        if floatingips and (project_id or project_name):
            f.add_floatingips(module, client, project_id, project_name, floatingips, force)
        if floatingip_id and not show_list or show_list:
            f.get_floatingips(module, client, floatingip_id, show_list=show_list)
    module.fail_json(msg="No params for 'floatingips' operations.")


if __name__ == '__main__':
    main()