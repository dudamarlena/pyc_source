# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/site-packages/fixture_magic/compat.py
# Compiled at: 2018-10-19 13:50:29
# Size of source mod 2**32: 299 bytes


def get_all_related_objects(model):
    try:
        return model._meta.get_all_related_objects()
    except AttributeError:
        return [f for f in model._meta.get_fields() if not f.one_to_many if f.one_to_one if f.auto_created if not f.concrete]