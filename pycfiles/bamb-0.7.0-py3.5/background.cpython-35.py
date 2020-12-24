# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rest/background.py
# Compiled at: 2017-09-08 11:38:51
# Size of source mod 2**32: 3197 bytes
from service import built_in_executors as be
from rest import tasks
from bamb import Bamb
from celery import group
from domain import base
from domain import exceptions
from common import constants
from service import event_service
from bamb import Bamb
from domain import base
import copy

class BackgroundExecutorImpl(be.BackgroundExecutor):

    def execute(self, executor_name, target_dict, parm_dict=None, eager=False):
        s = BackgroundExecutorImpl.get_signature(executor_name, target_dict, parm_dict)
        if eager:
            res = s.apply_async()
        else:
            res = s()
        res.get()
        em = Bamb.bean(constants.SERVICE_EVENT_MANAGER)
        if not isinstance(em, event_service.EventManager):
            return
        p = base.EasySerializable.es_load(parm_dict[constants.PARM_TASK_ID])
        task_id = p.value
        p = base.EasySerializable.es_load(parm_dict[constants.PARM_CURRENT_PATH])
        path = p.value
        e = base.Event(event_id=constants.EVENT_ID_TASK_STATE_CHANGED, data={constants.PARM_TASK_ID: task_id, 
         constants.PARM_CURRENT_PATH: path})
        em.dispatch(e)

    @staticmethod
    def get_signature(executor_name, target_dict, parm_dict=None):
        target = base.EasySerializable.es_load(target_dict)
        if not isinstance(target, base.Target):
            raise exceptions.IllegalArgumentException('invalid target dict!')
        if target.is_leaf:
            s = tasks.execute_on_target.s(executor_name, target_dict, parm_dict)
            return s
        sg = []
        parm_path = base.EasySerializable.es_load(parm_dict[constants.PARM_CURRENT_PATH])
        base_path = parm_path.value
        if not isinstance(parm_path, base.Parameter):
            raise exceptions.InternalErrorException('invalid parameter!')
        for i, t in enumerate(target.lt_children):
            if not isinstance(t, base.Target):
                raise exceptions.AppException('the children element is not a target instance!')
            td = t.es_to_dict()
            path = copy.copy(base_path)
            path.append(i)
            parm_path.value = path
            p = copy.copy(parm_dict)
            p[constants.PARM_CURRENT_PATH] = parm_path.es_to_dict()
            s = BackgroundExecutorImpl.get_signature(executor_name, td, p)
            sg.append(s)

        s = group(sg)
        return s

    @staticmethod
    def send_progress_event(body):
        print(body)


class BackgroundEventDispatcher(event_service.BackgroundDispatcher):

    def dispatch(self, e, queue, callback):
        s = tasks.background_dispatch.s(e=e, queue_name=queue, callback_service_name=callback)
        s.delay(queue=queue)


class BackgroundBroadcastDeliver(event_service.BackgroundBroadcastSender):

    def send(self, e):
        e_dict = base.EasySerializable.es_any_to_primary(e)
        s = tasks.background_broadcast_send.s(e_dict)
        s.delay()