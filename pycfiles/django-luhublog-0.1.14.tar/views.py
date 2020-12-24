# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/johsanca/Projects/luhu-blog-app/luhublog/views.py
# Compiled at: 2015-10-20 16:35:47
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy
from django.conf import settings
from luhublog.models import Author, Entry
from . import app_settings

class EntryListView(ListView):
    model = Entry
    context_object_name = 'entries'
    template_name = 'luhublog/entry_list.html'


class EntryDetailView(DetailView):
    model = Entry
    context_object_name = 'entry'
    template_name = 'luhublog/entry_detail.html'