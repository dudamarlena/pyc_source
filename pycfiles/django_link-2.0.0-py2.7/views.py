# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hedley/django/instances/django-link/link/views.py
# Compiled at: 2017-07-06 07:47:29
from django.views import generic
from link.models import Link

class LinkDetailView(generic.detail.DetailView):
    model = Link
    template = 'link/link_detail.html'


class LinkListView(generic.list.ListView):
    model = Link
    template = 'link/link_list.html'