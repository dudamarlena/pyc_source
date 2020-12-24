# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cox/Documents/GitHub/GoogleAuthenticatorPyPI/django_google_auth2/templatetags/otp_tags.py
# Compiled at: 2019-04-02 06:38:14
# Size of source mod 2**32: 665 bytes
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
register = template.Library()

@register.filter
@stringfilter
def qrcode(value, alt=None):
    url = conditional_escape('http://chart.apis.google.com/chart?%s' % urlencode({'chs':'150x150',  'cht':'qr',  'chl':value,  'choe':'UTF-8'}))
    alt = conditional_escape(alt or value)
    return mark_safe('<img class="qrcode" src="%s" width="150" height="150" alt="%s" />' % (url, alt))