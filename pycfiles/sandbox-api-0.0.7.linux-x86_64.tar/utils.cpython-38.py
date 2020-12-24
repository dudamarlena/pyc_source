# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/hostedtoolcache/Python/3.8.2/x64/lib/python3.8/site-packages/sandbox_api/utils.py
# Compiled at: 2020-05-04 08:09:32
# Size of source mod 2**32: 1823 bytes
from typing import Tuple

def validate_command(c: dict) -> bool:
    """Returns True if <d> is a valid representation of a command, False otherwise.

    Check that:
        - 'command' is present and is a string.
        - if 'timeout' is present, it is either an integer or a float."""
    return all((
     'command' in c and isinstance(c['command'], str),
     'timeout' not in c or isinstance(c['timeout'], (int, float))))


def validate(config: dict) -> Tuple[(bool, str)]:
    """Check the validity of a config dictionary.
    
    Returns a tuple (bool, msg). If bool is True, the config dictionary is valid and msg is an
    empty string.
    If bool is False, the config dictionary is invalid and msg contains a message explaining the
    error."""
    if 'result_path' in config:
        if not isinstance(config['result_path'], str):
            return (
             False, f"result_path must be a string, not {type(config['result_path'])}")
    else:
        if 'save' in config:
            if not isinstance(config['save'], bool):
                return (
                 False, f"save must be a boolean, not {type(config['save'])}")
        else:
            if 'environ' in config:
                if not isinstance(config['environ'], dict):
                    return (
                     False, f"environ must be a dict, not {type(config['environ'])}")
            if 'commands' not in config:
                return (False, "Missing field 'commands' in config")
            return isinstance(config['commands'], list) or (
             False, f"commands must be a list, not {type(config['commands'])}")
        return config['commands'] or (False, 'commands list is empty')
    for c in config['commands']:
        if isinstance(c, dict):
            if not (validate_command(c) or isinstance(c, str)):
                return (
                 False, f"Command badly formatted : '{c}'")
        return (True, '')