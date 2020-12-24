# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pm/.local/lib/python3.5/site-packages/configurator/formats/python.py
# Compiled at: 2016-05-20 05:07:39
# Size of source mod 2**32: 624 bytes
import configurator.formats._safe_importer, os, imp

def load(filename):
    if os.path.exists(filename):
        module = imp.load_source('virtual', filename)
        config = {i:getattr(module, i) for i in dir(module) if not i.startswith('__') and not i.endswith('__')}
        return config


def dump(filename, config):
    with open(filename, mode='w') as (f):
        f.write('#!/usr/bin/env python3\n\n')
        for key, value in config.items():
            f.write("{} = '{}'\n".format(key, value))