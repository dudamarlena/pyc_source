# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/service/beans.py
# Compiled at: 2017-09-08 11:08:24
# Size of source mod 2**32: 522 bytes
from service import task_service
from service import salt
from service import simple
from common import constants
from service import event_service
from service import user_service
from service import command_service
beans = {constants.SERVICE_TASK: task_service.TaskService, 
 'simple': simple.SimpleNativeExecutor, 
 constants.SERVICE_EVENT_MANAGER: event_service.EventManager, 
 constants.SERVICE_USER_MANAGER: user_service.UserManager, 
 constants.SERVICE_COMMAND_PROCESSOR: command_service.Processor}