# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hasher/apps/workflow/workflowapp/admin.py
# Compiled at: 2016-03-14 09:45:17
from django.contrib import admin
from workflowapp.models import Transition
from .models import Workflow, State, Task, Assignee, Permission
admin.site.register(Workflow)
admin.site.register(State)
admin.site.register(Transition)
admin.site.register(Task)
admin.site.register(Assignee)
admin.site.register(Permission)