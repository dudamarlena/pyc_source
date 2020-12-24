# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/val/Projects/workon/mpro/doozdev/backend/restful-backend/apps/geoware/management/utils/updater.py
# Compiled at: 2017-01-11 14:20:30
# Size of source mod 2**32: 1480 bytes
import logging
from django.utils.translation import ugettext as _
from ...models import *
logger = logging.getLogger('geoware.utils.updater')

def create_or_update_continent(code, name=''):
    obj = None
    created = False
    if code:
        try:
            obj = Continent.objects.get(code__iexact=code)
            created = True
        except:
            obj = Continent()

        obj.code = code
        if name:
            obj.name = name
        obj.save()
        if created:
            logger.debug(_('Adding continent {0} ({1})'.format(name, code)))
        return obj


def create_or_update_currency(code, name=''):
    obj = None
    created = False
    if code:
        try:
            obj = Currency.objects.get(code__iexact=code)
            created = True
        except:
            obj = Currency()

        obj.code = code
        if name:
            obj.name = name
        obj.save()
        if created:
            logger.debug(_('Adding currency {0} ({1})'.format(name, code)))
        return obj


def create_or_update_language(code, name=''):
    obj = None
    created = False
    if code:
        try:
            obj = Language.objects.get(code__iexact=code)
            created = True
        except:
            obj = Language()

        obj.code = code
        if name:
            obj.name = name
        obj.save()
        if created:
            logger.debug(_('Adding language {0} ({1})'.format(name, code)))
        return obj