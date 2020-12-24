# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/x0ox/Dropbox/ActiveDev/yac/yac/cli/ssh.py
# Compiled at: 2017-11-16 20:28:40
import argparse, os, inspect, jmespath, json
from colorama import Fore, Style
from yac.lib.service import get_service, get_service_parmeters, get_service_alias
from yac.lib.stack import get_stack_templates, get_stack_name, get_ec2_ips, deploy_stack_files
from yac.lib.naming import set_namer
from yac.lib.params import get_service_params, NULL_PARAMS, INVALID_PARAMS
from yac.lib.vpc import get_vpc_prefs
from yac.lib.inputs import get_inputs
from yac.lib.variables import get_variable, set_variable
from yac.lib.cache import get_cache_value, set_cache_value_dt

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error('The key file %s does not exist!' % arg)
    else:
        return arg


def main():
    path_help = 'path to the private key file for this service'
    user_help = 'the user to login as'
    public_help = 'connect using the public IP address?'
    parser = argparse.ArgumentParser('ssh into a stack ec2 instance')
    parser.add_argument('servicefile', help='location of the Servicefile (registry key or abspath)')
    parser.add_argument('--path', help=path_help + ' (defaults to previous)', type=lambda x: is_valid_file(parser, x))
    parser.add_argument('-u', '--user', help=user_help + ' (defaults to previous')
    parser.add_argument('-s', '--search', help='search string, to support multiple EC2 instances in the same auto-scaling group')
    parser.add_argument('--public', help=public_help + ' (defaults to previous)', action='store_true')
    parser.add_argument('-a', '--alias', help='service alias for the stack currently supporting this service (deault alias is per Servicefile)')
    parser.add_argument('-p', '--params', help='path to a file containing additional, static, service parameters (e.g. vpc params, of service constants)')
    args = parser.parse_args()
    service_descriptor, service_name, servicefile_path = get_service(args.servicefile)
    if not service_descriptor:
        print 'The Servicefile input does not exist locally or in registry. Please try again.'
        exit()
    vpc_prefs = get_vpc_prefs()
    set_namer(service_descriptor, servicefile_path, vpc_prefs)
    service_alias = get_service_alias(service_descriptor, args.alias)
    service_params_input, service_params_name = get_service_params(args.params)
    if args.params and service_params_name == NULL_PARAMS:
        print 'The service params specified do not exist locally or in registry. Please try again.'
        exit()
    elif service_params_name == INVALID_PARAMS:
        print 'The service params file specified failed validation checks. Please try again.'
        exit()
    service_parmeters = get_service_parmeters(service_alias, service_params_input, service_name, service_descriptor, servicefile_path, vpc_prefs)
    stack_name = get_stack_name(service_parmeters)
    use_public = get_use_public(service_alias, args.public)
    ec2_ips = get_ec2_ips(stack_name, args.search, use_public)
    if len(ec2_ips) > 0:
        ec2_ip = pick_ec2_ip(ec2_ips)
        ssh_user = get_ssh_user(service_alias, user_help, args.user)
        key_path = get_key_path(service_alias, path_help, args.path)
        ssh_cmd = 'ssh -i %s %s@%s' % (key_path, ssh_user, ec2_ip)
        os.system(ssh_cmd)
    else:
        print 'Could not find any ec2 hosts for the %s stack' % stack_name


def get_use_public(service_alias, arg_input):
    cache_key = '%s:arg:use-public'
    use_public = get_cached_arg_bool('public', arg_input, cache_key)
    return use_public


def get_key_path(service_alias, arg_help, arg_input):
    cache_key = '%s:arg:ssh-key'
    key_path = get_cached_arg_val('path', arg_input, cache_key, arg_help)
    return key_path


def get_ssh_user(service_alias, arg_help, arg_input):
    cache_key = '%s:arg:ssh-user'
    ssh_user = get_cached_arg_val('ssh-user', arg_input, cache_key, arg_help)
    return ssh_user


def pick_ec2_ip(ec2_ips):
    params = {}
    params['service-inputs'] = {'inputs': {'ec2-ip': {'description': 'EC2 IP', 
                             'help': 'The IP of target host', 
                             'wizard_fxn': {'name': 'string_wizard'}, 
                             'constraints': {'required': True, 
                                             'options': ec2_ips}}}}
    get_inputs(params)
    ec2_ip = get_variable(params, 'ec2-ip')
    return ec2_ip


def get_cached_arg_val(arg_name, arg_input, cache_key, input_help):
    cached_arg_val = ''
    if arg_input:
        cached_arg_val = arg_input
    else:
        cached_arg_val = get_cache_value(cache_key, '')
        if not cached_arg_val:
            print "The '%s' is not yet cached locally." % arg_name
            print 'Input description: %s.' % input_help
            input_prompt_msg = "Please enter a value for the '%s' >> " % arg_name
            cached_arg_val = raw_input(input_prompt_msg)
    set_cache_value_dt(cache_key, cached_arg_val)
    return cached_arg_val


def get_cached_arg_bool(arg_name, arg_input, cache_key):
    cached_arg_val = ''
    if arg_input:
        cached_arg_val = arg_input
    else:
        cached_arg_val = get_cache_value(cache_key, '')
    set_cache_value_dt(cache_key, cached_arg_val)
    return cached_arg_val