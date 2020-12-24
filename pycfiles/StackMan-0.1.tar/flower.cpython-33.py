# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/coltonprovias/Development/zymio/stackman/stackman/common/flower.py
# Compiled at: 2013-12-13 03:37:05
# Size of source mod 2**32: 667 bytes
"""
StackMan
Colton J. Provias - cj@coltonprovias.com
"""
from stackman.stack import StackItem

class Flower(StackItem):
    __doc__ = '\n    Let a flower blossom on top of Celery.\n\n    Arguments:\n    * base_command str Command\n                  Default: flower\n    * port int Port to bind to\n               Default: 5555\n    * broker str Broker\n                 Default: amqp://guest@localhost:5672//\n    '
    ready_text = 'Connected to'

    @property
    def command(self):
        fmap = {'base': self.base_command,  'port': self.port, 
         'broker': self.broker}
        return '{base} --port={port} --broker_api={broker}'.format_map(fmap)