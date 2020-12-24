# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kapt/workspace/django-check-seo/django_check_seo/conf/settings.py
# Compiled at: 2020-03-02 10:12:05
# Size of source mod 2**32: 1262 bytes
from django.conf import settings
DJANGO_CHECK_SEO_SETTINGS = {'content_words_number':[
  300, 600], 
 'internal_links':1, 
 'external_links':1, 
 'meta_title_length':[
  30, 60], 
 'meta_description_length':[
  50, 160], 
 'keywords_in_first_words':50, 
 'max_link_depth':4, 
 'max_url_length':70}
DJANGO_CHECK_SEO_SETTINGS.update(getattr(settings, 'DJANGO_CHECK_SEO_SETTINGS', {}))
DJANGO_CHECK_SEO_AUTH = {}
DJANGO_CHECK_SEO_AUTH.update(getattr(settings, 'DJANGO_CHECK_SEO_AUTH', {}))
DJANGO_CHECK_SEO_FORCE_HTTP = False
DJANGO_CHECK_SEO_FORCE_HTTP = getattr(settings, 'DJANGO_CHECK_SEO_FORCE_HTTP', False)
DJANGO_CHECK_SEO_SEARCH_IN = {'type':'exclude', 
 'selectors':[
  'header', '.cover-section', '#footer']}
DJANGO_CHECK_SEO_EXCLUDE_CONTENT = getattr(settings, 'DJANGO_CHECK_SEO_EXCLUDE_CONTENT', '')