# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vagrant/envs/conversocial/lib/python2.7/site-packages/djangosampler/plugins/celery_task.py
# Compiled at: 2015-11-17 05:08:04
from time import time
from celery.signals import task_prerun, task_postrun
from djangosampler.sampler import should_sample, sample
task_start_times = {}

def task_prerun_handler(task_id, task, args, kwargs, **kwds):
    task_start_times[task_id] = time()


def task_postrun_handler(task_id, task, args, kwargs, retval, **kwds):
    duration = time() - task_start_times[task_id]
    del task_start_times[task_id]
    if not should_sample(duration):
        return
    sample('celery', str(task), duration, [args, kwargs])


class Celery(object):
    """Plugin that hooks into Celery's signals to provide sampling of task
    duration.
    """

    @staticmethod
    def install():
        task_prerun.connect(task_prerun_handler)
        task_postrun.connect(task_postrun_handler)