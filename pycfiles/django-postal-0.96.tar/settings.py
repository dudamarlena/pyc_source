# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mick/src/django-postal/src/postal/settings.py
# Compiled at: 2010-11-19 03:33:52
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
POSTAL_ADDRESS_L10N = getattr(settings, 'POSTAL_ADDRESS_L10N', True)
POSTAL_ADDRESS_LINE1 = getattr(settings, 'POSTAL_ADDRESS_LINE1', (_('Street'), False))
POSTAL_ADDRESS_LINE2 = getattr(settings, 'POSTAL_ADDRESS_LINE2', (_('Area'), False))
POSTAL_ADDRESS_CITY = getattr(settings, 'POSTAL_ADDRESS_CITY', (_('City'), False))
POSTAL_ADDRESS_STATE = getattr(settings, 'POSTAL_ADDRESS_STATE', (_('State'), False))
POSTAL_ADDRESS_CODE = getattr(settings, 'POSTAL_ADDRESS_CODE', (_('Zip code'), False))