# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/deploy/library/ec2_vpc_net_custom.py
# Compiled at: 2017-04-06 07:19:28
# Size of source mod 2**32: 10134 bytes
DOCUMENTATION = '\n---\nmodule: ec2_vpc_net\nshort_description: Configure AWS virtual private clouds\ndescription:\n    - Create or terminate AWS virtual private clouds.  This module has a dependency on python-boto.\nversion_added: "2.0"\nauthor: Jonathan Davila (@defionscode)\noptions:\n  name:\n    description:\n      - The name to give your VPC. This is used in combination with the cidr_block parameter to determine if a VPC already exists.\n    required: yes\n  cidr_block:\n    description:\n      - The CIDR of the VPC\n    required: yes\n  tenancy:\n    description:\n      - Whether to be default or dedicated tenancy. This cannot be changed after the VPC has been created.\n    required: false\n    default: default\n    choices: [ \'default\', \'dedicated\' ]\n  dns_support:\n    description:\n      - Whether to enable AWS DNS support.\n    required: false\n    default: yes\n    choices: [ \'yes\', \'no\' ]\n  dns_hostnames:\n    description:\n      - Whether to enable AWS hostname support.\n    required: false\n    default: yes\n    choices: [ \'yes\', \'no\' ]\n  dhcp_opts_id:\n    description:\n      - the id of the DHCP options to use for this vpc\n    default: null\n    required: false\n  tags:\n    description:\n      - The tags you want attached to the VPC. This is independent of the name value, note if you pass a \'Name\' key it would override the Name of the VPC if it\'s different.\n    default: None\n    required: false\n    aliases: [ \'resource_tags\' ]\n  state:\n    description:\n      - The state of the VPC. Either absent or present.\n    default: present\n    required: false\n    choices: [ \'present\', \'absent\' ]\n  multi_ok:\n    description:\n      - By default the module will not create another VPC if there is another VPC with the same name and CIDR block. Specify this as true if you want duplicate VPCs created.\n    default: false\n    required: false\n\nextends_documentation_fragment:\n    - aws\n    - ec2\n'
EXAMPLES = '\n# Note: These examples do not set authentication details, see the AWS Guide for details.\n\n# Create a VPC with dedicate tenancy and a couple of tags\n\n- ec2_vpc_net:\n    name: Module_dev2\n    cidr_block: 10.10.0.0/16\n    region: us-east-1\n    tags:\n      module: ec2_vpc_net\n      this: works\n    tenancy: dedicated\n\n'
try:
    import boto, boto.ec2, boto.vpc
    from boto.exception import BotoServerError
    HAS_BOTO = True
except ImportError:
    HAS_BOTO = False

def boto_exception(err):
    """generic error message handler"""
    if hasattr(err, 'error_message'):
        error = err.error_message
    else:
        if hasattr(err, 'message'):
            error = err.message
        else:
            error = '%s: %s' % (Exception, err)
    return error


def vpc_exists(module, vpc, name, cidr_block, multi):
    """Returns True or False in regards to the existence of a VPC. When supplied
    with a CIDR, it will check for matching tags to determine if it is a match
    otherwise it will assume the VPC does not exist and thus return false.
    """
    matched_vpc = None
    try:
        matching_vpcs = vpc.get_all_vpcs(filters={'tag:Name': name,  'cidr-block': cidr_block})
    except Exception as e:
        e_msg = boto_exception(e)
        module.fail_json(msg=e_msg)

    if len(matching_vpcs) == 1:
        matched_vpc = matching_vpcs[0]
    elif len(matching_vpcs) > 1:
        if multi:
            module.fail_json(msg='Currently there are %d VPCs that have the same name and CIDR block you specified. If you would like to create the VPC anyway please pass True to the multi_ok param.' % len(matching_vpcs))
    return matched_vpc


def update_vpc_tags(vpc, module, vpc_obj, tags, name):
    if tags is None:
        tags = dict()
    tags.update({'Name': name})
    try:
        current_tags = dict((t.name, t.value) for t in vpc.get_all_tags(filters={'resource-id': vpc_obj.id}))
        if tags != current_tags:
            if not module.check_mode:
                vpc.create_tags(vpc_obj.id, tags)
            return True
        else:
            return False
    except Exception as e:
        e_msg = boto_exception(e)
        module.fail_json(msg=e_msg)


def update_dhcp_opts(connection, module, vpc_obj, dhcp_id):
    if vpc_obj.dhcp_options_id != dhcp_id:
        if not module.check_mode:
            connection.associate_dhcp_options(dhcp_id, vpc_obj.id)
        return True
    else:
        return False


def get_vpc_values(vpc_obj):
    if vpc_obj is not None:
        vpc_values = vpc_obj.__dict__
        if 'region' in vpc_values:
            vpc_values.pop('region')
        if 'item' in vpc_values:
            vpc_values.pop('item')
        if 'connection' in vpc_values:
            vpc_values.pop('connection')
        return vpc_values
    else:
        return


def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(name=dict(type='str', default=None, required=True), cidr_block=dict(type='str', default=None, required=True), tenancy=dict(choices=['default', 'dedicated'], default='default'), dns_support=dict(type='bool', default=True), dns_hostnames=dict(type='bool', default=True), dhcp_opts_id=dict(type='str', default=None, required=False), tags=dict(type='dict', required=False, default=None, aliases=['resource_tags']), state=dict(choices=['present', 'absent'], default='present'), multi_ok=dict(type='bool', default=False)))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    if not HAS_BOTO:
        module.fail_json(msg='boto is required for this module')
    name = module.params.get('name')
    cidr_block = module.params.get('cidr_block')
    tenancy = module.params.get('tenancy')
    dns_support = module.params.get('dns_support')
    dns_hostnames = module.params.get('dns_hostnames')
    dhcp_id = module.params.get('dhcp_opts_id')
    tags = module.params.get('tags')
    state = module.params.get('state')
    multi = module.params.get('multi_ok')
    changed = False
    region, ec2_url, aws_connect_params = get_aws_connection_info(module)
    if region:
        try:
            connection = connect_to_aws(boto.vpc, region, **aws_connect_params)
        except (boto.exception.NoAuthHandlerFound, AnsibleAWSError) as e:
            module.fail_json(msg=str(e))

    else:
        module.fail_json(msg='region must be specified')
    if dns_hostnames:
        if not dns_support:
            module.fail_json('In order to enable DNS Hostnames you must also enable DNS support')
    if state == 'present':
        vpc_obj = vpc_exists(module, connection, name, cidr_block, multi)
        if vpc_obj is None:
            try:
                changed = True
                if not module.check_mode:
                    vpc_obj = connection.create_vpc(cidr_block, instance_tenancy=tenancy)
                else:
                    module.exit_json(changed=changed)
            except BotoServerError as e:
                module.fail_json(msg=e)

        if dhcp_id is not None:
            try:
                if update_dhcp_opts(connection, module, vpc_obj, dhcp_id):
                    changed = True
            except BotoServerError as e:
                module.fail_json(msg=e)

        if tags is not None or name is not None:
            try:
                if update_vpc_tags(connection, module, vpc_obj, tags, name):
                    changed = True
            except BotoServerError as e:
                module.fail_json(msg=e)

        try:
            if not module.check_mode:
                connection.modify_vpc_attribute(vpc_obj.id, enable_dns_support=dns_support)
                connection.modify_vpc_attribute(vpc_obj.id, enable_dns_hostnames=dns_hostnames)
        except BotoServerError as e:
            e_msg = boto_exception(e)
            module.fail_json(msg=e_msg)

        if not module.check_mode:
            try:
                vpc_obj = connection.get_all_vpcs(vpc_obj.id)[0]
            except BotoServerError as e:
                e_msg = boto_exception(e)
                module.fail_json(msg=e_msg)

        module.exit_json(changed=changed, vpc=get_vpc_values(vpc_obj))
    elif state == 'absent':
        vpc_obj = vpc_exists(module, connection, name, cidr_block, multi)
        if vpc_obj is not None:
            try:
                if not module.check_mode:
                    connection.delete_vpc(vpc_obj.id)
                vpc_obj = None
                changed = True
            except BotoServerError as e:
                e_msg = boto_exception(e)
                module.fail_json(msg='%s. You may want to use the ec2_vpc_subnet, ec2_vpc_igw, and/or ec2_vpc_route_table modules to ensure the other components are absent.' % e_msg)

        module.exit_json(changed=changed, vpc=get_vpc_values(vpc_obj))


from ansible.module_utils.basic import *
from ansible.module_utils.ec2 import *
if __name__ == '__main__':
    main()