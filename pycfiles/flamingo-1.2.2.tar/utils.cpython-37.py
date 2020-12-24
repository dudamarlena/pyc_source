# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fsc/work/devel/flamingo/flamingo/plugins/rst/utils.py
# Compiled at: 2020-05-01 10:33:08
# Size of source mod 2**32: 1616 bytes
import re
from docutils.parsers.rst import roles
ROLE_RE = re.compile('^(?P<arg0>[^<]+)((\\s+)?<(?P<arg1>[^>]+)>)?((\\s+)?(?P<options>.*))?$')
ROLE_OPTIONS_RE = re.compile('((?P<name>[^=]+)=(?P<value>[^\\s,]+)([\\s,]+)?)')

def parse_role_text(role_text):
    role_args = {'args':[],  'options':{}}
    role_text = role_text.strip()
    if role_text.startswith('<'):
        if role_text.endswith('>'):
            role_args['args'].append(role_text[1:-1])
            return role_args
    try:
        role_parts = ROLE_RE.search(role_text).groupdict()
    except Exception:
        role_args['args'].append(role_text)
        return role_args
    else:
        if role_parts['arg0']:
            role_args['args'].append(role_parts['arg0'].strip())
        if role_parts['arg1']:
            role_args['args'].append(role_parts['arg1'].strip())
        if role_parts['options']:
            for parts in ROLE_OPTIONS_RE.finditer(role_parts['options']):
                role_args['options'][parts[2]] = parts[3]

        return role_args


def parse_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        try:
            return {'true':True, 
             '1':True, 
             'false':False, 
             '0':False}[value.strip().lower()]
        except Exception:
            pass

    return bool(value)


def register_canonical_role(name, role):
    if name in roles._roles:
        roles._roles.pop(name)
    if name in roles._role_registry:
        roles._role_registry.pop(name)
    roles.register_canonical_role(name, role)