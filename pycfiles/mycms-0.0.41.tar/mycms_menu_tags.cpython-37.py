# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jnvilo/Projects/web/mycms/mycms/templatetags/mycms_menu_tags.py
# Compiled at: 2019-02-05 11:01:21
# Size of source mod 2**32: 1568 bytes
import logging
from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.template import Template, Context
from django.template.loader import get_template
from mycms.models import CMSPaths
from mycms.models import CMSEntries
register = template.Library()
logger = logging.getLogger('mycms.templatetags')

@register.inclusion_tag('mycms/templatetags/dropdown_menu.html')
def dropdown_menu(path):
    try:
        parent = CMSEntries.objects.get(path__path=path)
    except ObjectDoesNotExist as e:
        try:
            msg = 'No CMSEntries to produce dropdown_menu for path: {}'.format(path)
            logger.fatal(msg)
            parent = []
        finally:
            e = None
            del e

    return {'parent': parent}


@register.inclusion_tag('mycms/templatetags/full_menu.html')
def full_menu():
    """
    Used to get a full category tree starting from /cms/. 
    """
    try:
        parent = CMSEntries.objects.get(path__path='/')
    except ObjectDoesNotExist as e:
        try:
            msg = 'No CMSEntries to produce full_menu from /. Perhaps / does not yet exist!!'
            logger.fatal(msg)
            parent = None
        finally:
            e = None
            del e

    return {'parent': parent}


@register.inclusion_tag('mycms/templatetags/mini_menu.html')
def mini_menu():
    try:
        parent = CMSEntries.objects.get(path__path='/')
    except ObjectDoesNotExist as e:
        try:
            msg = 'No CMSEntries to produce full_menu from /. Perhaps / does not yet exist!!'
            logger.fatal(msg)
            parent = None
        finally:
            e = None
            del e

    return {'parent': parent}