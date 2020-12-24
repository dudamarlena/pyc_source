# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/botnee/web/urls.py
# Compiled at: 2012-08-16 08:08:42
from django.conf.urls.defaults import patterns, url
import settings
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('', url('home/', 'web.interface.views.home'), url('query/', 'web.interface.views.query'), url('dump/', 'web.interface.views.dump'), url('force_reindex/', 'web.interface.views.force_reindex'), url('delete/', 'web.interface.views.delete'), url('flush/', 'web.interface.views.flush'), url('matrix/', 'web.interface.views.get_matrix_summary'), url('meta/', 'web.interface.views.meta'), url('recalculate_idf/', 'web.interface.views.recalculate_idf'), url('dump_dictionaries/', 'web.interface.views.dump_dictionaries'), url('^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'show_indexes': True}))
handler500 = 'web.interface.views.handler500'