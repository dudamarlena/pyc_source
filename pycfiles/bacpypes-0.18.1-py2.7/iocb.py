# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bacpypes/iocb.py
# Compiled at: 2018-08-02 15:42:10
"""
IOCB Module
"""
import sys, logging
from time import time as _time
import threading
from bisect import bisect_left
from .debugging import bacpypes_debugging, ModuleLogger, DebugContents
from .core import deferred
from .task import FunctionTask
from .comm import Client
_debug = 0
_log = ModuleLogger(globals())
_statelog = logging.getLogger(__name__ + '._statelog')
local_controllers = {}
IDLE = 0
PENDING = 1
ACTIVE = 2
COMPLETED = 3
ABORTED = 4
_stateNames = {0: 'IDLE', 
   1: 'PENDING', 
   2: 'ACTIVE', 
   3: 'COMPLETED', 
   4: 'ABORTED'}
CTRL_IDLE = 0
CTRL_ACTIVE = 1
CTRL_WAITING = 1
_ctrlStateNames = {0: 'IDLE', 
   1: 'ACTIVE', 
   2: 'WAITING'}
TimeoutError = RuntimeError('timeout')
_strftime = lambda : '%011.6f' % (_time() % 3600,)
_identNext = 1
_identLock = threading.Lock()

@bacpypes_debugging
class IOCB(DebugContents):
    _debug_contents = ('args', 'kwargs', 'ioState', 'ioResponse-', 'ioError', 'ioController',
                       'ioServerRef', 'ioControllerRef', 'ioClientID', 'ioClientAddr',
                       'ioComplete', 'ioCallback+', 'ioQueue', 'ioPriority', 'ioTimeout')

    def __init__(self, *args, **kwargs):
        global _identNext
        _identLock.acquire()
        ioID = _identNext
        _identNext += 1
        _identLock.release()
        if _debug:
            IOCB._debug('__init__(%d) %r %r', ioID, args, kwargs)
        self.ioID = ioID
        self.args = args
        self.kwargs = kwargs
        self.ioState = IDLE
        self.ioResponse = None
        self.ioError = None
        self.ioController = None
        self.ioComplete = threading.Event()
        self.ioComplete.clear()
        self.ioCallback = []
        self.ioQueue = None
        self.ioPriority = kwargs.get('_priority', 0)
        if '_priority' in kwargs:
            if _debug:
                IOCB._debug('    - ioPriority: %r', self.ioPriority)
            del kwargs['_priority']
        self.ioTimeout = None
        return

    def add_callback(self, fn, *args, **kwargs):
        """Pass a function to be called when IO is complete."""
        if _debug:
            IOCB._debug('add_callback(%d) %r %r %r', self.ioID, fn, args, kwargs)
        self.ioCallback.append((fn, args, kwargs))
        if self.ioComplete.isSet():
            self.trigger()

    def wait(self, *args, **kwargs):
        """Wait for the completion event to be set."""
        if _debug:
            IOCB._debug('wait(%d) %r %r', self.ioID, args, kwargs)
        return self.ioComplete.wait(*args, **kwargs)

    def trigger(self):
        """Set the completion event and make the callback(s)."""
        if _debug:
            IOCB._debug('trigger(%d)', self.ioID)
        if self.ioQueue:
            if _debug:
                IOCB._debug('    - dequeue')
            self.ioQueue.remove(self)
        if self.ioTimeout:
            if _debug:
                IOCB._debug('    - cancel timeout')
            self.ioTimeout.suspend_task()
        self.ioComplete.set()
        if _debug:
            IOCB._debug('    - complete event set')
        for fn, args, kwargs in self.ioCallback:
            if _debug:
                IOCB._debug('    - callback fn: %r %r %r', fn, args, kwargs)
            fn(self, *args, **kwargs)

    def complete(self, msg):
        """Called to complete a transaction, usually when ProcessIO has
        shipped the IOCB off to some other thread or function."""
        if _debug:
            IOCB._debug('complete(%d) %r', self.ioID, msg)
        if self.ioController:
            self.ioController.complete_io(self, msg)
        else:
            self.ioState = COMPLETED
            self.ioResponse = msg
            self.trigger()

    def abort(self, err):
        """Called by a client to abort a transaction."""
        if _debug:
            IOCB._debug('abort(%d) %r', self.ioID, err)
        if self.ioController:
            self.ioController.abort_io(self, err)
        elif self.ioState < COMPLETED:
            self.ioState = ABORTED
            self.ioError = err
            self.trigger()

    def set_timeout(self, delay, err=TimeoutError):
        """Called to set a transaction timer."""
        if _debug:
            IOCB._debug('set_timeout(%d) %r err=%r', self.ioID, delay, err)
        if self.ioTimeout:
            self.ioTimeout.suspend_task()
        else:
            self.ioTimeout = FunctionTask(self.abort, err)
        self.ioTimeout.install_task(delta=delay)

    def __repr__(self):
        xid = id(self)
        if xid < 0:
            xid += 4294967296
        sname = self.__module__ + '.' + self.__class__.__name__
        desc = '(%d)' % self.ioID
        return '<' + sname + desc + ' instance at 0x%08x' % (xid,) + '>'


@bacpypes_debugging
class IOChainMixIn(DebugContents):
    _debug_contents = ('ioChain++', )

    def __init__(self, iocb):
        if _debug:
            IOChainMixIn._debug('__init__ %r', iocb)
        self.ioChain = iocb
        self.add_callback(self.chain_callback)
        if not self.ioChain:
            return
        iocb.ioController = self
        iocb.ioState = ACTIVE
        try:
            if _debug:
                IOChainMixIn._debug('    - encoding')
            self.encode()
            if _debug:
                IOChainMixIn._debug('    - encode complete')
        except:
            err = sys.exc_info()[1]
            if _debug:
                IOChainMixIn._exception('    - encoding exception: %r', err)
            iocb.abort(err)

    def chain_callback(self, iocb):
        """Callback when this iocb completes."""
        if _debug:
            IOChainMixIn._debug('chain_callback %r', iocb)
        if not self.ioChain:
            return
        else:
            iocb = self.ioChain
            try:
                if _debug:
                    IOChainMixIn._debug('    - decoding')
                self.decode()
                if _debug:
                    IOChainMixIn._debug('    - decode complete')
            except:
                err = sys.exc_info()[1]
                if _debug:
                    IOChainMixIn._exception('    - decoding exception: %r', err)
                iocb.ioState = ABORTED
                iocb.ioError = err

            self.ioChain = None
            iocb.ioController = None
            iocb.trigger()
            return

    def abort_io(self, iocb, err):
        """Forward the abort downstream."""
        if _debug:
            IOChainMixIn._debug('abort_io %r %r', iocb, err)
        if iocb is not self.ioChain:
            raise RuntimeError('broken chain')
        self.abort(err)

    def encode(self):
        """Hook to transform the request, called when this IOCB is
        chained."""
        if _debug:
            IOChainMixIn._debug('encode')

    def decode(self):
        """Hook to transform the response, called when this IOCB is
        completed."""
        if _debug:
            IOChainMixIn._debug('decode')
        iocb = self.ioChain
        if self.ioState == COMPLETED:
            if _debug:
                IOChainMixIn._debug('    - completed: %r', self.ioResponse)
            iocb.ioState = COMPLETED
            iocb.ioResponse = self.ioResponse
        elif self.ioState == ABORTED:
            if _debug:
                IOChainMixIn._debug('    - aborted: %r', self.ioError)
            iocb.ioState = ABORTED
            iocb.ioError = self.ioError
        else:
            raise RuntimeError('invalid state: %d' % (self.ioState,))


@bacpypes_debugging
class IOChain(IOCB, IOChainMixIn):

    def __init__(self, chain, *args, **kwargs):
        """Initialize a chained control block."""
        if _debug:
            IOChain._debug('__init__ %r %r %r', chain, args, kwargs)
        IOCB.__init__(self, *args, **kwargs)
        IOChainMixIn.__init__(self, chain)


@bacpypes_debugging
class IOGroup(IOCB, DebugContents):
    _debug_contents = ('ioMembers', )

    def __init__(self):
        """Initialize a group."""
        if _debug:
            IOGroup._debug('__init__')
        IOCB.__init__(self)
        self.ioMembers = []
        self.ioState = COMPLETED
        self.ioComplete.set()

    def add(self, iocb):
        """Add an IOCB to the group, you can also add other groups."""
        if _debug:
            IOGroup._debug('add %r', iocb)
        self.ioMembers.append(iocb)
        self.ioState = PENDING
        self.ioComplete.clear()
        iocb.add_callback(self.group_callback)

    def group_callback(self, iocb):
        """Callback when a child iocb completes."""
        if _debug:
            IOGroup._debug('group_callback %r', iocb)
        for iocb in self.ioMembers:
            if not iocb.ioComplete.isSet():
                if _debug:
                    IOGroup._debug('    - waiting for child: %r', iocb)
                break
        else:
            if _debug:
                IOGroup._debug('    - all children complete')
            self.ioState = COMPLETED
            self.trigger()

    def abort(self, err):
        """Called by a client to abort all of the member transactions.
        When the last pending member is aborted the group callback
        function will be called."""
        if _debug:
            IOGroup._debug('abort %r', err)
        self.ioState = ABORTED
        self.ioError = err
        for iocb in self.ioMembers:
            iocb.abort(err)

        self.trigger()


@bacpypes_debugging
class IOQueue:

    def __init__(self, name=None):
        if _debug:
            IOQueue._debug('__init__ %r', name)
        self.notempty = threading.Event()
        self.notempty.clear()
        self.queue = []

    def put(self, iocb):
        """Add an IOCB to a queue.  This is usually called by the function
        that filters requests and passes them out to the correct processing
        thread."""
        if _debug:
            IOQueue._debug('put %r', iocb)
        if iocb.ioState != PENDING:
            raise RuntimeError('invalid state transition')
        wasempty = not self.notempty.isSet()
        priority = iocb.ioPriority
        item = (priority, iocb)
        self.queue.insert(bisect_left(self.queue, (priority + 1,)), item)
        iocb.ioQueue = self
        self.notempty.set()
        return wasempty

    def get(self, block=1, delay=None):
        """Get a request from a queue, optionally block until a request
        is available."""
        if _debug:
            IOQueue._debug('get block=%r delay=%r', block, delay)
        if not block and not self.notempty.isSet():
            if _debug:
                IOQueue._debug('    - not blocking and empty')
            return
        if delay:
            self.notempty.wait(delay)
            if not self.notempty.isSet():
                return
        else:
            self.notempty.wait()
        priority, iocb = self.queue[0]
        del self.queue[0]
        iocb.ioQueue = None
        qlen = len(self.queue)
        if not qlen:
            self.notempty.clear()
        return iocb

    def remove(self, iocb):
        """Remove a control block from the queue, called if the request
        is canceled/aborted."""
        if _debug:
            IOQueue._debug('remove %r', iocb)
        for i, item in enumerate(self.queue):
            if iocb is item[1]:
                if _debug:
                    IOQueue._debug('    - found at %d', i)
                del self.queue[i]
                qlen = len(self.queue)
                if not qlen:
                    self.notempty.clear()
                break

        if _debug:
            IOQueue._debug('    - not found')

    def abort(self, err):
        """Abort all of the control blocks in the queue."""
        if _debug:
            IOQueue._debug('abort %r', err)
        try:
            for iocb in self.queue:
                iocb.ioQueue = None
                iocb.abort(err)

            self.queue = []
            self.notempty.clear()
        except ValueError:
            pass

        return


@bacpypes_debugging
class IOController(object):

    def __init__(self, name=None):
        """Initialize a controller."""
        if _debug:
            IOController._debug('__init__ name=%r', name)
        self.name = name

    def abort(self, err):
        """Abort all requests, no default implementation."""
        pass

    def request_io(self, iocb):
        """Called by a client to start processing a request."""
        if _debug:
            IOController._debug('request_io %r', iocb)
        if not isinstance(iocb, IOCB):
            raise TypeError('IOCB expected')
        iocb.ioController = self
        try:
            err = None
            iocb.ioState = PENDING
            self.process_io(iocb)
        except:
            err = sys.exc_info()[1]

        if err:
            self.abort_io(iocb, err)
        return

    def process_io(self, iocb):
        """Figure out how to respond to this request.  This must be
        provided by the derived class."""
        raise NotImplementedError('IOController must implement process_io()')

    def active_io(self, iocb):
        """Called by a handler to notify the controller that a request is
        being processed."""
        if _debug:
            IOController._debug('active_io %r', iocb)
        if iocb.ioState != IDLE and iocb.ioState != PENDING:
            raise RuntimeError('invalid state transition (currently %d)' % (iocb.ioState,))
        iocb.ioState = ACTIVE

    def complete_io(self, iocb, msg):
        """Called by a handler to return data to the client."""
        if _debug:
            IOController._debug('complete_io %r %r', iocb, msg)
        if iocb.ioState == COMPLETED:
            pass
        elif iocb.ioState == ABORTED:
            pass
        else:
            iocb.ioState = COMPLETED
            iocb.ioResponse = msg
            iocb.trigger()

    def abort_io(self, iocb, err):
        """Called by a handler or a client to abort a transaction."""
        if _debug:
            IOController._debug('abort_io %r %r', iocb, err)
        if iocb.ioState == COMPLETED:
            pass
        elif iocb.ioState == ABORTED:
            pass
        else:
            iocb.ioState = ABORTED
            iocb.ioError = err
            iocb.trigger()


@bacpypes_debugging
class IOQController(IOController):
    wait_time = 0.0

    def __init__(self, name=None):
        """Initialize a queue controller."""
        if _debug:
            IOQController._debug('__init__ name=%r', name)
        IOController.__init__(self, name)
        self.state = CTRL_IDLE
        _statelog.debug('%s %s %s' % (_strftime(), self.name, 'idle'))
        self.active_iocb = None
        self.ioQueue = IOQueue(str(name) + ' queue')
        return

    def abort(self, err):
        """Abort all pending requests."""
        if _debug:
            IOQController._debug('abort %r', err)
        if self.state == CTRL_IDLE:
            if _debug:
                IOQController._debug('    - idle')
            return
        while True:
            iocb = self.ioQueue.get(block=0)
            if not iocb:
                break
            if _debug:
                IOQController._debug('    - iocb: %r', iocb)
            iocb.ioState = ABORTED
            iocb.ioError = err
            iocb.trigger()

        if self.state != CTRL_IDLE:
            if _debug:
                IOQController._debug('    - busy after aborts')

    def request_io(self, iocb):
        """Called by a client to start processing a request."""
        if _debug:
            IOQController._debug('request_io %r', iocb)
        iocb.ioController = self
        if self.state != CTRL_IDLE:
            if _debug:
                IOQController._debug('    - busy, request queued, active_iocb: %r', self.active_iocb)
            iocb.ioState = PENDING
            self.ioQueue.put(iocb)
            return
        else:
            try:
                err = None
                self.process_io(iocb)
            except:
                err = sys.exc_info()[1]
                if _debug:
                    IOQController._debug('    - process_io() exception: %r', err)

            if err:
                if _debug:
                    IOQController._debug('    - aborting')
                self.abort_io(iocb, err)
            return

    def process_io(self, iocb):
        """Figure out how to respond to this request.  This must be
        provided by the derived class."""
        raise NotImplementedError('IOController must implement process_io()')

    def active_io(self, iocb):
        """Called by a handler to notify the controller that a request is
        being processed."""
        if _debug:
            IOQController._debug('active_io %r', iocb)
        IOController.active_io(self, iocb)
        self.state = CTRL_ACTIVE
        _statelog.debug('%s %s %s' % (_strftime(), self.name, 'active'))
        self.active_iocb = iocb

    def complete_io(self, iocb, msg):
        """Called by a handler to return data to the client."""
        if _debug:
            IOQController._debug('complete_io %r %r', iocb, msg)
        if iocb is not self.active_iocb:
            raise RuntimeError('not the current iocb')
        IOController.complete_io(self, iocb, msg)
        self.active_iocb = None
        if self.wait_time:
            self.state = CTRL_WAITING
            _statelog.debug('%s %s %s' % (_strftime(), self.name, 'waiting'))
            task = FunctionTask(IOQController._wait_trigger, self)
            task.install_task(delta=self.wait_time)
        else:
            self.state = CTRL_IDLE
            _statelog.debug('%s %s %s' % (_strftime(), self.name, 'idle'))
            deferred(IOQController._trigger, self)
        return

    def abort_io(self, iocb, err):
        """Called by a handler or a client to abort a transaction."""
        if _debug:
            IOQController._debug('abort_io %r %r', iocb, err)
        IOController.abort_io(self, iocb, err)
        if iocb is not self.active_iocb:
            if _debug:
                IOQController._debug('    - not current iocb')
            return
        self.active_iocb = None
        self.state = CTRL_IDLE
        _statelog.debug('%s %s %s' % (_strftime(), self.name, 'idle'))
        deferred(IOQController._trigger, self)
        return

    def _trigger(self):
        """Called to launch the next request in the queue."""
        if _debug:
            IOQController._debug('_trigger')
        if self.state != CTRL_IDLE:
            if _debug:
                IOQController._debug('    - not idle')
            return
        if not self.ioQueue.queue:
            if _debug:
                IOQController._debug('    - empty queue')
            return
        iocb = self.ioQueue.get()
        try:
            err = None
            self.process_io(iocb)
        except:
            err = sys.exc_info()[1]

        if err:
            self.abort_io(iocb, err)
        if self.state == CTRL_IDLE:
            deferred(IOQController._trigger, self)
        return

    def _wait_trigger(self):
        """Called to launch the next request in the queue."""
        if _debug:
            IOQController._debug('_wait_trigger')
        if self.state != CTRL_WAITING:
            raise RuntimeError('not waiting')
        self.state = CTRL_IDLE
        _statelog.debug('%s %s %s' % (_strftime(), self.name, 'idle'))
        IOQController._trigger(self)


@bacpypes_debugging
class ClientController(Client, IOQController):

    def __init__(self):
        if _debug:
            ClientController._debug('__init__')
        Client.__init__(self)
        IOQController.__init__(self)

    def process_io(self, iocb):
        if _debug:
            ClientController._debug('process_io %r', iocb)
        self.active_io(iocb)
        self.request(iocb.args[0])

    def confirmation(self, pdu):
        if _debug:
            ClientController._debug('confirmation %r', pdu)
        if not self.active_iocb:
            ClientController._debug('no active request')
            return
        if isinstance(pdu, Exception):
            self.abort_io(self.active_iocb, pdu)
        else:
            self.complete_io(self.active_iocb, pdu)


@bacpypes_debugging
class SieveQueue(IOQController):

    def __init__(self, request_fn, address=None):
        if _debug:
            SieveQueue._debug('__init__ %r %r', request_fn, address)
        IOQController.__init__(self, str(address))
        self.request_fn = request_fn
        self.address = address

    def process_io(self, iocb):
        if _debug:
            SieveQueue._debug('process_io %r', iocb)
        self.active_io(iocb)
        self.request_fn(iocb.args[0])


@bacpypes_debugging
class SieveClientController(Client, IOController):

    def __init__(self, queue_class=SieveQueue):
        if _debug:
            SieveClientController._debug('__init__')
        Client.__init__(self)
        IOController.__init__(self)
        if not issubclass(queue_class, SieveQueue):
            raise TypeError('queue class must be a subclass of SieveQueue')
        self.queues = {}
        self.queue_class = queue_class

    def process_io(self, iocb):
        if _debug:
            SieveClientController._debug('process_io %r', iocb)
        destination_address = iocb.args[0].pduDestination
        if _debug:
            SieveClientController._debug('    - destination_address: %r', destination_address)
        queue = self.queues.get(destination_address, None)
        if not queue:
            if _debug:
                SieveClientController._debug('    - new queue')
            queue = self.queue_class(self.request, destination_address)
            self.queues[destination_address] = queue
        if _debug:
            SieveClientController._debug('    - queue: %r', queue)
        queue.request_io(iocb)
        return

    def request(self, pdu):
        if _debug:
            SieveClientController._debug('request %r', pdu)
        super(SieveClientController, self).request(pdu)

    def confirmation(self, pdu):
        if _debug:
            SieveClientController._debug('confirmation %r', pdu)
        source_address = pdu.pduSource
        if _debug:
            SieveClientController._debug('    - source_address: %r', source_address)
        queue = self.queues.get(source_address, None)
        if not queue:
            if _debug:
                SieveClientController._debug('    - no queue: %r' % (source_address,))
            return
        if _debug:
            SieveClientController._debug('    - queue: %r', queue)
        if not queue.active_iocb:
            if _debug:
                SieveClientController._debug('    - no active request')
            return
        if isinstance(pdu, Exception):
            queue.abort_io(queue.active_iocb, pdu)
        else:
            queue.complete_io(queue.active_iocb, pdu)
        if not queue.ioQueue.queue and not queue.active_iocb:
            if _debug:
                SieveClientController._debug('    - queue is empty')
            del self.queues[source_address]
        return


@bacpypes_debugging
def register_controller(controller):
    global local_controllers
    if _debug:
        register_controller._debug('register_controller %r', controller)
    if not controller.name:
        return
    if controller.name in local_controllers:
        raise RuntimeError('already a local controller named %r' % (controller.name,))
    local_controllers[controller.name] = controller


@bacpypes_debugging
def abort(err):
    """Abort everything, everywhere."""
    if _debug:
        abort._debug('abort %r', err)
    for controller in local_controllers.values():
        controller.abort(err)