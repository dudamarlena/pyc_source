# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/benzkji/Development/open/django-ckeditor-link/ckeditor_link/templatetags/ckeditor_link_tags.py
# Compiled at: 2019-09-30 08:33:06
# Size of source mod 2**32: 3175 bytes
import importlib
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from ckeditor_link import conf
from django import template
from django.template.defaultfilters import stringfilter
try:
    module_name, class_name = conf.CKEDITOR_LINK_MODEL.rsplit('.', 1)
    my_module = importlib.import_module(module_name)
    ckeditor_link_class = getattr(my_module, class_name, None)
except ImportError:
    ckeditor_link_class = None

register = template.Library()

@register.filter
@stringfilter
def ckeditor_link_add_links(html):
    from lxml.html import fragment_fromstring, tostring
    if not ckeditor_link_class:
        if settings.DEBUG:
            msg = 'Warning: CKEDITOR_LINK_MODEL (%s) could not be imported!?' % (conf.CKEDITOR_LINK_MODEL,)
            raise ImproperlyConfigured(msg)
        return html
    fragment = fragment_fromstring('<div>' + html + '</div>')
    links = fragment.cssselect('a')
    for link in links:
        if link.get('data-ckeditor-link', None):
            link.attrib.pop('data-ckeditor-link')
            kwargs = {}
            dummy_link = ckeditor_link_class()
            for key, value in link.items():
                if key.startswith('data-'):
                    new_key = key.replace('data-', '', 1)
                    if new_key == 'page_2':
                        new_key = 'cms_page'
                    if new_key == 'cms_page_2':
                        new_key = 'cms_page'
                if hasattr(dummy_link, new_key):
                    if hasattr(dummy_link, new_key + '_id'):
                        new_key = new_key + '_id'
                        if not value:
                            value = None
                    kwargs[new_key] = value
                    link.attrib.pop(key)

            for key, formatted_string in conf.CKEDITOR_LINK_ATTR_MODIFIERS.items():
                try:
                    kwargs[key] = (formatted_string.format)(**kwargs)
                except KeyError:
                    pass

            try:
                real_link = ckeditor_link_class(**kwargs)
                link.set('href', real_link.get_link())
                if getattr(real_link, 'get_link_target', None):
                    link.set('target', real_link.get_link_target())
                if getattr(real_link, 'get_link_style', None):
                    link.set('class', real_link.get_link_style())
            except (ValueError, ObjectDoesNotExist):
                continue

    return tostring(fragment, encoding='unicode')