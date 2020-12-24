# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/joel/Workspace/dev/dev/utils.py
# Compiled at: 2020-01-13 19:10:42
# Size of source mod 2**32: 748 bytes
import re, os, sys

def sub_to_exec(string, params):
    cmd = re.sub('<.+?>', lambda x: params[remove_chars(x.group(0), ['<', '>'])], string)
    return cmd.split(' ')


def remove_chars(string, chars):
    to_remove = {c:'' for c in chars}
    return string.translate(str.maketrans(to_remove))


def override(a, b, fmt=None):
    if fmt:
        return {k:(b[fmt(k)] if b[fmt(k)] else v) for k, v in a.items()}
    else:
        return {k:(b[k] if b[k] else v) for k, v in a.items()}


def join_paths(a, b):
    return os.path.abspath(os.path.join(a, b))


def get_module_from_path(abs_module_path):
    abs_dir_path, module_name = abs_module_path.rsplit('/', 1)
    return (abs_dir_path, module_name)