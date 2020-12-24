# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Sinisa/Documents/devel/sbg-zenom/sbdk/resources/__init__.py
# Compiled at: 2015-05-11 10:16:19
import os.path
from pkgutil import get_data

def read(name):
    return get_data('sbdk.resources', name)


def copy(name, dst):
    joined = os.path.join(dst, os.path.basename(name))
    dst_name = joined if os.path.isdir(dst) else dst
    if os.path.exists(dst_name):
        print ("File '{}' already exists, skipping").format(dst_name)
        return
    with open(dst_name, 'w') as (out):
        out.write(read(name))


def process_template(file_name, dst=None, **bind_data):
    tpl = read(file_name)
    out = tpl.format(**bind_data)
    if dst:
        dst_name = dst
        if os.path.exists(dst) and os.path.isdir(dst):
            dst_name = os.path.join(dst, file_name)
        if os.path.exists(dst_name):
            print ("File '{}' already exists, skipping").format(dst_name)
            return out
        with open(dst_name, 'w') as (of):
            of.write(out)
    return out