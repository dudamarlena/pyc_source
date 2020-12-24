# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pm/.local/lib/python3.5/site-packages/configurator/formats/json.py
# Compiled at: 2016-05-20 05:07:39
# Size of source mod 2**32: 393 bytes
import configurator.formats._safe_importer, os, json
default_indent = 2

def load(filename):
    if os.path.exists(filename):
        with open(filename, mode='r') as (f):
            return json.load(f)


def dump(filename, config, indent=default_indent):
    with open(filename, mode='w') as (f):
        json.dump(config, f, indent=indent, sort_keys=True)