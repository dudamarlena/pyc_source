# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/emails/templatetags/email_filters.py
# Compiled at: 2020-02-26 14:48:40
# Size of source mod 2**32: 806 bytes
from django import template
from tendenci.apps.site_settings.utils import get_setting
from django.utils.safestring import mark_safe
register = template.Library()
GLOBAL_SITE_URL = get_setting('site', 'global', 'siteurl')

def relative_to_absolute_urls(value):
    """
    Converts all relative urls to absolute urls.
    Automatically marks the strings as safe.
    e.g.
    {{ event.description|relative_to_absolute_urls }}
    """
    value = value.replace('src="/', 'src="%s/' % GLOBAL_SITE_URL)
    value = value.replace("src='/", "src='%s/" % GLOBAL_SITE_URL)
    value = value.replace('href="/', 'href="%s/' % GLOBAL_SITE_URL)
    value = value.replace("href='/", "<href='%s/" % GLOBAL_SITE_URL)
    return mark_safe(value)


register.filter('relative_to_absolute_urls', relative_to_absolute_urls)