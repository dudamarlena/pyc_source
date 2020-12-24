# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dadasu/demo/django/dj-translate/autotranslate/urls.py
# Compiled at: 2016-10-05 04:46:56
from django.conf.urls import url
from .views import home, list_languages, download_file, lang_sel, translate_text, ref_sel
urlpatterns = [
 url('^$', home, name='autotranslate-home'),
 url('^pick/$', list_languages, name='autotranslate-pick-file'),
 url('^download/$', download_file, name='autotranslate-download-file'),
 url('^select/(?P<langid>[\\w\\-_\\.]+)/(?P<idx>\\d+)/$', lang_sel, name='autotranslate-language-selection'),
 url('^select-ref/(?P<langid>[\\w\\-_\\.]+)/$', ref_sel, name='autotranslate-reference-selection'),
 url('^translate/$', translate_text, name='translate_text')]