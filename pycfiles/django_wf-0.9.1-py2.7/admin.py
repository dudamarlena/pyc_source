# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/django_workflow/admin.py
# Compiled at: 2017-08-28 08:25:01
from django.contrib import admin
from django_workflow.models import Workflow, State, Transition, Condition, Function, FunctionParameter, Callback, CallbackParameter, CurrentObjectState, TransitionLog
admin.site.register(Workflow)
admin.site.register(State)
admin.site.register(Transition)
admin.site.register(Condition)
admin.site.register(Function)
admin.site.register(FunctionParameter)
admin.site.register(Callback)
admin.site.register(CallbackParameter)
admin.site.register(CurrentObjectState)
admin.site.register(TransitionLog)