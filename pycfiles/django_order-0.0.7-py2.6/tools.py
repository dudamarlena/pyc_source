# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/order/tools.py
# Compiled at: 2011-09-15 05:06:32
from django.contrib import admin
from django.http import HttpResponseRedirect
import object_tools
from order.utils import is_orderable

class Order(object_tools.ObjectTool):
    name = 'order'
    label = 'Order'

    def view(self, request, extra_context=None):
        return HttpResponseRedirect('/admin/order/%sorderitem/' % extra_context['opts'].object_name.lower())


for (model, model_admin) in admin.site._registry.items():
    label = ('.').join([model._meta.app_label, model._meta.object_name])
    if is_orderable(label):
        object_tools.tools.register(Order, model)