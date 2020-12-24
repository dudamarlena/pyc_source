# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Axon/experimental/_pprocess_support.py
# Compiled at: 2008-10-19 12:19:52
r"""================================================
likefile - file-like interaction with components
================================================

likefile is a way to run Axon components with code that is not Axon-aware. It
does this by running the scheduler and all associated microprocesses in a
separate thread, and using a custom component to communicate if so desired.

Using this code
---------------

With a normal kamaelia system, you would start up a component and start
running the Axon scheduler as follows, either::

    from Axon.Scheduler import scheduler
    component.activate()
    scheduler.run.runThreads()
    someOtherCode()

or simply::

    component.run()
    someOtherCode()

In both cases, someOtherCode() only run when the scheduler exits. What do you
do if you want to (e.g.) run this alongside another external library that has
the same requirement?

Well, first we start the Axon scheduler in the background as follows::

    from likefile import background
    background().start()

The scheduler is now actively running in the background, and you can start
components on it from the foreground, in the same way as you would from inside
kamaelia (don't worry, activate() is threadsafe)::

    component.activate()
    someOtherCode()

"component" will immediately start running and processing. This is fine if it's
something non-interactive like a TCP server, but what do we do if we want to 
interact with this component from someOtherCode?

In this case, we use 'likefile', instead of activating. This is a wrapper
which sits around a component and provides a threadsafe way to interact
with it, whilst it is running in the backgrounded scheduler::

    from Axon.LikeFile import likefile
    wrappedComponent = likefile(component)
    someOtherCode()

Now, wrappedComponent is an instance of the likefile wrapper, and you can
interact with "component" by calling get() on wrappedComponent, to get data
from the outbox on "component", or by calling put(data) to put "data" into
the inbox of "component" like so::

    p = likefile( SimpleHTTPClient() )
    p.put("http://google.com")
    google = p.get()
    p.shutdown()
    print "google's homepage is", len(google), "bytes long.

for both get() and put(), there is an optional extra parameter boxname,
allowing you to interact with different boxes, for example to send a message
with the text "RELOAD" to a component's control inbox, you would do::

    wrappedComponent.put("RELOAD", "control")
    wrappedComponent.get("signal")

Finally, likefile objects have a shutdown() method that sends the usual Axon
IPC shutdown messages to a wrapped component, and prevents further IO.

Advanced likefile usage
-----------------------

likefile has some optional extra arguments on creation, for handling custom
boxes outside the "basic 4". For example, to wrap a component with inboxes
called "secondary" and "tertiary" and an outbox called "debug", You would do::

    p = likefile( componentMaker, 
                  extraInboxes = ("secondary", "tertiary"),
                  extraOutboxes = "debug", )

Either strings or tuples of strings will work.

It may be the case that the component you are trying to wrap will link its own 
inbox/outbox/signal/control, and this will result in a BoxAlreadyLinkedToDestination
exception. To stop likefile from wrapping the default 4 boxes, pass the parameter 
wrapDefault = False. Note that you will need to manually wrap every box you want to use,
for example to wrap a component that has its own linkages for signal/control::

    p = likefile( myComponent, 
                  wrapDefault = False,
                  extraInboxes = "inbox",
                  extraOutboxes = "outbox", )

Diagram of likefile's functionality
-----------------------------------

likefile is constructed from components like so::

         +----------------------------------+
         |             likefile             |
         +----------------------------------+
              |                      / \ 
              |                       |
          InQueues                 OutQueues
              |                       |
    +---------+-----------------------+---------+
    |        \ /                      |         |
    |    +---------+               +--------+   |
    |    |  Input  |   Shutdown    | Output |   |
    |    | Wrapper | ------------> |        |   |
    |    | (thread)|   Message     |Wrapper |   |
    |    +---------+               +--------+   |
    |         |                      / \        |
    |         |                       |         |
    |     Inboxes                 Outboxes      |
    |         |                       |         |
    |        \ /                      |         |
    |    +----------------------------------+   |
    |    |      the wrapped component       |   |
    |    +----------------------------------+   |
    |                                           |
    |    +----------------------------------+   |
    |    |       Some other component       |   | 
    |    |     that was only activated      |   |
    |    +----------------------------------+   |
    |                                           |
    |  AXON SCHEDULED COMPONENTS                |
    +-------------------------------------------+

Note 1: Threadsafeness of activate().

when a component is activated, it calls the method inherited from microprocess, which calls _addThread(self)
on an appropriate scheduler. _addThread calls wakeThread, which places the request on a threadsafe queue.

"""
from Axon.Scheduler import scheduler
from Axon.Component import component
from Axon.ThreadedComponent import threadedadaptivecommscomponent
from Axon.AdaptiveCommsComponent import AdaptiveCommsComponent
from Axon.AxonExceptions import noSpaceInBox
import Queue, threading, time, copy, warnings, Axon.Ipc as Ipc
queuelengths = 0
import Axon.CoordinatingAssistantTracker as cat
DEFIN = [
 'inbox', 'control']
DEFOUT = ['outbox', 'signal']

def addBox(names, boxMap, addBox):
    """        Add an extra wrapped box called name, using the addBox function provided
        (either self.addInbox or self.addOutbox), and adding it to the box mapping
        which is used to coordinate message routing within component wrappers.
        """
    for boxname in names:
        if boxname in boxMap:
            raise ValueError, '%s %s already exists!' % (direction, boxname)
        realboxname = addBox(boxname)
        boxMap[boxname] = realboxname


class dummyComponent(component):
    """A dummy component. Functionality: None. Prevents the scheduler from dying immediately."""

    def main(self):
        while True:
            self.pause()
            yield 1


class background(threading.Thread):
    """A python thread which runs a scheduler. Takes the same arguments at creation that scheduler.run.runThreads accepts."""
    lock = threading.Lock()

    def __init__(self, slowmo=0, zap=False):
        if not background.lock.acquire(False):
            raise 'only one scheduler for now can be run!'
        self.slowmo = slowmo
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.zap = zap

    def run(self):
        if self.zap:
            X = scheduler()
            scheduler.run = X
            cat.coordinatingassistanttracker.basecat.zap()
        dummyComponent().activate()
        scheduler.run.runThreads(slowmo=self.slowmo)
        background.lock.release()


class componentWrapperInput(threadedadaptivecommscomponent):
    """A wrapper that takes a child component and waits on an event from the foreground, to signal that there is 
    queued data to be placed on the child's inboxes."""

    def __init__(self, child, inboxes=DEFIN):
        super(componentWrapperInput, self).__init__()
        self.child = child
        self.inQueues = dict()
        self.whatInbox = Queue.Queue()
        self.isDead = threading.Event()
        self.childInboxMapping = dict()
        addBox(inboxes, self.childInboxMapping, self.addOutbox)
        for (childSink, parentSource) in self.childInboxMapping.iteritems():
            self.inQueues[childSink] = Queue.Queue(self.queuelengths)
            self.link((self, parentSource), (self.child, childSink))

        self.deathbox = self.addOutbox(str(id(self)))

    def main(self):
        while True:
            whatInbox = self.whatInbox.get()
            if not self.pollQueue(whatInbox):
                self.isDead.set()
                self.send(object, self.deathbox)
                return

    def pollQueue(self, whatInbox):
        """This method checks all the queues from the outside world, and forwards any waiting data
        to the child component. Returns False if we propogated a shutdown signal, true otherwise."""
        parentSource = self.childInboxMapping[whatInbox]
        queue = self.inQueues[whatInbox]
        while not queue.empty():
            if not self.outboxes[parentSource].isFull():
                msg = queue.get_nowait()
                try:
                    self.send(msg, parentSource)
                except noSpaceInBox, e:
                    raise 'Box delivery failed despite box (earlier) reporting being not full. Is more than one thread directly accessing boxes?'
                else:
                    if isinstance(msg, (Ipc.shutdownMicroprocess, Ipc.producerFinished)):
                        return False
            else:
                break

        return True


class componentWrapperOutput(AdaptiveCommsComponent):
    """A component which takes a child component and connects its outboxes to queues, which communicate
    with the likefile component."""

    def __init__(self, child, inputHandler, outboxes=DEFOUT):
        super(componentWrapperOutput, self).__init__()
        self.queuelengths = queuelengths
        self.child = child
        self.addChildren(self.child)
        self.outQueues = dict()
        self.isDead = inputHandler.isDead
        self.deathbox = self.addInbox(str(id(self)))
        self.link((inputHandler, inputHandler.deathbox), (self, self.deathbox))
        self.childOutboxMapping = dict()
        addBox(outboxes, self.childOutboxMapping, self.addInbox)
        for (childSource, parentSink) in self.childOutboxMapping.iteritems():
            self.outQueues[childSource] = Queue.Queue(self.queuelengths)
            self.link((self.child, childSource), (self, parentSink))

    def main(self):
        self.child.activate()
        while True:
            self.pause()
            yield 1
            self.sendPendingOutput()
            if self.dataReady(self.deathbox):
                return

    def sendPendingOutput(self):
        """This method will take any outgoing data sent to us from a child component and stick it on a queue 
        to the outside world."""
        for (childSource, parentSink) in self.childOutboxMapping.iteritems():
            queue = self.outQueues[childSource]
            while self.dataReady(parentSink):
                if not queue.full():
                    msg = self.recv(parentSink)
                    queue.put_nowait(msg)
                else:
                    break


class likefile(object):
    """An interface to the message queues from a wrapped component, which is activated on a backgrounded scheduler."""

    def __init__(self, child, extraInboxes=(), extraOutboxes=(), wrapDefault=True):
        if background.lock.acquire(False):
            background.lock.release()
            raise AttributeError, 'no running scheduler found.'
        if not isinstance(extraInboxes, tuple):
            extraInboxes = (
             extraInboxes,)
        if not isinstance(extraOutboxes, tuple):
            extraOutboxes = (
             extraOutboxes,)
        validInboxes = type(child).Inboxes.keys()
        validOutboxes = type(child).Outboxes.keys()
        inboxes = []
        outboxes = []
        if wrapDefault:
            for i in DEFIN:
                if i in validInboxes:
                    inboxes.append(i)

            for i in DEFOUT:
                if i in validOutboxes:
                    outboxes.append(i)

        inboxes += list(extraInboxes)
        outboxes += list(extraOutboxes)
        try:
            inputComponent = componentWrapperInput(child, inboxes)
        except KeyError, e:
            raise KeyError, 'component to wrap has no such inbox: %s' % e

        try:
            outputComponent = componentWrapperOutput(child, inputComponent, outboxes)
        except KeyError, e:
            del inputComponent
            raise KeyError, 'component to wrap has no such outbox: %s' % e

        self.inQueues = copy.copy(inputComponent.inQueues)
        self.outQueues = copy.copy(outputComponent.outQueues)
        self.inputComponent = inputComponent
        self.outputComponent = outputComponent
        inputComponent.activate()
        outputComponent.activate()
        self.alive = True

    def empty(self, boxname='outbox'):
        """Return True if there is no data pending collection on boxname, False otherwise."""
        return self.outQueues[boxname].empty()

    def qsize(self, boxname='outbox'):
        """Returns the approximate number of pending data items awaiting collection from boxname. Will never be smaller than the actual amount."""
        return self.outQueues[boxname].qsize()

    def get_nowait(self, boxname='outbox'):
        """Equivalent to get(boxname, False)"""
        return self.get(boxname, blocking=False)

    def anyReady(self):
        names = []
        for boxname in self.outQueues.keys():
            if self.qsize(boxname):
                names.append(boxname)

        if names != []:
            return names
        return

    def get(self, boxname='outbox', blocking=True, timeout=86400):
        """Performs a blocking read on the queue corresponding to the named outbox on the wrapped component.
        raises AttributeError if the likefile is not alive. Optional parameters blocking and timeout function
        the same way as in Queue objects, since that is what's used under the surface."""
        if self.alive:
            return self.outQueues[boxname].get(blocking, timeout)
        else:
            raise AttributeError, 'shutdown was previously called, or we were never activated.'

    def put(self, msg, boxname='inbox'):
        """Places an object on a queue which will be directed to a named inbox on the wrapped component."""
        if self.alive:
            queue = self.inQueues[boxname]
            queue.put_nowait(msg)
            self.inputComponent.whatInbox.put_nowait(boxname)
        else:
            raise AttributeError, 'shutdown was previously called, or we were never activated.'

    def shutdown(self):
        """Sends terminatory signals to the wrapped component, and shut down the componentWrapper.
        will warn if the shutdown took too long to confirm in action."""
        if self.alive:
            self.put(Ipc.shutdown(), 'control')
            self.put(Ipc.producerFinished(), 'control')
            self.put(Ipc.shutdownMicroprocess(), 'control')
        else:
            raise AttributeError, 'shutdown was previously called, or we were never activated.'
        self.inputComponent.isDead.wait(1)
        if not self.inputComponent.isDead.isSet():
            warnings.warn('Timed out waiting on shutdown confirmation, may not be dead.')
        self.alive = False

    def __del__(self):
        if self.alive:
            self.shutdown()


if __name__ == '__main__':
    background = background().start()
    time.sleep(0.1)
    from Kamaelia.Protocol.HTTP.HTTPClient import SimpleHTTPClient
    import time
    p = likefile(SimpleHTTPClient())
    p.put('http://google.com')
    p.put('http://slashdot.org')
    p.put('http://whatismyip.org')
    google = p.get()
    slashdot = p.get()
    whatismyip = p.get()
    p.shutdown()
    print 'google is', len(google), 'bytes long, and slashdot is', len(slashdot), 'bytes long. Also, our IP address is:', whatismyip