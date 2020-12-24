# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stein/Projekte/eclipse/django-dynamic-link/dynamicLink/presettings.py
# Compiled at: 2013-04-20 06:43:53
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
DYNAMIC_LINK_MEDIA = getattr(settings, 'DYNAMIC_LINK_MEDIA', settings.MEDIA_ROOT)
DYNAMIC_LINK_URL_BASE_COMPONENT = getattr(settings, 'DYNAMIC_LINK_URL_BASE_COMPONENT', 'serve')
TEXT_REQUEST_DOES_NOT_EXIST = _('This request is faulty')
TEXT_REQUEST_IS_EXPIRED = _('Sorry, this request is already expired')