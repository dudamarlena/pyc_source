# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/twisting/task_interface.py
# Compiled at: 2009-03-28 16:00:34
"""
"""
from zope.interface import Interface, Attribute

class ITask(Interface):
    """
    """
    id_ = Attribute('Mandatory')
    pretty_name = Attribute('Mandatory')
    task_event_queue = Attribute('Mandatory')
    task_event_queue = Attribute('Mandatory')
    is_finished = Attribute('Mandatory')
    is_playing = Attribute('Mandatory')
    is_playing = Attribute('Mandatory')
    max_pulse = Attribute('Mandatory')
    current_pulse = Attribute('Mandatory')
    fraction_step = Attribute('Mandatory')
    remove_callback = Attribute('Mandatory')
    finish_callback = Attribute('Mandatory')
    set_max_pulse = Attribute('Mandatory')
    pulse = Attribute('Mandatory')
    on_play = Attribute('Mandatory')
    play = Attribute('Mandatory')
    on_stop = Attribute('Mandatory')
    stop = Attribute('Mandatory')
    finish = Attribute('Mandatory')
    set_progress_end_state = Attribute('Mandatory')
    on_remove = Attribute('Mandatory')
    remove = Attribute('Mandatory')
    set_title = Attribute('Mandatory')
    set_text = Attribute('Mandatory')