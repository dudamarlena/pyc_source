# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/emencia/django/links/views.py
# Compiled at: 2010-01-14 11:17:33
"""views for emencia.django.links"""
from django.views.generic import list_detail
from emencia.django.links.models import Link

def links_by_language(request):
    language = request.LANGUAGE_CODE
    return list_detail.object_list(request, queryset=Link.published.filter(language=language), template_name='links/links_by_language.html', template_object_name='links')