# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/xica/.venvs/xica2.7/lib/python2.7/site-packages/kiga_plugin/__init__.py
# Compiled at: 2015-09-02 10:28:10
from pkg_resources import iter_entry_points

def load_entry_point(group, name):
    entry_point = next((x for x in iter_entry_points(group, name) if x.name == name), None)
    if entry_point is None:
        raise ValueError(('entry point "{}.{}" not found.').format(group, name))
    return entry_point.load()