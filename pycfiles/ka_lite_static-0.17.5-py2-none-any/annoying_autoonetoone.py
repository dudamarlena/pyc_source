# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/South/south/introspection_plugins/annoying_autoonetoone.py
# Compiled at: 2018-07-11 18:15:31
from django.conf import settings
from south.modelsinspector import add_introspection_rules
if 'annoying' in settings.INSTALLED_APPS:
    try:
        from annoying.fields import AutoOneToOneField
    except ImportError:
        pass
    else:
        add_introspection_rules([], ['^annoying\\.fields\\.AutoOneToOneField'])