# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/shuyucms/utils/deprecation.py
# Compiled at: 2016-05-21 00:07:07
from inspect import getmro
from django import VERSION
if VERSION < (1, 6):

    def get_permission_codename(action, opts):
        """
        Returns the codename of the permission for the specified action,
        in a 1.5 compatible manner.

        Compare with ``django/contrib/auth/__init__.py``.
        """
        return '%s_%s' % (action, opts.object_name.lower())


    def renamed_get_queryset(cls):
        """
        On classes and their bases with ``get_queryset`` defines
        ``get_query_set`` to preserve compatibility with Django 1.5, on
        those with ``get_query_set`` defines ``get_queryset``, so calls
        to the latter one can be always used.

        Compare with ``django.utils.deprecation.RenameMethodsBase``.
        """
        for base in getmro(cls):
            for old_method_name in ['get_query_set', 'queryset']:
                old_method = base.__dict__.get(old_method_name)
                new_method = base.__dict__.get('get_queryset')
                if not old_method and new_method:
                    setattr(base, old_method_name, new_method)
                elif not new_method and old_method:
                    setattr(base, 'get_queryset', old_method)

        return cls


else:

    def renamed_get_queryset(cls):
        return cls