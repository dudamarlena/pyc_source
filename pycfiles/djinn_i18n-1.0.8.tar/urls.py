# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bouma/gitprojects/provgroningen/buildout/src/djinn_i18n/djinn_i18n/urls.py
# Compiled at: 2015-10-30 05:56:25
from django.conf.urls import patterns, include, url
from views.index import IndexView, SaveView, SearchView
from views.module import ModuleView
from views.trans import TransView
from views.po import POView
from views.reload import ReloadView
_urlpatterns = patterns('', url('^$', IndexView.as_view(), name='djinn_i18n_index'), url('^save$', SaveView.as_view(), name='djinn_i18n_save'), url('^reload$', ReloadView.as_view(), name='djinn_i18n_reload'), url('^trans/(?P<locale>[a-z]{2}(_[A-Z]{2})?)?/?$', TransView.as_view(), name='djinn_i18n_trans'), url('^search$', SearchView.as_view(), name='djinn_i18n_search'), url('^po/(?P<locale>[a-z]{2}(_[A-Z]{2})?)/$', POView.as_view(), name='djinn_i18n_po'), url('^(?P<module>[\\w-]*)/(?P<locale>[\\w-]*)/$', ModuleView.as_view(), name='djinn_i18n_module'))
urlpatterns = patterns('', (
 '^djinn/i18n/', include(_urlpatterns)))