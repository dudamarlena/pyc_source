# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jnvilo/Projects/web/mycms/mycms/templatetags/mycms_content_tags.py
# Compiled at: 2019-02-05 11:01:21
# Size of source mod 2**32: 907 bytes
from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.template import Template, Context
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from mycms.models import CMSPaths
from mycms.models import CMSEntries
register = template.Library()

@register.inclusion_tag('mycms/templatetags/frontpage.html')
def frontpage():
    cmsentries = CMSEntries.objects.filter(frontpage=True, published=True).order_by('-date_created')[:10]
    paginator = Paginator(cmsentries, 4)
    return {'cmsentries': cmsentries}


@register.inclusion_tag('mycms/templatetags/archives.html')
def archives():
    pass