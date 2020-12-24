# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nubo/config.py
# Compiled at: 2014-05-18 16:15:39
import os, json
CONFFILE = os.path.join(os.getenv('HOME'), '.nuborc')

def read_config():
    try:
        return json.loads(open(CONFFILE).read())
    except IOError:
        return {}


def write_config(values):
    old_values = read_config()
    updated = dict(old_values.items() + values.items())
    open(CONFFILE, 'w').write(json.dumps(updated, indent=4))
    os.chmod(CONFFILE, 384)
    return updated