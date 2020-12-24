# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/studygroups/module_meta.py
# Compiled at: 2020-02-26 14:47:58
# Size of source mod 2**32: 4470 bytes
from django.utils.html import strip_tags
from django.utils.text import unescape_entities
from tendenci.apps.meta.utils import generate_meta_keywords
from tendenci.apps.site_settings.utils import get_setting
from tendenci.apps.base.utils import truncate_words
from tendenci.apps.categories.models import Category

class StudyGroupMeta:

    def get_title(self):
        object = self.object
        geo_location = get_setting('site', 'global', 'sitegeographiclocation')
        category = Category.objects.get_for_object(object, 'category')
        subcategory = Category.objects.get_for_object(object, 'subcategory')
        value = '%s' % object.title
        value = value.strip()
        if category:
            value = '%s %s' % (value, category)
        if category:
            if subcategory:
                value = '%s : %s' % (value, subcategory)
        value = value.strip()
        if geo_location:
            value = '%s | %s | ' % (value, geo_location)
        return value

    def get_description(self):
        object = self.object
        category = Category.objects.get_for_object(object, 'category')
        subcategory = Category.objects.get_for_object(object, 'subcategory')
        site_name = get_setting('site', 'global', 'sitedisplayname')
        geo_location = get_setting('site', 'global', 'sitegeographiclocation')
        content = object.content
        content = strip_tags(content)
        content = unescape_entities(content)
        content = content.replace('\n', '').replace('\r', '')
        content = truncate_words(content, 50)
        value = object.title
        value = '%s - %s' % (value, content)
        if site_name:
            value = '%s %s' % (value, site_name)
        else:
            if category:
                value = '%s, %s' % (value, category)
            if category:
                if subcategory:
                    value = '%s, %s' % (value, subcategory)
            value = '%s ' % value
        value = '%s %s %s' % (
         value, site_name, geo_location)
        value = value.strip()
        return value

    def get_keywords(self):
        object = self.object
        dynamic_keywords = generate_meta_keywords(object.content)
        primary_keywords = get_setting('site', 'global', 'siteprimarykeywords')
        secondary_keywords = get_setting('site', 'global', 'sitesecondarykeywords')
        geo_location = get_setting('site', 'global', 'sitegeographiclocation')
        site_name = get_setting('site', 'global', 'sitedisplayname')
        value = ''
        if primary_keywords:
            value = '%s %s' % (value, primary_keywords)
            value = value.strip()
        elif object.title:
            list = [site_name,
             geo_location,
             object.title]
            for item in list:
                if not item.strip():
                    list.remove(item)

            value = '%s %s, %s' % (value, ', '.join(list), dynamic_keywords)
        else:
            list = [site_name,
             geo_location,
             primary_keywords,
             secondary_keywords]
            value = '%s %s' % (value, ''.join(list))
        return value

    def get_canonical_url(self):
        return '{0}{1}'.format(get_setting('site', 'global', 'siteurl'), self.object.get_absolute_url())

    def get_meta(self, object, name):
        self.object = object
        self.name = name
        if name == 'title':
            if object.meta:
                if object.meta.title:
                    return object.meta.title
            return self.get_title()
        else:
            if name == 'description':
                if object.meta:
                    if object.meta.description:
                        return object.meta.description
                return self.get_description()
            else:
                if name == 'keywords':
                    if object.meta:
                        if object.meta.keywords:
                            return object.meta.keywords
                    return self.get_keywords()
                else:
                    if name == 'canonical_url':
                        if object.meta:
                            if object.meta.canonical_url:
                                return object.meta.canonical_url
                        return self.get_canonical_url()
        return ''