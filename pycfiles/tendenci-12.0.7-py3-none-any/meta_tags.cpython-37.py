# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/meta/templatetags/meta_tags.py
# Compiled at: 2020-02-26 14:48:40
# Size of source mod 2**32: 1594 bytes
from django.db.models import ForeignKey, TextField
import django.core.cache as cache
from django.template import Library
from bs4 import BeautifulSoup
from tendenci.libs.tinymce.models import HTMLField
from tendenci.apps.files.models import File
from tendenci.apps.site_settings.utils import get_setting
register = Library()

@register.inclusion_tag('meta/og_image.html')
def meta_og_image(obj, field_name):
    base_url = get_setting('site', 'global', 'siteurl')
    keys = ['meta_og_image', obj._meta.app_label, str(obj.id),
     field_name, obj.update_dt.strftime('%m%d%Y%H%M%S')]
    cache_key = '_'.join(keys)
    cached_value = cache.get(cache_key)
    if cached_value:
        return cached_value
    try:
        field = obj._meta.get_field(field_name)
        image_list = []
        if isinstance(field, HTMLField) or isinstance(field, TextField):
            content = getattr(obj, field_name)
            soup = BeautifulSoup(content)
            for image in soup.find_all('img'):
                image_url = image['src']
                if image_url:
                    if image_url[0] == '/':
                        if image_url[:2] != '//':
                            image_url = base_url + image_url
                    image_list.append(image_url)

        else:
            if isinstance(field, ForeignKey):
                image = getattr(obj, field_name)
                if isinstance(image, File):
                    image_list.append(base_url + image.get_absolute_url())
        value = {'urls': image_list}
        cache.set(cache_key, value)
        return value
    except Exception:
        return {}