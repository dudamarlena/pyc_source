# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/contrib/admin/templatetags/admin_static.py
# Compiled at: 2019-02-14 00:35:15
from django.template import Library
from django.templatetags.static import static as _static
register = Library()

@register.simple_tag
def static(path):
    return _static(path)