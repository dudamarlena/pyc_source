# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/craterdome/work/django_common/lib/python2.7/site-packages/django_common/context_processors.py
# Compiled at: 2012-03-11 19:20:35
from django.conf import settings as django_settings

def common_settings(request):
    return {'domain_name': django_settings.DOMAIN_NAME, 
       'www_root': django_settings.WWW_ROOT, 
       'is_dev': django_settings.IS_DEV, 
       'is_prod': django_settings.IS_PROD}