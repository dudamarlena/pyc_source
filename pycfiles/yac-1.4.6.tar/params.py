# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/x0ox/Dropbox/ActiveDev/yac/yac/lib/params.py
# Compiled at: 2018-01-04 15:04:07
import os, json, jmespath, copy
from yac.lib.registry import get_registry_keys, get_remote_value, clear_entry_w_challenge
from yac.lib.registry import set_remote_string_w_challenge
from yac.lib.file import get_file_contents
from yac.lib.variables import get_variable, set_variable
from yac.lib.validator import validate_dictionary
NULL_PARAMS = 'service params do not exist'
INVALID_PARAMS = 'service params are not valid'
SERVICE_PARAMS_SUFFIX = '-service-params'
REQUIRED_FIELDS = [
 'params-name.value',
 'params']
SUPPORTED_KEYS = [
 'params-name',
 'params',
 'description']

class ServiceError:

    def __init__(self, msg):
        self.msg = msg


def validate_service_params(service_params):
    val_errors = validate_dictionary(service_params, SUPPORTED_KEYS, REQUIRED_FIELDS)
    return val_errors


def get_all_service_params_names(search_string=''):
    params_names = []
    registry_keys = get_registry_keys()
    for key in registry_keys:
        if SERVICE_PARAMS_SUFFIX in key:
            if search_string and search_string in key:
                params_names = params_names + [key.replace(SERVICE_PARAMS_SUFFIX, '')]

    return params_names


def get_service_params(serviceparams_arg):
    service_params, params_name = get_service_params_from_file(serviceparams_arg)
    if serviceparams_arg and params_name == NULL_PARAMS:
        if is_service_params_name_complete(serviceparams_arg):
            params_name = serviceparams_arg
        elif is_service_params_available_partial_name(serviceparams_arg):
            params_name = get_complete_name(serviceparams_arg)
        service_params, params_name = get_service_params_by_name(params_name)
    return (service_params, params_name)


def get_service_params_from_file(serviceparams_arg, params_only=True):
    service_params = {}
    params_name = NULL_PARAMS
    abs_path = ''
    if serviceparams_arg:
        file_contents = get_file_contents(serviceparams_arg)
        if file_contents:
            service_params_descriptor = json.loads(file_contents)
            if not validate_service_params(service_params_descriptor):
                params_name = get_variable(service_params_descriptor, 'params-name')
                if params_only:
                    service_params = service_params_descriptor['params']
                else:
                    service_params = service_params_descriptor
            else:
                params_name = INVALID_PARAMS
    return (
     service_params, params_name)


def convert_kvps_to_params(kvps, params):
    kvp_array = kvps.split(',')
    for kvp in kvp_array:
        kcv = kvp.split(':')
        if len(kcv) == 2:
            set_variable(params, kcv[0], kcv[1])
        if len(kcv) == 3:
            set_variable(params, kcv[0], kcv[1], kcv[2])


def get_service_params_by_name(params_name):
    service_params = {}
    if params_name:
        reg_key = params_name + SERVICE_PARAMS_SUFFIX
        service_contents = get_remote_value(reg_key)
        if service_contents:
            service_params_descriptor = json.loads(service_contents)
            service_params = service_params_descriptor['params']
        else:
            params_name = NULL_PARAMS
    return (
     service_params, params_name)


def clear_service_params(params_name, challenge):
    service_params, params_name_returned = get_service_params_by_name(params_name)
    if service_params:
        reg_key = params_name + SERVICE_PARAMS_SUFFIX
        clear_entry_w_challenge(reg_key, challenge)
    else:
        raise ServiceError("service params with key %s doesn't exist" % params_name)


def register_service_params(params_name, service_path, challenge):
    if os.path.exists(service_path):
        service_contents_str = get_file_contents(service_path)
        if service_contents_str:
            reg_key = params_name + SERVICE_PARAMS_SUFFIX
            set_remote_string_w_challenge(reg_key, service_contents_str, challenge)
    else:
        raise ServiceError("service path %s doesn't exist" % service_path)


def is_service_params_name_complete(params_name):
    is_complete = False
    name_parts = params_name.split(':')
    if len(name_parts) == 2:
        is_complete = True
    return is_complete


def is_service_params_available_partial_name(service_partial_name):
    is_available = False
    if not is_service_params_name_complete(service_partial_name):
        complete_name_candidate = '%s:%s' % (service_partial_name, 'latest')
        service_desc, params_name = get_service_params_by_name(complete_name_candidate)
        if service_desc:
            is_available = True
    return is_available


def get_complete_name(params_name):
    complete_name = ''
    if not is_service_params_name_complete(params_name):
        complete_name_candidate = '%s:%s' % (params_name, 'latest')
        service_desc, params_name = get_service_params_by_name(complete_name_candidate)
        if service_desc:
            complete_name = complete_name_candidate
    return complete_name