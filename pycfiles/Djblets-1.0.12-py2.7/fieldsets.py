# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/forms/fieldsets.py
# Compiled at: 2019-06-12 01:17:17
"""Utilities related to django.contrib.admin fieldsets."""
from __future__ import unicode_literals

def filter_fieldsets(form, admin=None, fieldsets=None, exclude=None, exclude_collapsed=True):
    """Filter fieldsets.

    This method allows us to filter fieldsets from a ModelAdmin to exclude
    fields (or an entire fieldset).

    Args:
        form (type or django.forms.Form):
            The form (or form class) to retrieve fieldsets for.

        admin (django.contrib.admin.ModelAdmin, optional):
            The model admin to retrieve fieldsets from. If this argument is not
            provided, ``fieldsets`` will be used instead.

        fieldsets (tuple, optional):
            The fieldsets to use.

        exclude (list of unicode, optional):
            An optional list of fields to exclude.

        exclude_collapsed (bool, optional):
            Whether or not to exclude fieldsets marked as collapsed by default.

    Yields:
        dict:
        An entry for each field set that should be rendered.

        If a field set would have no rendered fields, it is not yielded.
    """
    if admin is None and fieldsets is None:
        raise ValueError(b'filter_fieldsets: either admin or fieldsets must be provided.')
    if exclude is None:
        exclude = []
    exclude.extend(list(form._meta.exclude or []))
    if fieldsets is None:
        assert hasattr(admin, b'fieldsets'), b'admin.fieldsets is undefined.'
        assert iter(admin.fieldsets), b'admin.fieldsets should be iterable.'
        fieldsets = admin.fieldsets
    for name, data in fieldsets:
        fieldset = data.copy()
        if exclude_collapsed and b'collapse' in data.get(b'classes', ()):
            continue
        fieldset[b'fields'] = [ field_name for field_name in data[b'fields'] if field_name not in exclude
                              ]
        if fieldset[b'fields']:
            yield (
             name, fieldset)

    return