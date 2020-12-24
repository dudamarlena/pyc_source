# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/helpdesk/views/kb.py
# Compiled at: 2020-02-26 14:48:40
# Size of source mod 2**32: 1917 bytes
"""
django-helpdesk - A Django powered ticket tracker for small enterprise.

(c) Copyright 2008 Jutda. All Rights Reserved. See LICENSE for details.

views/kb.py - Public-facing knowledgebase views. The knowledgebase is a
              simple categorised question/answer system to show common
              resolutions to common problems.
"""
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
import tendenci.apps.theme.shortcuts as render_to_resp
import tendenci.apps.helpdesk as helpdesk_settings
from tendenci.apps.helpdesk.models import KBCategory, KBItem

def index(request):
    category_list = KBCategory.objects.all()
    return render_to_resp(request=request, template_name='helpdesk/kb_index.html', context={'kb_categories':category_list, 
     'helpdesk_settings':helpdesk_settings})


def category(request, slug):
    category = get_object_or_404(KBCategory, slug__iexact=slug)
    items = category.kbitem_set.all()
    return render_to_resp(request=request, template_name='helpdesk/kb_category.html', context={'category':category, 
     'items':items, 
     'helpdesk_settings':helpdesk_settings})


def item(request, item):
    item = get_object_or_404(KBItem, pk=item)
    return render_to_resp(request=request, template_name='helpdesk/kb_item.html', context={'item':item, 
     'helpdesk_settings':helpdesk_settings})


def vote(request, item):
    item = get_object_or_404(KBItem, pk=item)
    vote = request.GET.get('vote', None)
    if vote in ('up', 'down'):
        item.votes += 1
        if vote == 'up':
            item.recommendations += 1
        item.save()
    return HttpResponseRedirect(item.get_absolute_url())