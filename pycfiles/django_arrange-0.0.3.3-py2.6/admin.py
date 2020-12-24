# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/arrange/admin.py
# Compiled at: 2011-02-05 04:22:02
from django.contrib import admin
from arrange.utils import is_arrangeable
for (model, model_admin) in admin.site._registry.items():
    if is_arrangeable(model):
        model_admin.change_list_template = 'arrange/arrange_change_list.html'