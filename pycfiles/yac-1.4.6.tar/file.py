# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: yac/lib/file.py
# Compiled at: 2017-11-16 20:28:41
import os, urlparse, json
from yac.lib.registry import set_remote_string_w_challenge, get_remote_value, get_registry_keys
from yac.lib.registry import clear_entry_w_challenge
from yac.lib.registry import set_local_value, get_local_value, delete_local_value, get_local_keys
from yac.lib.paths import get_yac_path, get_lib_path
from yac.lib.variables import get_variable
YAC_FILE_PREFIX = 'yac://'

class FileError:

    def __init__(self, msg):
        self.msg = msg


def get_all_file_keys():
    file_keys = []
    registry_keys = get_registry_keys()
    for key in registry_keys:
        if file_in_registry(key):
            file_keys = file_keys + [key.replace(YAC_FILE_PREFIX, '')]

    return file_keys


def get_file_from_registry(file_key):
    file_contents = ''
    reg_key = get_file_reg_key(file_key)
    file_contents = get_remote_value(reg_key)
    return file_contents


def clear_file_from_registry(file_path, challenge):
    if get_file_from_registry(file_path):
        reg_key = get_file_reg_key(file_path)
        clear_entry_w_challenge(reg_key, challenge)
    else:
        raise FileError("file with key %s doesn't exist" % file_path)


def register_file(file_key, file_path, challenge):
    if os.path.exists(file_path):
        with open(file_path) as (file_path_fp):
            file_contents = file_path_fp.read()
            reg_key = get_file_reg_key(file_key)
            set_remote_string_w_challenge(reg_key, file_contents, challenge)
    else:
        raise FileError("file at %s doesn't exist" % file_path)


def get_file_reg_key(file_with_path, file_namespace=''):
    file_key = file_with_path
    if file_namespace:
        file_key = os.path.join(file_namespace, file_with_path)
    return YAC_FILE_PREFIX + file_key


def get_file_contents(file_key_or_path, servicefile_path=''):
    file_contents = ''
    if file_in_registry(file_key_or_path):
        file_contents = get_remote_value(file_key_or_path)
    elif os.path.exists(file_key_or_path):
        with open(file_key_or_path) as (file_arg_fp):
            file_contents = file_arg_fp.read()
    elif os.path.exists(os.path.join(servicefile_path, file_key_or_path)):
        with open(os.path.join(servicefile_path, file_key_or_path)) as (file_arg_fp):
            file_contents = file_arg_fp.read()
    return file_contents


def get_file_abs_path(file_key_or_path, servicefile_path):
    abs_path = ''
    if os.path.exists(file_key_or_path):
        abs_path = os.path.dirname(os.path.abspath(file_key_or_path))
    elif os.path.exists(os.path.join(servicefile_path, file_key_or_path)):
        abs_path = os.path.dirname(os.path.join(servicefile_path, file_key_or_path))
    return abs_path


def localize_file(file_key_or_path, servicefile_path=''):
    localized_file = ''
    if file_in_registry(file_key_or_path):
        file_contents = get_remote_value(file_key_or_path)
        localized_file = create_customization_file(file_key_or_path, file_contents)
    elif os.path.exists(file_key_or_path):
        localized_file = file_key_or_path
    elif os.path.exists(os.path.join(servicefile_path, file_key_or_path)):
        localized_file = os.path.join(servicefile_path, file_key_or_path)
    return localized_file


def file_in_registry(file_key):
    to_ret = False
    if file_key and YAC_FILE_PREFIX in file_key:
        to_ret = True
    return to_ret


def file_in_yac_sources(file_key):
    sources_root = get_yac_path()
    source_path = os.path.join(sources_root, file_key)
    return os.path.exists(source_path)


def create_customization_file(file_yac_url, file_contents=''):
    if not file_contents:
        file_contents = get_file_contents(file_yac_url)
    file_parts = urlparse.urlparse(file_yac_url)
    script_file_rel_path = file_parts.netloc + file_parts.path
    script_file_path = os.path.join(get_lib_path(), 'customizations', script_file_rel_path)
    script_file_dir = os.path.dirname(script_file_path)
    if not os.path.exists(script_file_dir):
        os.makedirs(script_file_dir)
    with open(script_file_path, 'w') as (script_file_path_fp):
        script_file_path_fp.write(file_contents)
    return script_file_path


def dump_dictionary(dictionary, service_name, file_name):
    file_contents = json.dumps(dictionary, indent=2)
    file_path = dump_file_contents(file_contents, service_name, file_name)
    return file_path


def dump_file_contents(file_contents, service_name, file_name):
    dump_path = get_dump_path(service_name)
    file_path = os.path.join(dump_path, file_name)
    with open(file_path, 'w') as (the_file):
        the_file.write(file_contents)
    return file_path


def get_dump_path(service_name):
    home = os.path.expanduser('~')
    service_name_cleaned = service_name.replace(':', os.sep)
    dump_path = os.path.join(home, '.yac', 'tmp', service_name_cleaned)
    if not os.path.exists(dump_path):
        os.makedirs(dump_path)
    return dump_path


def get_localized_script_path(script_path_arg, params):
    if file_in_registry(script_path_arg):
        script_file_path = create_customization_file(script_path_arg)
    elif file_in_yac_sources(script_path_arg):
        script_file_path = os.path.join(get_yac_path(), script_path_arg)
    else:
        servicefile_path = get_variable(params, 'servicefile-path')
        script_file_path = os.path.join(servicefile_path, script_path_arg)
    return script_file_path