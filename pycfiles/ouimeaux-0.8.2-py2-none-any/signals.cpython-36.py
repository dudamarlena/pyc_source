# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ian/src/github.com/iancmcc/ouimeaux/ouimeaux/signals.py
# Compiled at: 2018-08-26 09:51:15
# Size of source mod 2**32: 773 bytes
from ouimeaux.pysignals import Signal, StateChange, receiver
import sys
_main = sys.modules.get('__main__')
if _main:
    _main.__file__ = '__main__.py'
discovered = Signal(providing_args=['address', 'headers'])
devicefound = Signal()
subscription = Signal(providing_args=['type', 'value'])
statechange = StateChange(providing_args=['state'])

@receiver(subscription)
def _got_subscription(sender, **kwargs):
    if kwargs['type'] == 'BinaryState':
        statechange.send(sender, state=(int(kwargs['value'])))