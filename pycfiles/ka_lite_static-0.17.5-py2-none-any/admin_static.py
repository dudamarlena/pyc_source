# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/contrib/admin/templatetags/admin_static.py
# Compiled at: 2018-07-11 18:15:30
from django.conf import settings
from django.template import Library
register = Library()
if 'django.contrib.staticfiles' in settings.INSTALLED_APPS:
    from django.contrib.staticfiles.templatetags.staticfiles import static
else:
    from django.templatetags.static import static
static = register.simple_tag(static)