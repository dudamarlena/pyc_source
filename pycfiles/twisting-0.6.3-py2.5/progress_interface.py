# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/twisting/progress_interface.py
# Compiled at: 2009-03-28 16:00:34
"""
"""
from zope.interface import Interface, Attribute

class IProgress(Interface):
    """
    """
    initialized = Attribute('Mandatory')
    task_dict = Attribute('Mandatory')
    add_task = Attribute('Mandatory')
    start_task = Attribute('Mandatory')
    stop_task = Attribute('Mandatory')
    stop_all_tasks = Attribute('Mandatory')
    remove_task = Attribute('Mandatory')
    remove_all_tasks = Attribute('Mandatory')
    pulse = Attribute('Mandatory')
    task_finish = Attribute('Mandatory')