# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/idapload/inspectlocust.py
# Compiled at: 2020-04-15 05:33:11
# Size of source mod 2**32: 1617 bytes
import inspect
from .core import Locust, TaskSet
from .log import console_logger

def print_task_ratio(idaploads, total=False, level=0, parent_ratio=1.0):
    d = get_task_ratio_dict(idaploads, total=total, parent_ratio=parent_ratio)
    _print_task_ratio(d)


def _print_task_ratio(x, level=0):
    for k, v in x.items():
        padding = '  ' * level
        ratio = v.get('ratio', 1)
        console_logger.info(' %-10s %-50s' % (padding + '%-6.1f' % (ratio * 100), padding + k))
        if 'tasks' in v:
            _print_task_ratio(v['tasks'], level + 1)


def get_task_ratio_dict(tasks, total=False, parent_ratio=1.0):
    """
    Return a dict containing task execution ratio info
    """
    if hasattr(tasks[0], 'weight'):
        divisor = sum((t.weight for t in tasks))
    else:
        divisor = len(tasks) / parent_ratio
    ratio = {}
    for task in tasks:
        ratio.setdefault(task, 0)
        ratio[task] += task.weight if hasattr(task, 'weight') else 1

    ratio_percent = dict(((k, float(v) / divisor) for k, v in ratio.items()))
    task_dict = {}
    for idapload, ratio in ratio_percent.items():
        d = {'ratio': ratio}
        if inspect.isclass(idapload):
            if issubclass(idapload, Locust):
                T = idapload.task_set.tasks
            else:
                if issubclass(idapload, TaskSet):
                    T = idapload.tasks
                elif total:
                    d['tasks'] = get_task_ratio_dict(T, total, ratio)
                else:
                    d['tasks'] = get_task_ratio_dict(T, total)
        task_dict[idapload.__name__] = d

    return task_dict