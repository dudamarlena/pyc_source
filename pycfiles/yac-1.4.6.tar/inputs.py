# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/x0ox/Dropbox/ActiveDev/yac/yac/lib/inputs.py
# Compiled at: 2018-01-04 15:04:07
import boto3, jmespath, sys, json, requests, os, imp
from sets import Set
from yac.lib.variables import get_variable, set_variable
from yac.lib.naming import get_stack_name
from yac.lib.stack import stack_exists, get_asg_subnet_ids, get_stack_param_value
from yac.lib.stack import get_stack_vpc, get_stack_ssh_keys
USER_INPUTS_PARAM_KEY = 'UserInputs'

def get_inputs(params, inputs_key='service-inputs', these_input_keys=[]):
    user_inputs = {}
    parameter_mapping = {}
    if inputs_key in params and 'inputs' in params[inputs_key]:
        service_param = params[inputs_key]['inputs']
        for param_key in service_param:
            if not these_input_keys or these_input_keys and param_key in these_input_keys:
                value, user_prompted = handle_service_input(params, service_param[param_key], param_key)
                if user_prompted:
                    set_variable(user_inputs, param_key, value, service_param[param_key]['help'])
                if 'param' in service_param[param_key]:
                    this_mapping = service_param[param_key]['param']
                    this_mapping['value'] = value
                    parameter_mapping[param_key] = this_mapping

    if inputs_key in params and 'conditional-inputs' in params[inputs_key]:
        conditional_params = params[inputs_key]['conditional-inputs']
        for param_key in conditional_params:
            if not these_input_keys or these_input_keys and param_key in these_input_keys:
                value = ''
                if 'input' in conditional_params[param_key]['condition']:
                    conditional_input = conditional_params[param_key]['condition']['input']
                    conditional_value = ''
                    if 'value' in conditional_params[param_key]['condition']:
                        conditional_value = conditional_params[param_key]['condition']['value']
                    conditional_setting = get_variable(params, conditional_input, '')
                elif 'fxn' in conditional_params[param_key]['condition']:
                    conditional_fxn = str(conditional_params[param_key]['condition']['fxn'])
                    conditional_value = ''
                    if 'value' in conditional_params[param_key]['condition']:
                        conditional_value = conditional_params[param_key]['condition']['value']
                    conditional_setting = eval(conditional_fxn)(params)
                if 'value' not in conditional_params[param_key]['condition'] or conditional_value == conditional_setting:
                    value, user_prompted = handle_service_input(params, conditional_params[param_key], param_key)
                    if user_prompted:
                        set_variable(user_inputs, param_key, value, conditional_params[param_key]['help'])
                if 'param' in conditional_params[param_key]:
                    this_mapping = conditional_params[param_key]['param']
                    this_mapping['value'] = value
                    parameter_mapping[param_key] = this_mapping

    set_variable(params, 'user-inputs', user_inputs)
    set_variable(params, 'param-mapping', parameter_mapping)


def handle_service_input(params, dynamic_param, param_key):
    wizard_arg = ''
    if 'arg' in dynamic_param['wizard_fxn']:
        wizard_arg = dynamic_param['wizard_fxn']['arg']
    options = []
    if 'options' in dynamic_param['constraints']:
        options = dynamic_param['constraints']['options']
    elif 'options_fxn' in dynamic_param['constraints']:
        options_fxn = dynamic_param['constraints']['options_fxn']['name']
        if 'namespace' in dynamic_param['constraints']['options_fxn']:
            name_space = dynamic_param['constraints']['options_fxn']['name_space']
            import_statement = 'from %s import %s' % (name_space, options_fxn)
            exec import_statement
        if 'arg' in dynamic_param['constraints']['options_fxn']:
            options_arg = dynamic_param['constraints']['options_fxn']['arg']
            options = eval(options_fxn)(params, options_arg)
        else:
            options = eval(options_fxn)(params)
    required = True
    if 'required' in dynamic_param['constraints']:
        required = dynamic_param['constraints']['required']
    allow_changes_on_updates = True
    if 'param' in dynamic_param and 'on-updates' in dynamic_param['param'] and dynamic_param['param']['on-updates'] == False:
        allow_changes_on_updates = False
    value, user_prompted = set_service_input(params, param_key, dynamic_param['description'], dynamic_param['help'], dynamic_param['wizard_fxn']['name'], required, options, wizard_arg, allow_changes_on_updates)
    return (
     value, user_prompted)


def set_service_input(params, param_key, param_desc, param_help, wizard_fxn, required, options, wizard_arg, allow_changes_on_updates):
    value = ''
    user_prompted = False
    value = get_variable(params, param_key, 'absolutely-nada')
    if value == 'absolutely-nada':
        stack_name = get_stack_name(params)
        current_setpoint = ''
        if current_setpoint:
            if change_wizard(current_setpoint, param_desc):
                value = eval(wizard_fxn)(param_desc, param_help, options, required, wizard_arg)
        default_value = get_vpc_default(params, param_key)
        if stack_exists(stack_name) and not default_value and allow_changes_on_updates:
            value = get_stack_service_inputs_value(stack_name, param_key)
            if change_wizard(value, param_desc):
                value = eval(wizard_fxn)(param_desc, param_help, options, required, wizard_arg)
                user_prompted = True
        elif not stack_exists(stack_name) and not default_value:
            value = eval(wizard_fxn)(param_desc, param_help, options, required, wizard_arg)
            user_prompted = True
        elif not stack_exists(stack_name) and default_value:
            print 'setting %s to %s per vpc prefs' % (param_key, default_value)
            value = default_value
        elif stack_exists(stack_name) and default_value:
            print 'keeping %s as %s per vpc prefs' % (param_key, default_value)
            value = default_value
        set_variable(params, param_key, value, param_desc)
    return (value, user_prompted)


def get_variable_or_default(params, param_key):
    value = get_variable(params, param_key)
    if not value:
        vpc_defaults = get_variable(params, 'vpc-defaults', {})
        value = get_variable(vpc_defaults, param_key)
        if value:
            print 'setting %s per vpc default value: %s' % (param_key, value)
            set_variable(params, param_key, value)
    return value


def does_stack_exist(params):
    stack_name = get_stack_name(params)
    return stack_exists(stack_name)


def get_vpc_default(params, param_key):
    vpc_defaults = get_variable(params, 'vpc-defaults', {})
    value = get_variable(vpc_defaults, param_key)
    return value


def get_user_inputs_as_stack_param(service_params):
    stack_parameter = {}
    user_inputs = get_user_inputs(service_params)
    if user_inputs:
        user_inputs_str = json.dumps(user_inputs)
        print user_inputs_str
        stack_parameter['ParameterKey'] = USER_INPUTS_PARAM_KEY
        stack_parameter['ParameterValue'] = user_inputs_str
    return stack_parameter


def get_mapping_as_stack_params(service_params, costing=False):
    stack_parameters = []
    param_mapping = get_variable(service_params, 'param-mapping')
    if param_mapping:
        stack_exists = get_variable(service_params, 'stack-exists', False)
        for param_key in param_mapping:
            if costing or not stack_exists or stack_exists and 'on-updates' not in param_mapping[param_key] or stack_exists and 'on-updates' in param_mapping[param_key] and param_mapping[param_key]['on-updates']:
                stack_parameters = stack_parameters + [
                 {'ParameterKey': param_mapping[param_key]['key'], 'ParameterValue': param_mapping[param_key]['value']}]
            else:
                stack_parameters = stack_parameters + [
                 {'ParameterKey': param_mapping[param_key]['key'], 'UsePreviousValue': True}]

    return stack_parameters


def get_user_inputs(service_params):
    user_inputs = get_variable(service_params, 'user-inputs')
    return user_inputs


def get_user_inputs_from_vpc_prres(service_params):
    user_inputs = {}
    if 'vpc-defaults' in service_params and 'user-inputs' in service_params['vpc-defaults']:
        user_inputs.update(service_params['vpc-defaults']['user-inputs'])
    return user_inputs


def string_wizard(param_desc, help_msg, options, required, str_len=''):
    value = validated_input(param_desc, help_msg, options, string_validation, required, str_len)
    return value


def int_wizard(param_desc, help_msg, options, required, arg=''):
    value = validated_input(param_desc, help_msg, options, int_validation, required)
    return value


def bool_wizard(param_desc, help_msg, options, required, arg=''):
    value = validated_input(param_desc, help_msg, [
     'True', 'False'], bool_validation, required)
    return value == 'True'


def array_wizard(param_desc, help_msg, options, required, layer=''):
    value = validated_array_input(param_desc, help_msg, options, array_validation, required)
    return value


def path_wizard(param_desc, help_msg, options, required, str_len=''):
    value = validated_input(param_desc, help_msg, options, path_validation, required, str_len)
    return value


def change_wizard(current_value, field_name):
    msg = "Current '%s' value is %s. Do you want to change it? (y/n/<enter>) >> " % (field_name, current_value)
    validation_failed = True
    change = False
    options = [
     'y', 'n', '']
    while validation_failed:
        input = raw_input(msg)
        validation_failed = string_validation(input, options, False)

    if input and input == 'y':
        change = True
    return change


def validated_input(param_desc, help_msg, options, function, required=True, optional_arg=''):
    validation_failed = True
    if required:
        param_msg = '\nThis service requires the following input: %s' % param_desc
    else:
        param_msg = '\nThis service accepts the following optional input: %s' % param_desc
    print param_msg
    print help_msg
    if options:
        if len(options) > 10:
            input = raw_input('Press <enter> to see a list of availble options >> ')
            print 'Choices include: \n%s' % pp_list(options)
        else:
            print 'Choices include: \n%s' % pp_short_list(options)
    while validation_failed:
        if options:
            input_msg = 'Please paste in one of the available options for %s >> ' % param_desc
        else:
            input_msg = 'Please input a value for %s >> ' % param_desc
        input = raw_input(input_msg)
        input = input.strip("'")
        validation_failed = function(input, options, required, optional_arg)

    return input


def validated_array_input(param_desc, help_msg, options, function, required=True, optional_arg=''):
    validation_failed = True
    array_building = True
    if required:
        param_msg = '\nThis service requires the following input: %s' % param_desc
    else:
        param_msg = '\nThis service accepts the following optional input: %s' % param_desc
    print param_msg
    print pp_help(help_msg)
    if options:
        input = raw_input('Press <enter> to see a list of availble options >> ')
        print 'Choices include: \n%s' % pp_list(options)
    print 'Paste in values one at a time and press Enter ( press Enter when done ) ...'
    inputs = []
    while validation_failed:
        input = raw_input("... input an item for '%s' >> " % param_desc)
        if input:
            inputs.append(input)
        else:
            validation_failed, inputs = function(inputs, options, required, optional_arg)

    return inputs


def validated_array_input_old(param_desc, retry_msg, options, function):
    validation_failed = True
    array_building = True
    print 'enter values one at a time, cr when done ...'
    inputs = []
    while validation_failed:
        input = raw_input(param_desc).strip("'")
        if input:
            inputs.append(input)
        else:
            validation_failed, inputs = function(inputs, options, retry_msg)


def string_validation(input, options, required, max_strlen=4000):
    validation_failed = False
    if options:
        if type(options[0]) == dict:
            options = jmespath.search('[*].Option', options)
        if input not in options:
            validation_failed = True
            retry_msg = 'Input invalid - please select from the available options'
    if max_strlen:
        if len(input) > max_strlen:
            validation_failed = True
            retry_msg = 'Input invalid (too long) - please input a string with <= %s chars' % max_strlen
    if required and not input:
        validation_failed = True
        retry_msg = 'Input required - please enter a value'
    if validation_failed:
        print retry_msg
    return validation_failed


def path_validation(input, options, required, max_strlen=4000):
    validation_failed = False
    if options:
        if type(options[0]) == dict:
            options = jmespath.search('[*].Option', options)
        if input not in options:
            validation_failed = True
            retry_msg = 'Input invalid - please select from the available options'
    if max_strlen:
        if len(input) > max_strlen:
            validation_failed = True
            retry_msg = 'Input invalid (too long) - please input a string with <= %s chars' % max_strlen
    if required and not input:
        validation_failed = True
        retry_msg = 'Input required - please enter a value'
    if not os.path.exists(input):
        validation_failed = True
        retry_msg = 'Invalid path - please try again'
    if validation_failed:
        print retry_msg
    return validation_failed


def int_validation(input, options, required, max_value=sys.maxint):
    validation_failed = False
    if options:
        if input not in options:
            validation_failed = True
            retry_msg = 'Input invalid - please select from the available options'
    if max_value:
        if input > max_value:
            validation_failed = True
            retry_msg = 'Input invalid - please input an int <= %s' % max_value
    if required and not input:
        validation_failed = True
        retry_msg = 'Input required - please enter a value'
    if input and not input.isdigit():
        validation_failed = True
        retry_msg = 'Input invalid - integers only'
    if validation_failed:
        print retry_msg
    return validation_failed


def bool_validation(input, options, required, optional_arg=''):
    validation_failed = input not in ('True', 'False')
    if required and not input:
        retry_msg = 'Input required - please enter a value'
    elif validation_failed:
        retry_msg = 'Input invalid - True/False only'
    if validation_failed:
        print retry_msg
    return validation_failed


def input_validation(input, options, required, retry_msg):
    validation_failed = input not in options
    if validation_failed:
        print retry_msg
    return validation_failed


def array_validation(inputs, options, required, arg=''):
    validation_failed = len(Set(inputs) & Set(options)) != len(inputs)
    if validation_failed:
        retry_msg = 'Input invalid - please select from the available options'
        print retry_msg
        inputs = []
    return (validation_failed, inputs)


def get_vpc_ids(params):
    ec2 = boto3.client('ec2')
    vpcs = ec2.describe_vpcs()
    vpc_ids = jmespath.search('Vpcs[*].VpcId', vpcs)
    return vpc_ids


def get_s3_buckets(params):
    s3 = boto3.client('s3')
    buckets = s3.list_buckets()
    bucket_names = jmespath.search('Buckets[*].Name', buckets)
    return bucket_names


def get_sns_topic_arns(params):
    s3 = boto3.client('sns')
    topics = s3.list_topics()
    topics_arns = jmespath.search('Topics[*].TopicArn', topics)
    return topics_arns


def get_key_pairs(params):
    s3 = boto3.client('iam')
    public_keys = s3.list_ssh_public_keys()
    key_names = jmespath.search('SSHPublicKeys[*].SSHPublicKeyId', public_keys)
    return key_names


def get_ssl_certs(params):
    iam = boto3.client('iam')
    certs = iam.list_server_certificates()
    cert_name = jmespath.search('ServerCertificateMetadataList[*].ServerCertificateName', certs)
    return cert_name


def get_iam_roles(params):
    iam = boto3.client('iam')
    profiles = iam.list_instance_profiles()
    profile_ids = jmespath.search('InstanceProfiles[*].InstanceProfileId', profiles)
    return profile_ids


def get_snapshot_ids(params, name_search_string):
    iam = boto3.client('rds')
    filters = [{'Name': 'tag:Name', 'Values': [name_search_string]}]
    snapshots = iam.describe_db_snapshots(Filters=filters)
    snapshots_ids = jmespath.search('DBSnapshots[*].DBSnapshotIdentifier', snapshots)
    return snapshots_ids


def get_azs(params):
    ec2 = boto3.client('ec2')
    azs = ec2.describe_availability_zones(Filters=[{'Name': 'state', 'Values': ['available']}])
    az_names = jmespath.search('AvailabilityZones[*].ZoneName', azs)
    return az_names


def get_coreos_ami(params):
    ec2 = boto3.client('ec2')
    images = ec2.describe_images(Filters=[{'Name': 'name', 'Values': ['CoreOS-stable*hvm']}, {'Name': 'owner-id', 'Values': ['595879546273']}])
    image_ids = jmespath.search('Images[*].{Option: ImageId, Description: Name}', images)
    return image_ids


def get_subnet_ids(params):
    vpc_id = get_variable(params, 'vpc-id')
    availabilty_zones = get_variable(params, 'availability-zones')
    ec2 = boto3.client('ec2')
    subnets = ec2.describe_subnets(Filters=[
     {'Name': 'vpc-id', 
        'Values': [
                 vpc_id]},
     {'Name': 'availability-zone', 
        'Values': availabilty_zones}])
    subnet_ids = jmespath.search('Subnets[*].SubnetId', subnets)
    return subnet_ids


def get_db_subnet_group_ids(params):
    vpc_id = get_variable(params, 'vpc-id')
    rds = boto3.client('rds')
    subnets = rds.describe_db_subnet_groups()
    db_subnet_group_ids = jmespath.search("DBSubnetGroups[?VpcId=='%s'].DBSubnetGroupName" % vpc_id, subnets)
    return db_subnet_group_ids


def get_image_versions(image_name, registry_url='https://registry.hub.docker.com'):
    endpoint_uri = '/v2/repositories/%s/tags' % image_name
    endpoint_response = requests.get(registry_url + endpoint_uri)
    versions = jmespath.search('results[*].name', endpoint_response.json())
    return versions


def get_stack_service_inputs(stack_name):
    decoded_dict = {}
    stack_param_key = USER_INPUTS_PARAM_KEY
    param_value = get_stack_param_value(stack_name, stack_param_key)
    if param_value:
        decoded_dict = json.loads(param_value)
    return decoded_dict


def get_stack_service_inputs_value(stack_name, yac_param_key):
    yac_param_value = ''
    stack_param_key = USER_INPUTS_PARAM_KEY
    param_value = get_stack_param_value(stack_name, stack_param_key)
    if param_value:
        decoded_dict = json.loads(param_value)
        if yac_param_key in decoded_dict:
            yac_param_value = get_variable(decoded_dict, yac_param_key)
    return yac_param_value


def pp_list(list):
    str = ''
    for item in list:
        str = str + '* %s\n' % item

    return str


def pp_short_list(list):
    str = ''
    for item in list:
        str = str + ' %s' % item

    return '( %s )' % str


def pp_help(help):
    if type(help) == list:
        ret = pp_list(help)
    else:
        ret = str(help)
    return ret


def validate_inputs_script(inputs_script, prefs_path):
    script_path = os.path.join(prefs_path, inputs_script)
    val_errors = {}
    if os.path.exists(script_path):
        naming_module = imp.load_source('yac.lib', script_path)
        if 'get_value' not in dir(naming_module):
            val_errors.update({'inputs-script': 'inputs script %s lacks the get_value fxn' % inputs_script})
    else:
        val_errors = {'inputs-script': "inputs script %s doesn't exist" % inputs_script}
    return val_errors