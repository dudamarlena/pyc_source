# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Util/DataSource.py
# Compiled at: 2008-10-19 12:19:52
"""=====================
Data Source component
=====================

This component outputs messages specified at its creation one after another.

Example Usage
-------------

To output "hello" then "world"::
  
    pipeline(
        DataSource(["hello", "world"]),
        ConsoleEchoer()
    ).run()

    

==========================
Triggered Source component
==========================

Whenever this component receives a message on inbox, it outputs a certain message.

Example Usage
-------------

To output "wibble" each time a line is entered to the console::

    pipeline(
        ConsoleReader(),
        TriggeredSource("wibble"),
        ConsoleEchoer()
    ).run()

"""
from Axon.Component import component
from Axon.Ipc import producerFinished, shutdown
from PureTransformer import PureTransformer

class DataSource(component):

    def __init__(self, messages):
        super(DataSource, self).__init__()
        self.messages = messages

    def main(self):
        while len(self.messages) > 0:
            yield 1
            self.send(self.messages.pop(0), 'outbox')

        yield 1
        self.send(producerFinished(self), 'signal')


def TriggeredSource(msg):
    return PureTransformer(lambda r: msg)


__kamaelia_components__ = (
 DataSource,)
__kamaelia_prefabs__ = (TriggeredSource,)
if __name__ == '__main__':
    from Kamaelia.Chassis.Pipeline import pipeline
    from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
    pipeline(DataSource(['hello', ' ', 'there', ' ', 'how', ' ', 'are', ' ', 'you', ' ', 'today\r\n', '?', '!']), ConsoleEchoer()).run()