# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/flanker/Developer/Github/Updoc/updoc/urls.py
# Compiled at: 2017-07-10 01:59:22
# Size of source mod 2**32: 1405 bytes
from django.conf.urls import url
from updoc import views
__author__ = 'Matthieu Gallet'
app_name = 'updoc'
urlpatterns = [
 url('^show_alt/proxy\\.pac$', (views.show_proxies), name='show_proxies'),
 url('^favorite\\.html', (views.show_favorite), name='show_favorite'),
 url('^favorite/(?P<root_id>\\d+).html$', (views.show_favorite), name='show_favorite'),
 url('^my_docs\\.html$', (views.my_docs), name='my_docs'),
 url('^delete_url/(?P<url_id>\\d+)\\.html$', (views.delete_url), name='delete_url'),
 url('^delete_doc/(?P<doc_id>\\d+)\\.html$', (views.delete_doc), name='delete_doc'),
 url('^show/(?P<doc_id>\\d+)/(?P<path>.*)$', (views.show_doc), name='show_doc'),
 url('^show_alt/(?P<doc_id>\\d+)/(?P<path>.*)$', (views.show_doc_alt), name='show_doc_alt'),
 url('^download/(?P<doc_id>\\d+)\\.(?P<fmt>zip|bz2|gz|xz)$', (views.compress_archive), name='compress_archive'),
 url('^show_search_results\\.html$', (views.show_search_results), name='show_search_results'),
 url('^show_all_docs\\.html$', (views.show_all_docs), name='show_all_docs'),
 url('^docsets/docset-(?P<doc_id>\\d+)/(?P<doc_name>.*)\\.xml$', (views.docset_feed), name='docset_feed'),
 url('^docsets/docset-(?P<doc_id>\\d+)\\.tgz$', (views.docset), name='docset'),
 url('^docsets/docset-(?P<doc_id>\\d+)\\.tgz\\.tarix$', (views.docset_tarix), name='docset_tarix')]