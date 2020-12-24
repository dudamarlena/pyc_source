# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/catchbot/config.py
# Compiled at: 2018-06-23 13:58:03
# Size of source mod 2**32: 294 bytes
import os, yaml
from pkg_resources import resource_stream
DIR_TEMPLATES = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir, 'msg_templates'))

def load_mapping():
    with resource_stream('catchbot', 'etc/mapping.yml') as (f):
        return yaml.load(f)