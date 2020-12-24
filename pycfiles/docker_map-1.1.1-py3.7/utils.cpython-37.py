# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dockermap/utils.py
# Compiled at: 2019-10-19 14:38:08
# Size of source mod 2**32: 917 bytes
from __future__ import unicode_literals
import os
from .functional import lazy_once
expand_path = lambda value: os.path.expanduser(os.path.expandvars(value))
expand_path_lazy = lambda value: lazy_once(expand_path, value)

def merge_list(merged_list, items):
    """
    Merges items into a list, appends ignoring duplicates but retaining the original order. This modifies the list and
    does not return anything.

    :param merged_list: List to append de-duplicated items to.
    :type merged_list: list
    :param items: Items to merge into the list.
    :type items: collections.Iterable
    """
    if not items:
        return
    merged_set = set(merged_list)
    merged_add = merged_set.add
    merged_list.extend((item for item in items if item not in merged_set if not merged_add(item)))


format_image_tag = '{0[0]}:{0[1]}'.format