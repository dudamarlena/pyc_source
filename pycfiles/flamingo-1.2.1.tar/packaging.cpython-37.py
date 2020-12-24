# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fsc/work/devel/flamingo/flamingo/core/packaging.py
# Compiled at: 2020-04-28 06:15:31
# Size of source mod 2**32: 378 bytes
from pkg_resources import iter_entry_points

def find_entry_points(prefix):
    dirs = []
    for entry_point in iter_entry_points('flamingo'):
        if entry_point.name.startswith(prefix):
            dirs.append((entry_point.name[len(prefix):], entry_point.load()))

    return dirs


def find_project_template_dirs():
    return find_entry_points('project_templates.')