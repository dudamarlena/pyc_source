# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/x0ox/Dropbox/ActiveDev/yac/yac/lib/vpc.py
# Compiled at: 2017-11-16 20:28:41
import os, json, jmespath, boto3
from botocore.exceptions import ClientError
from yac.lib.paths import get_config_path
from yac.lib.registry import set_remote_string_w_challenge, get_remote_value, get_registry_keys
from yac.lib.registry import set_local_value, get_local_value, clear_entry_w_challenge
from yac.lib.validator import validate_dictionary
from yac.lib.file_converter import convert_local_files, find_and_delete_remotes
from yac.lib.variables import get_variable, set_variable
from yac.lib.file import get_file_contents, create_customization_file, get_file_reg_key
from yac.lib.naming import validate_namer_script
from yac.lib.inputs import validate_inputs_script
YAC_VPC_SUFFIX = '-vpc'
REQUIRED_FIELDS = [
 'prefs-name.value',
 'vpc-params']
SUPPORTED_KEYS = [
 'prefs-repo',
 'prefs-name',
 'vpc-inputs',
 'vpc-params',
 'resource-namer',
 'service-inputs',
 'service-templates']

def validate_vpc_prefs(vpc_prefs, prefs_path=''):
    prefs_errors = validate_dictionary(vpc_prefs, SUPPORTED_KEYS, REQUIRED_FIELDS)
    namer_script = get_variable(vpc_prefs, 'resource-namer', '')
    if namer_script:
        namer_errors = validate_namer_script(namer_script, prefs_path)
        prefs_errors.update(namer_errors)
    if 'service-inputs' in vpc_prefs:
        inputs_script = get_variable(vpc_prefs, 'service-inputs', '')
        if inputs_script:
            inputs_errors = validate_inputs_script(inputs_script, prefs_path)
            prefs_errors.update(inputs_errors)
    return prefs_errors


def get_vpc_prefs():
    vpc_preferences = get_local_value('vpc_preferences')
    return vpc_preferences


def set_vpc_prefs(vpc_prefs):
    if vpc_prefs:
        set_local_value('vpc_preferences', vpc_prefs)


def clear_vpc_prefs():
    set_local_value('vpc_preferences', {})


def register_vpc_prefs(vpc_prefs_key, vpc_prefs_file, challenge):
    with open(vpc_prefs_file) as (vpc_prefs_file_fp):
        vpc_preferences_str = vpc_prefs_file_fp.read()
        vpc_prefs_file_path = os.path.dirname(vpc_prefs_file)
        updated_vpc_preferences_str = convert_local_files(vpc_prefs_key, vpc_preferences_str, vpc_prefs_file_path, challenge)
        vpc_prefs_registry_key = vpc_prefs_key + YAC_VPC_SUFFIX
        set_remote_string_w_challenge(vpc_prefs_registry_key, updated_vpc_preferences_str, challenge)


def clear_vpc_prefs_from_registry(vpc_prefs_name, challenge):
    vpc_prefs = get_vpc_prefs_from_registry(vpc_prefs_name)
    if vpc_prefs:
        vpc_prefs_registry_key = vpc_prefs_name + YAC_VPC_SUFFIX
        clear_entry_w_challenge(vpc_prefs_registry_key, challenge)
        find_and_delete_remotes(vpc_prefs, challenge)


def get_vpc_prefs_from_file(prefs_file_path):
    vpc_prefs = {}
    vpc_prefs_name = ''
    with open(prefs_file_path) as (vpc_prefs_file_fp):
        vpc_prefs = json.load(vpc_prefs_file_fp)
    return vpc_prefs


def get_vpc_prefs_from_registry(vpc_def_registry_key):
    vpc_prefs = {}
    if vpc_def_registry_key:
        vpc_prefs_str = get_remote_value('%s-vpc' % vpc_def_registry_key)
        if vpc_prefs_str:
            vpc_prefs = json.loads(vpc_prefs_str)
            vpc_inputs_yac_path = get_variable(vpc_prefs, 'service-inputs', '')
            print 'inputs path: %s' % vpc_inputs_yac_path
            if vpc_inputs_yac_path:
                inputs_file_local_path = create_customization_file(vpc_inputs_yac_path)
                vpc_prefs['service-inputs']['value'] = inputs_file_local_path
            vpc_namer_yac_path = get_variable(vpc_prefs, 'resource-namer', '')
            if vpc_namer_yac_path:
                namer_file_local_path = create_customization_file(vpc_namer_yac_path)
                set_variable(vpc_prefs, 'resource-namer', namer_file_local_path)
    return vpc_prefs


def get_all_vpc_def_keys():
    vpc_prefs = []
    registry_keys = get_registry_keys()
    for key in registry_keys:
        if '-vpc' in key:
            vpc_prefs = vpc_prefs + [key.replace('-vpc', '')]

    return vpc_prefs


def get_vpc_prefs_from_local_file(vpc_prefs_file):
    vpc_prefs = get_vpc_prefs_from_file(vpc_prefs_file)
    vpc_prefs_name = get_variable(vpc_prefs, 'prefs-name', '')
    prefs_path = os.path.dirname(vpc_prefs_file)
    vpc_inputs_script_path = get_variable(vpc_prefs, 'service-inputs', '')
    if vpc_inputs_script_path:
        yac_file_key = get_file_reg_key(vpc_inputs_script_path, vpc_prefs_name)
        prefs_file_contents = get_file_contents(os.path.join(prefs_path, vpc_inputs_script_path))
        inputs_file_yac_path = create_customization_file(yac_file_key, prefs_file_contents)
        vpc_prefs['service-inputs']['value'] = inputs_file_yac_path
    vpc_namer = get_variable(vpc_prefs, 'resource-namer', '')
    if vpc_namer:
        yac_file_key = get_file_reg_key(vpc_namer, vpc_prefs_name)
        namer_contents = get_file_contents(os.path.join(prefs_path, vpc_namer))
        namer_file_yac_path = create_customization_file(yac_file_key, namer_contents)
        set_variable(vpc_prefs, 'resource-namer', namer_file_yac_path)
    return vpc_prefs


def set_dmz_subnets(vpc_id):
    env = get_variable(params, 'env')
    stack_name = get_stack_name(params)
    subnet_ids = []
    if not stack_exists(stack_name):
        dmz_subnets_prefs = get_variable('dmz-subnet-ids')
        if not dmz_subnets_prefs:
            subnet_ids = subnets_wizard()
        else:
            subnet_ids = vpcs_per_prefs
    else:
        subnet_ids = get_stack_private_subnets(params)
    return vpc


def _get_availability_zones(params):
    azs = {}
    env = get_variable(params, 'env')
    stack_name = get_stack_name(params)
    if not stack_exists(stack_name):
        availabilty_zones = get_variable(params, 'availability-zones', [])
        azs_per_prefs = get_variable(params, 'vpc-id')
        if not vpcs_per_prefs:
            azs = get_vpc_wizard()
        else:
            azs = vpcs_per_prefs
    else:
        azs = get_stack_vpc(params)
    return azs