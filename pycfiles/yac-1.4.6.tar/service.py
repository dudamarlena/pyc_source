# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/x0ox/Dropbox/ActiveDev/yac/yac/lib/service.py
# Compiled at: 2018-01-05 13:50:32
import os, json, jmespath, copy
from sets import Set
from yac.lib.registry import get_registry_keys, get_remote_value, clear_entry_w_challenge
from yac.lib.registry import set_remote_string_w_challenge
from yac.lib.file import get_file_contents, register_file, get_file_abs_path
from yac.lib.file_converter import convert_local_files, find_and_delete_remotes
from yac.lib.variables import get_variable, set_variable
from yac.lib.intrinsic import apply_custom_fxn
from yac.lib.vpc import get_vpc_prefs
from yac.lib.validator import validate_dictionary
from yac.lib.stack import get_stack_name, stack_exists
from yac.lib.inputs import get_inputs, get_user_inputs
from yac.lib.cache import get_cache_value, set_cache_value_dt
from yac.lib.secrets import load_secrets
PARAMS_CACHE_SUFFIX = 'params'
NULL_SERVICE = 'servicefile does not exist'
REQUIRED_FIELDS = [
 'service-name.value',
 'default-alias.value',
 'service-description.summary',
 'service-description.details',
 'service-description.maintainer.name',
 'service-description.maintainer.email']
MERGEABLE_FIELDS = [
 'service-inputs',
 'deploy-for-boot',
 'service-params',
 'service-secrets',
 'stack-template',
 'tasks']
SUPPORTED_KEYS = [
 'service-name',
 'service-version',
 'service-inputs',
 'default-alias',
 'service-description',
 'services-consumed',
 'resource-namer',
 'deploy-for-boot',
 'service-params',
 'service-secrets',
 'inputs-function',
 'post-function',
 'resource-function',
 'stack-template',
 'tasks']
YAC_SERVICE_SUFFIX = '-service'

class ServiceError:

    def __init__(self, msg):
        self.msg = msg


def validate_service(service_descriptor, servicefile_path):
    val_errors = validate_dictionary(service_descriptor, SUPPORTED_KEYS, REQUIRED_FIELDS)
    if 'services-consumed' in service_descriptor and 'services' in service_descriptor['services-consumed']:
        for service_key in service_descriptor['services-consumed']['services']:
            sub_service_name = get_variable(service_descriptor['services-consumed']['services'], service_key)
            sub_service_comment = service_descriptor['services-consumed']['services'][service_key]['comment']
            sub_service_descriptor, sub_name_found, b = get_service(sub_service_name, servicefile_path)
            if sub_name_found == NULL_SERVICE:
                val_errors['missing sub'] = "the '%s' services from %s does not exist locally or in registry." % (sub_service_comment, sub_service_name)
            else:
                sub_service_errors = validate_dictionary(sub_service_descriptor, SUPPORTED_KEYS, REQUIRED_FIELDS)
                val_errors.update(sub_service_errors)

    return val_errors


def get_all_service_names(search_str=''):
    service_names = []
    registry_keys = get_registry_keys()
    for key in registry_keys:
        if key.endswith(YAC_SERVICE_SUFFIX) and (not search_str or search_str in key):
            service_names = service_names + [key.replace(YAC_SERVICE_SUFFIX, '')]

    return service_names


def get_service(servicefile_arg, servicefile_path=''):
    this_service_descriptor, service_name, servicefile_path = get_service_from_file(servicefile_arg, servicefile_path)
    if service_name == NULL_SERVICE:
        if is_service_name_complete(servicefile_arg):
            service_name = servicefile_arg
        elif is_service_available_partial_name(servicefile_arg):
            service_name = get_complete_name(servicefile_arg)
        this_service_descriptor, service_name = get_service_by_name(service_name)
    if 'services-consumed' in this_service_descriptor and 'services' in this_service_descriptor['services-consumed']:
        aggregated_service_descriptor = {}
        init_mergeable_fields(aggregated_service_descriptor)
        for service_key in this_service_descriptor['services-consumed']['services']:
            sub_service_name = get_variable(this_service_descriptor['services-consumed']['services'], service_key)
            sub_service_comment = this_service_descriptor['services-consumed']['services'][service_key]['comment']
            print "adding '%s' services from %s ..." % (sub_service_comment, sub_service_name)
            sub_service_descriptor, a, b = get_service(sub_service_name, servicefile_path)
            merge_service_descriptor(aggregated_service_descriptor, sub_service_descriptor)

        merge_service_descriptor(aggregated_service_descriptor, this_service_descriptor)
        swap_service_identity(aggregated_service_descriptor, this_service_descriptor)
        return (
         aggregated_service_descriptor, service_name, servicefile_path)
    else:
        return (this_service_descriptor, service_name, servicefile_path)


def swap_service_identity(dest_service_descriptor, src_service_descriptor):
    supported_keys = set(SUPPORTED_KEYS)
    mergeable_keys = set(MERGEABLE_FIELDS)
    identity_keys = supported_keys - mergeable_keys
    for identify_key in identity_keys:
        if identify_key in src_service_descriptor:
            dest_service_descriptor[identify_key] = src_service_descriptor[identify_key]

    if 'service-inputs' in src_service_descriptor and 'value' in src_service_descriptor['service-inputs']:
        dest_service_descriptor['service-inputs']['value'] = src_service_descriptor['service-inputs']['value']


def merge_service_descriptor(service_descriptor, sub_service_descriptor):
    service_descriptor['service-inputs']['inputs'].update(sub_service_descriptor['service-inputs']['inputs'])
    service_descriptor['service-inputs']['conditional-inputs'].update(sub_service_descriptor['service-inputs']['conditional-inputs'])
    service_descriptor['service-params'].update(sub_service_descriptor['service-params'])
    service_descriptor['service-secrets']['secrets'].update(sub_service_descriptor['service-secrets']['secrets'])
    service_descriptor['stack-template']['Parameters'].update(sub_service_descriptor['stack-template']['Parameters'])
    service_descriptor['stack-template']['Resources'].update(sub_service_descriptor['stack-template']['Resources'])
    service_descriptor['stack-template']['Conditions'].update(sub_service_descriptor['stack-template']['Conditions'])
    tasks = get_variable(service_descriptor, 'tasks', {})
    tasks.update(get_variable(sub_service_descriptor, 'tasks'))
    service_descriptor['deploy-for-boot']['files'] = service_descriptor['deploy-for-boot']['files'] + sub_service_descriptor['deploy-for-boot']['files']
    service_descriptor['deploy-for-boot']['directories'] = service_descriptor['deploy-for-boot']['directories'] + sub_service_descriptor['deploy-for-boot']['directories']


def get_service_from_file(servicefile_arg, servicefile_path=''):
    service_descriptor = {}
    service_name = NULL_SERVICE
    abs_path = ''
    file_contents = get_file_contents(servicefile_arg, servicefile_path)
    if file_contents:
        service_descriptor = json.loads(file_contents)
        service_name = get_variable(service_descriptor, 'service-name')
        abs_path = get_file_abs_path(servicefile_arg, servicefile_path)
    init_mergeable_fields(service_descriptor)
    return (
     service_descriptor, service_name, abs_path)


def get_service_by_name(service_name):
    service_descriptor = {}
    if service_name:
        reg_key = service_name + YAC_SERVICE_SUFFIX
        service_contents = get_remote_value(reg_key)
        if service_contents:
            service_descriptor = json.loads(service_contents)
        else:
            service_name = NULL_SERVICE
    init_mergeable_fields(service_descriptor)
    return (
     service_descriptor, service_name)


def init_mergeable_fields(service_descriptor):
    if 'service-params' not in service_descriptor:
        service_descriptor['service-params'] = {}
    if 'service-secrets' not in service_descriptor:
        service_descriptor['service-secrets'] = {'secrets': {}}
    if 'tasks' not in service_descriptor:
        service_descriptor['tasks'] = {'value': {}}
    if 'deploy-for-boot' not in service_descriptor:
        service_descriptor['deploy-for-boot'] = {'files': [], 'directories': []}
    elif 'deploy-for-boot' in service_descriptor and 'directories' not in service_descriptor['deploy-for-boot']:
        service_descriptor['deploy-for-boot']['directories'] = []
    elif 'deploy-for-boot' in service_descriptor and 'files' not in service_descriptor['deploy-for-boot']:
        service_descriptor['deploy-for-boot']['files'] = []
    if 'service-inputs' not in service_descriptor:
        service_descriptor['service-inputs'] = {'inputs': {}, 'conditional-inputs': {}}
    elif 'service-inputs' in service_descriptor and 'conditional-inputs' not in service_descriptor['service-inputs']:
        service_descriptor['service-inputs']['conditional-inputs'] = {}
    elif 'service-inputs' in service_descriptor and 'inputs' not in service_descriptor['service-inputs']:
        service_descriptor['service-inputs']['inputs'] = {}
    if 'stack-template' not in service_descriptor:
        service_descriptor['stack-template'] = {}
    if 'Parameters' not in service_descriptor['stack-template']:
        service_descriptor['stack-template']['Parameters'] = {}
    if 'Resources' not in service_descriptor['stack-template']:
        service_descriptor['stack-template']['Resources'] = {}
    if 'Conditions' not in service_descriptor['stack-template']:
        service_descriptor['stack-template']['Conditions'] = {}


def clear_service(service_name, challenge):
    service_descriptor, service_name_returned = get_service_by_name(service_name)
    if service_descriptor:
        reg_key = service_name + YAC_SERVICE_SUFFIX
        clear_entry_w_challenge(reg_key, challenge)
        find_and_delete_remotes(service_descriptor, challenge)
    else:
        raise ServiceError("service with key %s doesn't exist" % service_name)


def register_service(service_name, service_path, challenge):
    if os.path.exists(service_path):
        service_contents_str = get_file_contents(service_path)
        if service_contents_str:
            reg_key = service_name + YAC_SERVICE_SUFFIX
            servicefile_path = os.path.dirname(service_path)
            updated_service_contents_str = convert_local_files(service_name, service_contents_str, servicefile_path, challenge)
            set_remote_string_w_challenge(reg_key, updated_service_contents_str, challenge)
    else:
        raise ServiceError("service path %s doesn't exist" % service_path)


def publish_service_description(service_name, service_path):
    print 'stub for service publication to human-readable docs - not yet implemented'


def is_service_alias(service_alias, vpc_prefs):
    is_alias = False
    if 'aliases' in vpc_prefs and service_alias in vpc_prefs['aliases']:
        is_alias = True
    return is_alias


def get_alias_from_name(complete_service_name):
    alias = ''
    if complete_service_name:
        name_parts = complete_service_name.split(':')
        name_prefix_parts = name_parts[0].split('/')
        alias = name_prefix_parts[(-1)]
    return alias


def get_service_name(service_alias, vpc_prefs):
    server_name = ''
    if 'aliases' in vpc_prefs and service_alias in vpc_prefs['aliases']:
        server_name = vpc_prefs['aliases'][service_alias]
    return server_name


def is_service_name_complete(service_name):
    is_complete = False
    name_parts = service_name.split(':')
    if len(name_parts) == 2:
        is_complete = True
    return is_complete


def is_service_available_partial_name(service_partial_name):
    is_available = False
    if not is_service_name_complete(service_partial_name):
        complete_name_candidate = '%s:%s' % (service_partial_name, 'latest')
        service_desc, service_name = get_service_by_name(complete_name_candidate)
        if service_desc:
            is_available = True
    return is_available


def get_complete_name(service_name):
    complete_name = ''
    if not is_service_name_complete(service_name):
        complete_name_candidate = '%s:%s' % (service_name, 'latest')
        service_desc, service_name = get_service_by_name(complete_name_candidate)
        if service_desc:
            complete_name = complete_name_candidate
    return complete_name


def get_service_alias(service_descriptor, service_alias_arg):
    if service_alias_arg:
        service_alias = service_alias_arg
    else:
        service_alias = get_variable(service_descriptor, 'default-alias')
    return service_alias


def get_service_version(service_descriptor, service_version_arg):
    if service_version_arg:
        service_version = service_version_arg
    elif get_variable(service_descriptor, 'service-version', ''):
        service_version = get_variable(service_descriptor, 'service-version')
    return service_version


def get_service_parmeters(service_alias, service_params_via_cli, service_name, service_descriptor, servicefile_path, vpc_prefs={}):
    service_parmeters = static_service_parmeters(service_alias, service_params_via_cli, service_name, service_descriptor, servicefile_path, vpc_prefs)
    load_service_secrets(service_parmeters, service_descriptor)
    allow_params_cache = get_variable(service_parmeters, 'allow-params-cache', False)
    param_cache_key = '%s:%s' % (service_name, PARAMS_CACHE_SUFFIX)
    if allow_params_cache and get_cache_value(param_cache_key):
        use_cached_inputs = raw_input('\nWant to use inputs from cache?' + '\n(hint: o.w. you will be re-prompted for inputs)' + '\nPlease answer y or n (or <enter>) >> ')
        if use_cached_inputs and use_cached_inputs == 'y':
            service_parmeters = get_cache_value(param_cache_key)
        else:
            dynamic_service_parmeters(service_parmeters, service_descriptor, vpc_prefs)
    else:
        dynamic_service_parmeters(service_parmeters, service_descriptor, vpc_prefs)
        if allow_params_cache:
            set_cache_value_dt(param_cache_key, service_parmeters)
    return service_parmeters


def static_service_parmeters(service_alias, service_params_via_cli, service_name, service_descriptor, servicefile_path, vpc_prefs={}):
    service_parmeters = {}
    if 'vpc-params' in vpc_prefs:
        service_parmeters.update(vpc_prefs['vpc-params'])
    set_variable(service_parmeters, 'service-alias', service_alias)
    set_variable(service_parmeters, 'service-name', service_name)
    set_variable(service_parmeters, 'servicefile-path', servicefile_path)
    if 'service-params' in service_descriptor:
        service_parmeters.update(service_descriptor['service-params'])
    if service_params_via_cli:
        service_parmeters.update(service_params_via_cli)
    services_consumed = get_variable(service_descriptor, 'services-consumed', [])
    set_variable(service_parmeters, 'services-consumed', services_consumed)
    stack_description = service_descriptor['service-description']['summary']
    set_variable(service_parmeters, 'service-description', stack_description)
    if 'service-inputs' in service_descriptor:
        service_parmeters['service-inputs'] = service_descriptor['service-inputs']
    if 'tasks' in service_descriptor:
        service_parmeters['tasks'] = service_descriptor['tasks']
    if 'services-consumed' in service_descriptor and 'sub-descriptors' in service_descriptor['services-consumed']:
        sub_descriptors = get_variable(service_descriptor['services-consumed'], 'sub-descriptors')
        if sub_descriptors:
            sub_keys = sub_descriptors.keys()
            for sub_key in sub_keys:
                sub_descriptor = sub_descriptors[sub_key]
                if 'service-params' in sub_descriptor:
                    print 'loading params from %s' % sub_key
                    service_parmeters.update(sub_descriptor['service-params'])

    return service_parmeters


def load_service_secrets(service_parmeters, service_descriptor):
    if 'service-secrets' in service_descriptor:
        load_secrets(service_parmeters, service_descriptor['service-secrets'])


def dynamic_service_parmeters(service_parmeters, service_descriptor, vpc_prefs={}):
    if 'service-inputs' in vpc_prefs:
        vpc_defaults = service_parmeters.copy()
        vpc_defaults['service-inputs'] = vpc_prefs['service-inputs']
        vpc_inputs_script = get_variable(vpc_prefs, 'service-inputs', '')
        if vpc_inputs_script:
            apply_custom_fxn(vpc_inputs_script, vpc_defaults)
        else:
            get_inputs(vpc_defaults)
        set_variable(service_parmeters, 'vpc-defaults', vpc_defaults)
        service_parmeters.update(get_variable(vpc_defaults, 'user-inputs'))
    if 'service-inputs' in service_descriptor:
        service_input_script = get_variable(service_descriptor, 'inputs-function', '')
        if not service_input_script:
            service_input_script = get_variable(service_descriptor, 'service-inputs', '')
        if service_input_script:
            apply_custom_fxn(service_input_script, service_parmeters)
        else:
            get_inputs(service_parmeters)
    default_vpc_params(service_parmeters)
    stack_name = get_stack_name(service_parmeters)
    set_variable(service_parmeters, 'stack-name', stack_name, 'Name of the service stack')
    set_variable(service_parmeters, 'stack-exists', stack_exists(stack_name), 'Stack exists')


def default_vpc_params(service_parmeters):
    if not get_variable(service_parmeters, 'proxy-port', ''):
        set_variable(service_parmeters, 'proxy-port', '')
    if not get_variable(service_parmeters, 'proxy-cidr', ''):
        set_variable(service_parmeters, 'proxy-cidr', '')
    if not get_variable(service_parmeters, 'corporate-cidr', ''):
        set_variable(service_parmeters, 'corporate-cidr', '')
    if not get_variable(service_parmeters, 'dns-cidr', ''):
        set_variable(service_parmeters, 'dns-cidr', '0.0.0.0/0')
    if not get_variable(service_parmeters, 'ntp-servers', ''):
        set_variable(service_parmeters, 'ntp-servers', '0.pool.ntp.org;1.pool.ntp.org;2.pool.ntp.org;3.pool.ntp.org')