# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Chassis/Carousel.py
# Compiled at: 2008-10-19 12:19:52
"""==========================
Component Carousel Chassis
==========================

This component lets you create and wire up another component. You can then
swap it for a new one by sending it a message. The message contents is used by
a factory function to create the new replacement component.

The component that is created is a child contained within Carousel. Wire up to
Carousel's "inbox" inbox and "outbox" outbox to send and receive messages from
the child.

Example Usage
-------------

A reusable file reader::

    def makeFileReader(filename):
        return ReadFileAdapter(filename = filename, ...other args... )

    reusableFileReader = Carousel(componentFactory = makeFileReader)

Whenever you send a filename to the "next" inbox of the reusableFileReader
component, it will read that file. You can do this as many times as you wish.
The data read from the file comes out of the carousel's outbox.

Why is this useful?
-------------------

This chassis component is for making a carousel of components. It gets its name
from a broadcast carousel - where a programme (or set of programmes) is
broadcast one after another, often on a loop. Alternatively, think of public
information screens which display a looping carousel of slides of information.

You gain reusability from things that are not directly reusable and normally
come to a halt. For example, make a carousel of file reader components, and you
can read from more than one file, one after another. The carousel will make a
new file reader component every time you make new request.

The Carousel automatically sends a "NEXT" message when a component finishes, to
prompt you make a new request.

How does it work?
-----------------

The carousel chassis creates and encapsulates (as a child) the component you
want it to, and lets it get on with it.

Anything sent to the carousel's "inbox" inbox is passed onto the child
component. Anything the child sends out appears at the carousel's "outbox"
outbox.

If the child terminates, then the carousel unwires it and sends a "NEXT"
message out of its "requestNext" outbox (unless of course it has been told to
shutdown).

Another component, such as a Chooser, can respond to this message by sending
the new set of arguments (for the factory function) to the carousel's "next"
inbox. The carousel then uses your factory function to create a new child
component. This way, a sequence of operations can be automatically chained
together.

If the argument source needs to receive a "NEXT" message before sending its
first set of arguments, then set the argument make1stRequest=True when creating
the carousel.

You can actually send new orders to the "next" inbox at any time, not just in
response to requests from the Carousel. The carousel will immediately ask that
child to terminate; then as soon as it has done so, it will create the new one
and wire it in in its place.

If Carousel receives an Axon.Ipc.producerFinished message on its "control" inbox
then it will finish handling any pending messages on its "next" inbox (in the
way described above) then when there are none left, it will ask the child
component to shut down by sending on the producerFinished message to the child.
As soon as the child has terminated, the Carousel will terminate and send on the
producerFinished message out of its own "signal" outbox.

If Carousel receives an Axon.Ipc.shutdownMicroprocess message on its "control"
inbox then it will immediately send it on to its child component to ask it
to terminate. As soon as the child has termianted, the Carousel will terminate
and send on the shutdownMicroprocess message out of its own "signal" outbox.

Of course, if the Carousel has no child at the time either shutdown request is
received, it will immediately terminate and send on the message out of its
"signal" outbox.
"""
import Axon
from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess, newComponent

class Carousel(component):
    """
    Carousel(componentFactory,[make1stRequest]) -> new Carousel component
        
    Create a Carousel component that makes child components one at a time
    (in carousel fashion) using the supplied factory function.

    Keyword arguments:
    
    - componentFactory  -- function that takes a single argument and returns a component
    - make1stRequest    -- if True, Carousel will send an initial "NEXT" request. (default=False)
    """
    Inboxes = {'inbox': "child's inbox", 'next': 'requests to replace child', 
       'control': ''}
    Outboxes = {'outbox': "child's outbox", 'signal': '', 
       '_signal': "internal use: for sending 'shutdownMicroprocess' to child", 
       'requestNext': 'for requesting new child component'}

    def __init__(self, componentFactory, make1stRequest=False):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(Carousel, self).__init__()
        self.factory = componentFactory
        self.childDone = False
        self.make1stRequest = make1stRequest
        self.mustStop = None
        self.pleaseStop = None
        return

    def main(self):
        if self.make1stRequest:
            self.requestNext()
        while 1:
            while len(self.childComponents()) == 0:
                self.handleChildTerminations()
                (mustStop, pleaseStop) = self.checkControl()
                if mustStop:
                    self.send(mustStop, 'signal')
                    return
                elif self.dataReady('next'):
                    self.instantiateNewChild(self.recv('next'))
                elif pleaseStop:
                    self.send(pleaseStop, 'signal')
                    return
                elif len(self.childComponents()) == 0:
                    self.pause()
                    yield 1

            yield 1
            alreadyTerminatingChild = False
            while len(self.childComponents()) > 0:
                self.handleChildTerminations()
                (mustStop, pleaseStop) = self.checkControl()
                if mustStop and not alreadyTerminatingChild:
                    self.shutdownChild(mustStop)
                    alreadyTerminatingChild = True
                elif self.dataReady('next') and not alreadyTerminatingChild:
                    self.shutdownChild(shutdownMicroprocess())
                    alreadyTerminatingChild = True
                elif pleaseStop and not alreadyTerminatingChild:
                    self.shutdownChild(pleaseStop)
                    alreadyTerminatingChild = True
                elif len(self.childComponents()) > 0:
                    self.pause()
                    yield 1

            if not self.dataReady('next') and not pleaseStop and not mustStop:
                self.requestNext()

    def handleChildTerminations(self):
        """Unplugs any children that have terminated"""
        for child in self.childComponents():
            if child._isStopped():
                self.removeChild(child)

    def checkControl(self):
        while self.dataReady('control'):
            msg = self.recv('control')
            if isinstance(msg, producerFinished):
                self.pleaseStop = msg
            elif isinstance(msg, shutdownMicroprocess):
                self.mustStop = msg

        return (
         self.mustStop, self.pleaseStop)

    def requestNext(self):
        """Sends 'next' out the 'requestNext' outbox"""
        self.send('NEXT', 'requestNext')

    def instantiateNewChild(self, args):
        newChild = self.factory(args)
        self.addChildren(newChild)
        self.link((self, 'inbox'), (newChild, 'inbox'), passthrough=1)
        self.link((self, '_signal'), (newChild, 'control'))
        self.link((newChild, 'outbox'), (self, 'outbox'), passthrough=2)
        newChild.activate()

    def shutdownChild(self, shutdownMsg):
        self.send(shutdownMsg, '_signal')


__kamaelia_components__ = (
 Carousel,)
if __name__ == '__main__':
    pass