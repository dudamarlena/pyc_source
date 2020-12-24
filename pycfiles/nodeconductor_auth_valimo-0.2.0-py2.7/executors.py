# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_auth_valimo/executors.py
# Compiled at: 2016-09-19 07:37:17
from celery import chain
from nodeconductor.core import executors
from .tasks import AuthTask, PollTask

class AuthExecutor(executors.ErrorExecutorMixin, executors.BaseExecutor):

    @classmethod
    def get_task_signature(cls, instance, serialized_instance):
        return chain(AuthTask().si(serialized_instance, state_transition='begin_processing'), PollTask().si(serialized_instance).set(countdown=30))