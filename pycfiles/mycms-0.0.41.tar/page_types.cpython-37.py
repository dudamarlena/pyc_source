# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jnvilo/Projects/web/mycms/mycms/view_handlers/page_types.py
# Compiled at: 2019-02-05 11:01:21
# Size of source mod 2**32: 5311 bytes
from mycms.models import CMSEntries
from mycms.models import CMSPageTypes
from mycms.view_handlers.mycms_view import ViewObject
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.utils import OperationalError
import logging
logger = logging.getLogger('mycms.page_handlers')
try:
    try:
        singlepageview_pagetype_obj, c = obj = CMSPageTypes.objects.get_or_create(page_type='SINGLEPAGE', text='Single Page HTML',
          view_class='SinglePage',
          view_template='SinglePage.html')
    except ObjectDoesNotExist as e:
        try:
            singlepageview_pagetype_obj = CMSPageTypes(page_type='SINGLEPAGE', text='Single Page HTML',
              view_class='SinglePage',
              view_template='SinglePage.html')
            singlepageview_pagetype_obj.save()
        finally:
            e = None
            del e

    except MultipleObjectsReturned as e:
        try:
            msg = 'Got more than 1 CMSPageTypes : SINGLEPAGE. Database is inconsistent, Will return the first one. '
            logger.warn(msg)
            singlepageview_pagetype_obj = CMSPageTypes.objects.filter(page_type='SINGLEPAGE')[0]
        finally:
            e = None
            del e

    try:
        categorypageview_pagetype_obj = CMSPageTypes.objects.get(page_type='CATEGORY')
    except ObjectDoesNotExist as e:
        try:
            msg = 'Could not load CATEGORY view object. Going to create it.'
            logger.debug(msg)
            pagetype_obj, _ = CMSPageTypes.objects.get_or_create(page_type='CATEGORY', text='Category Page',
              view_class='CategoryPage',
              view_template='CategoryPage.html')
        finally:
            e = None
            del e

    except MultipleObjectsReturned as e:
        try:
            msg = 'Got more than 1 CMSPageType: CATEGORY. Database is inconsistent. Will return the first one.'
            logger.info(msg)
            categorypageview_pagetype_obj = CMSPageTypes.objects.filter(page_type='CATEGORY')[0]
        finally:
            e = None
            del e

    try:
        multipageview_pagetype_obj = CMSPageTypes.objects.get(page_type='MULTIPAGE')
    except ObjectDoesNotExist as e:
        try:
            msg = 'Could not load MULTIPAGE view object. Going to create it.'
            logger.debug(msg)
            multipageview_pagetype_obj, _ = CMSPageTypes.objects.get_or_create(page_type='MULTIPAGE', text='MultPage Article',
              view_class='MultiPage',
              view_template='MultiPage.html')
        finally:
            e = None
            del e

    except MultipleObjectsReturned as e:
        try:
            msg = 'Got more than 1 CMSMultiPageType: MULTIPAGE. Database is inconsistent. Will return the first one.'
            logger.info(msg)
            multipageview_pagetype_obj = CMSMultiPageTypes.objects.filter(page_type='MULTIPAGE')[0]
        finally:
            e = None
            del e

    try:
        memberpageview_pagetype_obj = CMSPageTypes.objects.get(page_type='MEMBERPAGE')
    except ObjectDoesNotExist as e:
        try:
            msg = 'Could not load MULTIPAGE view object. Going to create it.'
            logger.debug(msg)
            pagetype_obj, _ = CMSPageTypes.objects.get_or_create(page_type='MEMBERPAGE', text='MemberPage Article',
              view_class='MemberPage',
              view_template='MemberPage.html')
        finally:
            e = None
            del e

    except MultipleObjectsReturned as e:
        try:
            msg = 'Got more than 1 CMSMultiPageType: MULTIPAGE. Database is inconsistent. Will return the first one.'
            logger.info(msg)
            memberpageview_pagetype_obj = CMSMultiPageTypes.objects.filter(page_type='MEMBERPAGE')[0]
        finally:
            e = None
            del e

    try:
        allarticles_pagetype_obj, c = obj = CMSPageTypes.objects.get_or_create(page_type='ALLARTICLES', text='All Articles ',
          view_class='AllArticlesPage',
          view_template='AllArticlesPage.html')
    except ObjectDoesNotExist as e:
        try:
            allarticles_pagetype_obj = CMSPageTypes(ppage_type='ALLARTICLES', text='All Articles ',
              view_class='AllArticlesPage',
              view_template='AllArticlesPage.html')
            allarticles_pagetype_obj.save()
        finally:
            e = None
            del e

    except MultipleObjectsReturned as e:
        try:
            msg = 'Got more than 1 CMSPageTypes : SINGLEPAGE. Database is inconsistent, Will return the first one. '
            logger.warn(msg)
            allarticles_pagetype_obj = CMSPageTypes.objects.filter(page_type='ALLARTICLES')[0]
        finally:
            e = None
            del e

except OperationalError as e:
    try:
        pass
    finally:
        e = None
        del e