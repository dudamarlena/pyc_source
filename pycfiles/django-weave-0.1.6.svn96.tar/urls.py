# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jens/workspace/django-weave/django_weave_env/src/django-weave/testproject/urls.py
# Compiled at: 2010-04-07 04:53:43
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
admin.autodiscover()
import weave.urls
from testproject.views import url_info
handler404 = 'django.views.defaults.page_not_found'
handler500 = 'django.views.defaults.server_error'
urlpatterns = patterns('', url('^$', url_info), url('^weave/', include(weave.urls), name='weave-root'), url('^admin/doc/', include('django.contrib.admindocs.urls')), url('^admin/', include(admin.site.urls)))