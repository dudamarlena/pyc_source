# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stein/Projekte/eclipse/django-easy-contact/easy_contact/urls.py
# Compiled at: 2014-10-17 10:59:57
from django.conf.urls.defaults import *
urlpatterns = patterns('easy_contact', ('^success/$', 'views.thanks'), ('^contact/$',
                                                                        'views.contact'))