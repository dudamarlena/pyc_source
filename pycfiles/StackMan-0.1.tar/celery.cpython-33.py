# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/coltonprovias/Development/zymio/stackman/stackman/common/celery.py
# Compiled at: 2013-12-13 03:36:50
# Size of source mod 2**32: 669 bytes
"""
StackMan
Colton J. Provias - cj@coltonprovias.com
"""
from stackman.stack import StackItem

class Celery(StackItem):
    __doc__ = '\n    Celery eats RabbitMQs...okay.  Anyway, start a Celery worker.\n\n    Arguments:\n    * base_command str Base Command\n                       Default: celery\n    * module str Celery Module\n                 Default: project.celery\n    * enable_beats bool Enable Celery Beats\n                 Default: True\n    '
    ready_text = 'ready'

    @property
    def command(self):
        command = [self.base_command, '-A', self.module, 'worker']
        if self.enable_beats:
            command.append('-B')
        return ' '.join(command)