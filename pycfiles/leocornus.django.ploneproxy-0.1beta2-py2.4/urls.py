# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/leocornus/django/ploneproxy/urls.py
# Compiled at: 2010-05-30 08:27:16
from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('', (
 '^admin/', include(admin.site.urls)), ('^login/$', 'leocornus.django.ploneproxy.views.login'), ('^mail_password/$',
                                                                                                 'leocornus.django.ploneproxy.views.mailPassword'), ('^password_reset/$',
                                                                                                                                                     'leocornus.django.ploneproxy.views.passwordReset'), ('^logout/$',
                                                                                                                                                                                                          'leocornus.django.ploneproxy.views.logout'))