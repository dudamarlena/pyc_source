# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hedley/django/instances/django-navbuilder/navbuilder/views.py
# Compiled at: 2017-01-25 06:30:30
from django.views import generic
from navbuilder.models import Menu

class MenuDetailView(generic.detail.DetailView):
    model = Menu


class MenuListView(generic.list.ListView):
    model = Menu