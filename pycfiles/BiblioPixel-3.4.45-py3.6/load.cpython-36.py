# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/project/load.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 1546 bytes
from . import aliases
import loady, os, platform
from ..util import data_file, log
guess_name = loady.importer.guess_name
CACHE = os.path.expanduser('~/.bibliopixel/code_cache')
ROOT_FILE = None

def data(name, use_json=True):
    if not name:
        return {}
    try:
        return data_file.loads(name)
    except:
        return loady.data.load(name, use_json)


def code(name, python_path=None):
    return name and loady.code.load_code(name, python_path, recurse=True)


def module(name, python_path=None):
    return name and loady.code.load_module(name, python_path)


def extender(path):
    parts = [
     os.getcwd()] + _split_path(path)
    missing = [p for p in parts if not os.path.exists(p)]
    if missing:
        msg = 'This "path" entry does not exist' if len(missing) == 1 else 'These "path" entries do not exist'
        m2 = ['"%s"' % p for p in missing]
        log.warning('%s: %s', msg, ', '.join(m2))
        parts = [p for p in parts if os.path.exists(p)]
    return parts and loady.sys_path.extender(':'.join(parts))


def load_if_filename(s):
    if isinstance(s, str):
        if s.endswith('.yml') or s.endswith('.json'):
            if ROOT_FILE:
                if not os.path.isabs(s):
                    s = os.path.join(os.path.dirname(ROOT_FILE), s)
            return data_file.load(s)


def _split_path(path):
    if not path:
        return []
    else:
        p = path.split(';')
        if platform.system() == 'Windows':
            return p
        return [j for i in p for j in i.split(':')]