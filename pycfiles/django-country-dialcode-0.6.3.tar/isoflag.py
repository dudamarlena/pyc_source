# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/areski/projects/django/django-country-dialcode/country_dialcode/utils/isoflag.py
# Compiled at: 2012-10-02 13:04:02
from django.conf import settings

def iso_flag(iso, flag_path=''):
    """
    Returns a full path to the ISO 3166-1 alpha-2 country code flag image.

    ``flag_path`` is given in the form
    ``'<path relative to media root>/%s.gif'``
    and is appended to ``settings.MEDIA_URL``

    if a valid flag_path is not given trys to use
    ``settings.COUNTRIES_FLAG_PATH``
    defaults to ``'flags/%s.gif'``

    """
    default = '-'
    if not iso:
        iso = default
    else:
        iso = iso.lower().strip()
    try:
        flag_name = flag_path % iso
    except (ValueError, TypeError):
        flag_path = getattr(settings, 'COUNTRIES_FLAG_PATH', 'flags/%s.png')
        try:
            flag_name = flag_path % iso
        except (ValueError, TypeError):
            return ''

    return flag_name