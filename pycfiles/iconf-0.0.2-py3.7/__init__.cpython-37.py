# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3392)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/iconf/__init__.py
# Compiled at: 2018-06-20 15:28:27
# Size of source mod 2**32: 955 bytes
import json, os

def get(keys=None, path=None):
    if not keys:
        if not path:
            raise Exception('please set the keys or path argument')
        elif keys and not isinstance(keys, list):
            raise Exception('keys argument must be a list')
        json_data = {}
        if path:
            try:
                with open(path, 'r') as (f):
                    json_data = json.load(f)
            except IOError:
                pass

        if json_data:
            if not keys:
                return json_data
    else:
        configs = {key:None for key in keys}
        try:
            import django.conf as dj_settings
        except ImportError:
            dj_settings = None

    for key in keys:
        if key in os.environ:
            configs.update({key: os.environ[key]})
        else:
            if key in json_data:
                configs.update({key: json_data[key]})

    return configs