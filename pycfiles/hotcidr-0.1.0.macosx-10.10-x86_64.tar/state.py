# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/skemper/workspace/hotcidr/venv/lib/python2.7/site-packages/hotcidr/state.py
# Compiled at: 2014-09-10 16:58:32
import yaml, ports

def load(f):
    r = yaml.safe_load(f)
    if r and 'rules' in r:
        for rule in r['rules']:
            if 'ports' in rule:
                p = ports.parse(rule['ports'])
                if p:
                    rule['ports'] = p
                    rule['fromport'] = p.fromport or -1
                    rule['toport'] = p.toport or -1

    return r


def dump(s, default_flow_style=True):
    if s and 'rules' in s:
        for rule in s['rules']:
            if 'ports' in rule:
                rule['ports'] = rule['ports'].yaml_str()
            if 'fromport' in rule:
                del rule['fromport']
            if 'toport' in rule:
                del rule['toport']

    return yaml.safe_dump(s, default_flow_style=default_flow_style)