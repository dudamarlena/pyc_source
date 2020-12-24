# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\develop\code\Python\scape\scape\template\project_name\executors\executor.py
# Compiled at: 2020-04-20 06:53:39
# Size of source mod 2**32: 222 bytes
from scape.action.executor import ActionExecutor

class ExecutorDemo(ActionExecutor):

    def __init__(self):
        super().__init__()

    @staticmethod
    def print_to_screen(status):
        print(status)