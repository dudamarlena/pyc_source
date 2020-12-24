# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-core/ovp_core/helpers.py
# Compiled at: 2017-04-20 14:47:52
# Size of source mod 2**32: 729 bytes
from django.conf import settings
from django.utils.translation import ugettext as _

def get_settings(string='OVP_CORE'):
    return getattr(settings, string, {})


def is_email_enabled(email):
    """ Emails are activated by default. Returns false
      if an email has been disabled in settings.py
  """
    s = get_settings(string='OVP_EMAILS')
    email_settings = s.get(email, {})
    enabled = True
    if email_settings.get('disabled', False):
        enabled = False
    return enabled


def get_email_subject(email, default):
    """ Allows for email subject overriding from settings.py  """
    s = get_settings(string='OVP_EMAILS')
    email_settings = s.get(email, {})
    title = email_settings.get('subject', default)
    return _(title)