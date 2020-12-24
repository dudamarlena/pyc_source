# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Util/Chargen.py
# Compiled at: 2008-10-19 12:19:52
"""==========================
Simple Character Generator
==========================

This component is intended as a simple 'stream of characters' generator.

At the moment, it continually sends the string "Hello world" as fast as it can,
indefinitely out of its "outbox" outbox.

Example Usage
-------------
::
    >>> Pipeline( Chargen(), ConsoleEchoer() ).run()
    Hello WorldHello WorldHello WorldHello WorldHello WorldHello WorldHello WorldHel
    lo WorldHello WorldHello WorldHello WorldHello WorldHello WorldHello WorldHello
    WorldHello WorldHello WorldHello WorldHello WorldHello WorldHello WorldHello Wor
    ldHello WorldHello WorldHello WorldHello WorldHello WorldHello WorldHello WorldH
    ello WorldHello WorldHello WorldHello WorldHello WorldHello WorldHello WorldHell

    ... you get the idea!

    
How does it work?
-----------------

This component, once activated repeatedly emits the string "Hello World" from
its "outbox" outbox. It is emitted as a single string. It does this continuously
forever. It is not rate limited in any way, and so emits as fast as it can.

This component does not terminate, and ignores messages arriving at any of its
inboxes. It does not output anything from its "signal" outbox.
"""
import socket, Axon

class Chargen(Axon.Component.component):
    """   Chargen() -> new Chargen component.

   Component that emits a continuous stream of the string "Hello World" from its
   "outbox" outbox as fast as it can.
   """
    Inboxes = {'inbox': 'NOT USED', 'control': 'NOT USED'}
    Outboxes = {'outbox': 'NOT USED', 'signal': 'NOT USED'}

    def main(self):
        """Main loop."""
        while 1:
            self.send('Hello World', 'outbox')
            yield 1


def tests():
    from Axon.Scheduler import scheduler
    from Kamaelia.Util.Console import ConsoleEchoer

    class testComponent(Axon.Component.component):

        def main(self):
            chargen = Chargen()
            display = ConsoleEchoer()
            self.link((chargen, 'outbox'), (display, 'inbox'))
            self.addChildren(chargen, display)
            yield Axon.Ipc.newComponent(*self.children)
            while 1:
                self.pause()
                yield 1

    harness = testComponent()
    harness.activate()
    scheduler.run.runThreads(slowmo=0)


__kamaelia_components__ = (
 Chargen,)
if __name__ == '__main__':
    tests()