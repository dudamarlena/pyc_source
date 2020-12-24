# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/twisting/messages.py
# Compiled at: 2009-03-28 16:00:34
"""Some messages for queue status workflow.
"""

class Message(object):
    """Base message to communicate between queues.
    """

    def __init__(self, id_):
        """Init with a taskbox id for multi task management.
        """
        self.id_ = id_


class TaskMessage(Message):
    """Specific message for taskbox communication.
    """
    pass


class Pause(TaskMessage):
    """Pause message for taskbox.
    """
    pass


class Play(TaskMessage):
    """Play message for taskbox.
    """
    pass


class Stop(TaskMessage):
    """Stop message for taskbox.
    """
    pass