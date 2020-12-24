# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/onepassword_tools/lib/MiscUtils.py
# Compiled at: 2019-05-24 16:38:50
# Size of source mod 2**32: 1166 bytes
import onepassword_tools.lib.ConfigFile as ConfigFile
import secrets, string
from uuid import UUID

def generate_password(password_length):
    characters = string.ascii_letters + string.digits + '-_=.*+'
    return ''.join((secrets.choice(characters) for i in range(password_length)))


def is_uuid(uuid_string, version=4):
    try:
        uid = UUID(uuid_string, version=version)
        return uid.hex == uuid_string.replace('-', '')
    except ValueError:
        return False


def remove_null_value_keys_in_dict(data, only_keys=None):
    if only_keys is None:
        only_keys = [
         'v', 'value']
    new_data = {}
    for k, v in data.items():
        if isinstance(v, dict):
            v = remove_null_value_keys_in_dict(v)
        else:
            if isinstance(v, list):
                clean_list = []
                for el in v:
                    clean_list.append(remove_null_value_keys_in_dict(el))

                v = clean_list
            elif k in only_keys and v in ('', None, {}):
                continue
            new_data[k] = v

    return new_data


class SimpleFormatter(string.Formatter):

    def get_value(self, key, args, kwargs):
        return args[0].get(key)