# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mw/dev/pixelcms-server/cms/common/utils.py
# Compiled at: 2016-12-31 04:04:09
# Size of source mod 2**32: 1046 bytes
from django.utils.translation import get_language
from cms.settings.models import Settings

def current_lang():
    return get_language()


def served_langs():
    return (
     'any', get_language())


def generate_meta(title=None, title_suffix=True, description=None, robots=None):
    try:
        settings = Settings.objects.get(language=current_lang())
    except Settings.DoesNotExist:
        try:
            settings = Settings.objects.get(language__in=served_langs())
        except Settings.DoesNotExist:
            settings = Settings.objects.create()

    if title_suffix is None:
        title_suffix = settings.page_title_site_name_suffix
    if title_suffix:
        if title:
            title += ' {} '.format(settings.suffix_separator)
        title += settings.site_name
    if not title:
        title = settings.site_name
    return {'title': title, 
     'description': description or settings.meta_description, 
     'robots': robots or settings.meta_robots}