# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/home/me/work/py27/lib/python2.7/site-packages/fabric_alias/__init__.py
# Compiled at: 2015-05-04 03:17:42


def set_alias(modules={}, seen_clear=False):
    from fabric.main import load_tasks_from_module, is_task_module, _seen
    from fabric.task_utils import _Dict
    from fabric import state
    new_style_tasks = _Dict()
    for name, module in modules.items():
        if is_task_module(module):
            docs, newstyle, classic, default = load_tasks_from_module(module)
            for task_name, task in newstyle.items():
                if name not in new_style_tasks:
                    new_style_tasks[name] = _Dict()
                new_style_tasks[name][task_name] = task

            if default is not None:
                new_style_tasks[name].default = default

    state.commands.update(new_style_tasks)
    if seen_clear:
        _seen.clear()
    return