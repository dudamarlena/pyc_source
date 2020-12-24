# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/coltonprovias/Development/zymio/stackman/stackman/common/rabbitmq.py
# Compiled at: 2013-12-13 03:37:26
# Size of source mod 2**32: 296 bytes
"""
StackMan
Colton J. Provias - cj@coltonprovias.com
"""
from stackman.stack import StackItem

class RabbitMQ(StackItem):
    __doc__ = '\n    Start a RabbitMQ message queue.\n\n    Arguments:\n    * command str Command\n                  Default: rabbitmq-server\n    '
    ready_text = 'broker running'