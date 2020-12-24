# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/ansible/modules/selvpc/selvpc_licenses.py
# Compiled at: 2018-02-16 17:30:07
import os
from ansible.module_utils.basic import AnsibleModule
from selvpcclient.client import Client, setup_http_client
from ansible.modules.selvpc import custom_user_agent
from ansible.module_utils.selvpc_utils import common as c
from ansible.module_utils.selvpc_utils import licenses as lic
DOCUMENTATION = '\n---\nmodule: selvpc_licenses\nshort_description: selvpc module for licenses management\ndescription:\n    - Create licenses\n    - Delete licenses\n    - Get info about licenses\nversion_added: "2.3"\nauthor: Rutskiy Daniil (@rutskiy)\noptions:\n  token:\n    description:\n     - Selectel VPC API token.\n  state:\n    description:\n     - Indicate desired state\n    required: true\n    default: present\n    choices: [\'present\', \'absent\']\n  list:\n    description:\n    - Option for getting list of desired objects (if possible)\n    default: false\n  project_name:\n    description:\n    - Selectel VPC project name\n  project_id:\n    description:\n    - Selectel VPC project ID\n  licenses:\n    description:\n    - Array of licenses [{\'region\': <region>, \'quantity\': <quantity>,\n    \'type\': <type>}]\n  licenses_id:\n    description:\n    - Licenses ID\n  force:\n    description:\n    - if \'true\' allows to delete "ACTIVE" licenses if it\'s needed\n    default: false\nrequirements:\n  - python-selvpcclient\nnote:\n    - For operations where \'project_id\' is needed you can use \'project_name\'\n    instead\n'
EXAMPLES = '\n# Describe state with 2 licenses in ru-1 region and 1 in ru-2\n- selvpc_licenses:\n      project_id: <project id>\n      licenses:\n      - region: ru-1\n        quantity: 2\n        type: <license type>\n      - region: ru-2\n        quantity: 1\n        type: <license type>\n# Delete all licenses\n- selvpc_licenses:\n    project_name: <project name>\n    licenses:\n    - region: ru-1\n      quantity: 0\n      type: <license type>\n    - region: ru-2\n      quantity: 0\n      type: <license type>\n    force: True\n# Delete specific licenses\n- selvpc_licenses:\n    state: absent\n    license_id: <license id>\n# Get info about all licenses\n- selvpc_licenses:\n    list: True\n# Get info about specific license\n- selvpc_licenses:\n    license_id: <licenses id>\n'

def _check_license_exists(client, license_id):
    try:
        client.licenses.show(license_id)
    except Exception:
        return False

    return True


def _system_state_change(module, client):
    state = module.params.get('state')
    if state == 'absent':
        license_id = module.params.get('license_id')
        if license_id:
            return _check_license_exists(client, license_id)
    if state == 'present':
        licenses = module.params.get('licenses')
        project_name = module.params.get('project_name')
        project_id = module.params.get('project_id')
        force = module.params.get('force')
        if not c._check_valid_quantity(licenses):
            return False
        if (project_name or project_id) and licenses:
            if not project_id:
                project = c.get_project_by_name(client, project_name)
                if not project:
                    return False
                project_id = project.id
            parsed_subnets = lic.parse_licenses_to_add(licenses)
            actual_subnets = lic.get_project_licenses_quantity(client, project_id)
            to_add, to_del = c.compare_existed_and_needed_objects(actual_subnets, parsed_subnets, force)
            if to_add or to_del:
                return True
            return False
    return False


def main():
    module = AnsibleModule(argument_spec=dict(state=dict(choices=['present', 'absent'], default='present'), token=dict(type='str', no_log=True), list=dict(type='bool', default=False), project_name=dict(type='str'), project_id=dict(type='str'), licenses=dict(type='list'), license_id=dict(type='str'), detailed=dict(type='bool', default=False), force=dict(type='bool', default=False)), supports_check_mode=True)
    project_id = module.params.get('project_id')
    state = module.params.get('state')
    show_list = module.params.get('list')
    licenses = module.params.get('licenses')
    license_id = module.params.get('license_id')
    detailed = module.params.get('detailed')
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
    if state == 'absent' and license_id:
        lic.delete_license(module, client, license_id)
    if state == 'present':
        if licenses and (project_id or project_name):
            lic.add_licenses(module, client, project_id, project_name, licenses, force)
        if license_id and not show_list or show_list:
            lic.get_licenses(module, client, license_id, detailed, show_list=show_list)
    module.fail_json(msg="No params for 'licenses' operations.")


if __name__ == '__main__':
    main()