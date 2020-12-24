# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Python34\Lib\site-packages\autohdl\pkg_info.py
# Compiled at: 2015-05-16 02:35:10
# Size of source mod 2**32: 484 bytes
import os, json

def load():
    ver_fp = os.path.join(os.path.dirname(__file__), 'data', 'version.json')
    with open(ver_fp) as (f):
        data = json.load(f)
        return (ver_fp, data)


def version():
    _, ver = load()
    return '{}.{}.{}'.format(ver['major'], ver['minor'], ver['build'])


def inc_version():
    ver_fp, ver = load()
    ver['build'] += 1
    with open(ver_fp, 'w') as (f):
        f.write(json.dumps(ver))
    return version()