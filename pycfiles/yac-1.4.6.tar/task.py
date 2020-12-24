# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/x0ox/Dropbox/ActiveDev/yac/yac/lib/task.py
# Compiled at: 2017-11-16 20:28:41
import os, imp
from yac.lib.intrinsic import apply_custom_fxn
from yac.lib.variables import get_variable, set_variable
from yac.lib.file import get_localized_script_path
from yac.lib.inputs import get_inputs

def get_task(task_name, service_parameters):
    task = {}
    tasks = get_variable(service_parameters, 'tasks', {})
    if tasks:
        if task_name in tasks.keys():
            task = tasks[task_name]
    return task


def get_task_names(service_parameters):
    task_names = []
    tasks = get_variable(service_parameters, 'tasks', {})
    if tasks:
        task_names = tasks.keys()
    return task_names


def get_task_script(task_name, service_parameters):
    task_script = ''
    tasks = get_variable(service_parameters, 'tasks', {})
    if tasks and get_variable(tasks, task_name):
        task_script = get_variable(tasks, task_name)['script']
    return task_script


def get_task_inputs(task_name, service_parameters):
    inputs = {}
    conditional_inputs = {}
    tasks = get_variable(service_parameters, 'tasks', {})
    if tasks and get_variable(tasks, task_name) and 'inputs' in get_variable(tasks, task_name):
        inputs = get_variable(tasks, task_name)['inputs']
    if tasks and get_variable(tasks, task_name) and 'conditional-inputs' in get_variable(tasks, task_name):
        conditional_inputs = get_variable(tasks, task_name)['conditional-inputs']
    return (inputs, conditional_inputs)


def run_task(task_name, service_parameters, stack_template):
    return_val = ''
    script_rel_path = get_task_script(task_name, service_parameters)
    inputs, conditional_inputs = get_task_inputs(task_name, service_parameters)
    script_path = get_localized_script_path(script_rel_path, service_parameters)
    if not script_path or not os.path.exists(script_path):
        print 'task %s executable does not exist' % script_path
    else:
        module_name = 'yac.lib.customizations'
        script_module = imp.load_source(module_name, script_path)
        return_val = script_module.task_handler(service_parameters, stack_template, inputs, conditional_inputs)
    return return_val


def handle_task_inputs(inputs, conditional_inputs):
    task_params = {}
    task_params = {'task-inputs': {'inputs': inputs, 'conditional-inputs': conditional_inputs}}
    get_inputs(task_params, 'task-inputs')
    return task_params