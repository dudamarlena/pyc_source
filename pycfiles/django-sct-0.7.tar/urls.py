# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/herbert/dev/python/sctdev/simpleproject/simpleproject/../../communitytools/sphenecoll/sphene/sphwiki/urls.py
# Compiled at: 2012-03-17 12:42:14
from django.conf.urls.defaults import *
urlpatterns = patterns('', (
 '^$', 'django.views.generic.simple.redirect_to', {'url': 'show/Start/'}))
snip = '(?P<snipName>[\\w/:\\-.]+?)'
urlpatterns += patterns('sphene.sphwiki.views', ('^recentchanges/$', 'recentChanges'), (
 '^show/' + snip + '/$', 'showSnip'), (
 '^pdf/' + snip + '/$', 'generatePDF'), (
 '^edit/' + snip + '/$', 'editSnip'), url('^editversion/' + snip + '/(?P<versionId>\\d+)/$', 'editSnip', name='sphwiki_editversion'), (
 '^history/' + snip + '/$', 'history'), (
 '^diff/' + snip + '/(?P<changeId>\\d+)/$', 'diff'), (
 '^attachments/edit/' + snip + '/(?P<attachmentId>\\d+)/$', 'attachmentEdit'), (
 '^attachments/create/' + snip + '/$', 'attachmentCreate'), (
 '^attachments/list/' + snip + '/$', 'attachment'), url('^tag/(?P<tag_name>\\w+)/$', 'show_tag_snips', name='sphwiki_show_tag_snips'))