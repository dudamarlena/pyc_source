# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/django_workflow/utils.py
# Compiled at: 2017-08-28 11:23:36


def import_from(module, name):
    module = __import__(module, fromlist=[name])
    return getattr(module, name)


def import_from_path(full_path):
    parts = full_path.rsplit('.', 1)
    return import_from(parts[0], parts[1])