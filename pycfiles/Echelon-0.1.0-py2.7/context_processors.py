# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/echelon/context_processors.py
# Compiled at: 2011-09-24 06:25:11
from django.core.urlresolvers import reverse
from django.template import RequestContext
import echelon
from echelon import conf

def default(request):
    return {'request': request, 
       'ECHELON_TITLE': conf.TITLE, 
       'ECHELON_NAME': conf.NAME, 
       'ECHELON_MEDIA_PREFIX': (conf.MEDIA_PREFIX or reverse('echelon:media')).rstrip('/'), 
       'ECHELON_VERSION': echelon.VERSION}


def root_categories(request):
    from echelon.models import Category
    root_categories = Category.objects.filter(parent=None).exclude(slug='index')
    return {'root_categories': root_categories}


def settings(request):
    from echelon.models import SiteSettings
    try:
        settings = SiteSettings.objects.all()[0:1].get()
    except SiteSettings.DoesNotExist:
        settings = SiteSettings.objects.create()
        settings.save()

    return {'global_javascript': settings.global_javascript}