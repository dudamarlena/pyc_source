# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/db/models/fields/proxy.py
# Compiled at: 2019-02-14 00:35:17
"""
Field-like classes that aren't really fields. It's easier to use objects that
have the same attributes as fields sometimes (avoids a lot of special casing).
"""
from django.db.models import fields

class OrderWrt(fields.IntegerField):
    """
    A proxy for the _order database field that is used when
    Meta.order_with_respect_to is specified.
    """

    def __init__(self, *args, **kwargs):
        kwargs['name'] = '_order'
        kwargs['editable'] = False
        super(OrderWrt, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(OrderWrt, self).deconstruct()
        del kwargs['editable']
        return (name, path, args, kwargs)