# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/helpdesk/templatetags/load_helpdesk_settings.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 733 bytes
"""
django-helpdesk - A Django powered ticket tracker for small enterprise.

templatetags/load_helpdesk_settings.py - returns the settings as defined in
                                    django-helpdesk/helpdesk/settings.py
"""
from django.template import Library
import tendenci.apps.helpdesk as helpdesk_settings_config

def load_helpdesk_settings(request):
    try:
        return helpdesk_settings_config
    except Exception as e:
        try:
            import sys
            print("'load_helpdesk_settings' template tag (django-helpdesk) crashed with following error:", file=(sys.stderr))
            print(e, file=(sys.stderr))
            return ''
        finally:
            e = None
            del e


register = Library()
register.filter('load_helpdesk_settings', load_helpdesk_settings)