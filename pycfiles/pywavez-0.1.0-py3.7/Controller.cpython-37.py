# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pywavez/Controller.py
# Compiled at: 2019-12-28 13:16:28
# Size of source mod 2**32: 19796 bytes
import asyncio, bisect, collections, functools, logging, time, traceback, typing
from asyncinit import asyncinit
from pywavez.zwave import outboundMessageClass, inboundMessageFromBytes
from pywavez.zwave.Constants import LibraryType, MessageClass, MessageType
from pywavez.util import toCamelCase, waitForOne, spawnTask
import pywavez.ControllerNode as ControllerNode
from pywavez.SerialDeviceBase import SerialDeviceBase, makeSerialDevice
import pywavez.SerialProtocol as SerialProtocol
from pywavez.Transmission import Priority, MessageTransmission, SimpleQueue, MessageQueue

class FuncIdManager:

    class TimeoutEvent:
        __slots__ = ('id', 'expires', 'cancelled', 'future')

        def __init__(self, id, expires):
            self.id = id
            self.expires = expires
            self.cancelled = False
            self.future = asyncio.Future()

        def __lt__(self, other):
            return self.expires < other.expires

    class FuncId:
        __slots__ = ('_FuncId__id', 'release', 'future')

        def __init__(self, id, release, future):
            self._FuncId__id = id
            self.release = release
            self.future = future

        @property
        def value(self):
            return self._FuncId__id

    def __init__(self):
        self._FuncIdManager__available_ids = collections.deque(range(1, 256))
        self._FuncIdManager__event = asyncio.Event()
        self._FuncIdManager__timeout_events_by_time = collections.deque()
        self._FuncIdManager__timeout_events_by_id = {}

    async def get(self, timeout=90):
        now = time.monotonic()
        while not self._FuncIdManager__available_ids:
            while not self._FuncIdManager__timeout_events_by_time or self._FuncIdManager__timeout_events_by_time[0].expires < now or self._FuncIdManager__timeout_events_by_time[0].cancelled:
                toe = self._FuncIdManager__timeout_events_by_time.popleft()
                if self._FuncIdManager__cancel(toe):
                    break

            if self._FuncIdManager__available_ids:
                break
            else:
                self._FuncIdManager__event.clear()
                if self._FuncIdManager__timeout_events_by_time:
                    timeout = self._FuncIdManager__timeout_events_by_time[0].expires - now
                    await waitForOne((self._FuncIdManager__event.wait()), timeout=timeout)
                else:
                    await self._FuncIdManager__event.wait()
            now = time.monotonic()

        id = self._FuncIdManager__available_ids.popleft()
        toe = self.TimeoutEvent(id, now + timeout)
        self._FuncIdManager__timeout_events_by_id[id] = toe
        idx = bisect.bisect_right(self._FuncIdManager__timeout_events_by_time, toe)
        self._FuncIdManager__timeout_events_by_time.insert(idx, toe)
        return self.FuncId(id, lambda : self._FuncIdManager__cancel(toe), toe.future)

    def set_result(self, id, result):
        self._FuncIdManager__timeout_events_by_id[id].future.set_result(result)

    def __cancel(self, toe):
        if not toe.cancelled:
            toe.cancelled = True
            del self._FuncIdManager__timeout_events_by_id[toe.id]
            self._FuncIdManager__available_ids.append(toe.id)
            self._FuncIdManager__event.set()
            return True


@asyncinit
class Controller:

    async def __init__(self, serial_protocol: typing.Union[(SerialProtocol, SerialDeviceBase, str)]):
        if not isinstance(serial_protocol, SerialProtocol):
            if isinstance(serial_protocol, SerialDeviceBase):
                serial_protocol = SerialProtocol(serial_protocol)
            else:
                serial_protocol = SerialProtocol(await makeSerialDevice(serial_protocol))
        else:
            self._Controller__sp = serial_protocol
            self._Controller__mq = MessageQueue()
            self._Controller__node = [None] * 233
            self._Controller__initializationNodeQueue = []
            self.initializationRequiredEvent = asyncio.Event()
            self._Controller__responseHandler = {MessageClass.SERIAL_API_GET_INIT_DATA: self._Controller__handleSerialApiGetInitDataResponse}
            self._Controller__incomingRequestHandler = {MessageClass.APPLICATION_UPDATE: self._Controller__handleApplicationUpdateRequest, 
             
             MessageClass.APPLICATION_COMMAND_HANDLER: self._Controller__handleApplicationCommandHandlerRequest, 
             
             MessageClass.SEND_DATA: self._Controller__handleSendDataRequest}
            self._funcIdManager = FuncIdManager()
            self._receivedMessages = SimpleQueue()
            self.hasMessage = self._receivedMessages.hasMessage
            self.waitForMessage = self._receivedMessages.waitForMessage
            self.takeMessage = self._receivedMessages.takeMessage
            self._Controller__task = spawnTask(self._Controller__taskImpl())
            self._Controller__nodeInitializationTask = spawnTask(self._Controller__nodeInitializationTaskImpl())
            cap = await self._Controller__sendMessage(outboundMessageClass(MessageType.REQUEST, MessageClass.SERIAL_API_GET_CAPABILITIES)())
            self._Controller__manufacturer = (
             cap.manufacturerId,
             cap.manufacturerProduct,
             cap.manufacturerProductId)
            self._Controller__serialApiVersionRevision = (
             cap.serialApiVersion,
             cap.serialApiRevision)
            funcs = []
            for f in cap.supportedFunctions:
                try:
                    funcs.append(MessageClass(f))
                except ValueError:
                    logging.warning(f"Controller supports unknown message class {f}")

            self._Controller__setSupportedFunctions(funcs)
            if hasattr(self, 'memoryGetId'):
                msg = await self.memoryGetId()
                self._Controller__homeId = f"{msg.homeId:08x}"
                self._Controller__controllerNodeId = msg.controllerNodeId
            else:
                self._Controller__homeId = None
            self._Controller__controllerNodeId = 1
        vr = await self.getVersion()
        self._Controller__libraryVersion = vr.libraryVersion
        self._Controller__libraryType = vr.libraryType
        await self.serialApiGetInitData()
        if self._Controller__libraryType != LibraryType.BRIDGE_CONTROLLER:
            if hasattr(self, 'serialApiSetTimeouts'):
                await self.serialApiSetTimeouts(rxAckTimeout=150, rxByteTimeout=15)
        for id in sorted(self._Controller__apiInitData.nodes):
            if id == self._Controller__controllerNodeId:
                continue
            if not 1 <= id <= 232:
                logging.warning(f"Invalid node id {id}")
                continue
            self._Controller__addNode(id)

    def __addNode(self, id):
        if self._Controller__node[id] is not None:
            logging.warning(f"Tried to add already existing node {id}")
            return
        node = self._Controller__node[id] = ControllerNode(id, self)
        self._Controller__initializationNodeQueue.append(node)
        self.initializationRequiredEvent.set()

    async def shutdown(self):
        self._Controller__task.cancel()
        await self._Controller__sp.close()

    def sendCommand(self, node_id, command, *, endpoint=0, priority=Priority.DEFAULT):
        return self._getNode(node_id).sendCommand(command,
          endpoint=endpoint, priority=priority)

    async def __taskImpl(self):
        msgtx = None
        tx_timeout = None
        while 1:
            if msgtx is None:
                if not self._Controller__sp.messageReady():
                    if not self._Controller__mq.hasMessage():
                        await waitForOne(self._Controller__mq.waitForMessage(), self._Controller__sp.waitForMessage())
                    else:
                        if not self._Controller__sp.messageReady():
                            await waitForOne((self._Controller__sp.waitForMessage()),
                              timeout=(tx_timeout - time.monotonic()))
                while self._Controller__sp.messageReady():
                    msg = await next(self._Controller__sp)
                    try:
                        msg = inboundMessageFromBytes(msg)
                    except Exception:
                        logging.warning(f"Ignoring unknown incoming message: {msg.hex()}")
                        continue

                    logging.debug(f"msg received: {msg!r}")
                    if msgtx is not None:
                        if msg.MessageType is MessageType.RESPONSE:
                            if msg.MessageClass is msgtx.message.MessageClass:
                                msgtx.transmitting = False
                                msgtx.finished = True
                                if msgtx.responseHandler is not None:
                                    try:
                                        msgtx.responseHandler(msgtx.message, msg)
                                    except Exception as ex:
                                        try:
                                            logging.warning(f"Response handler raised exception: {ex!r}")
                                        finally:
                                            ex = None
                                            del ex

                                if not msgtx.cancelled():
                                    msgtx.set_result(msg)
                                msgtx = None
                                tx_timeout = None
                                continue
                    if msg.MessageType is MessageType.REQUEST:
                        handler = self._Controller__incomingRequestHandler.get(msg.MessageClass)
                        if handler is not None:
                            try:
                                for rmsg in handler(msg):
                                    self._receivedMessages.append(rmsg)
                                    logging.debug(f"msg received (after handler): {rmsg!r}")

                            except Exception as ex:
                                try:
                                    logging.warning(f"Incoming request handler raised exception: {ex!r}")
                                    traceback.print_exc()
                                finally:
                                    ex = None
                                    del ex

                            msg = None
                    if msg is not None:
                        self._receivedMessages.append(msg)

                if msgtx is None and self._Controller__mq.hasMessage():
                    if not self._Controller__sp.idle:
                        await waitForOne(self._Controller__sp.waitForIdleState(), self._Controller__sp.waitForMessage())
                        continue
                    msgtx = self._Controller__mq.takeMessage()
                    msgtx.transmitting = True
                    logging.debug(f"Attempting transmission: {msgtx.message!r}")
                    try:
                        data = msgtx.message.toBytes()
                    except Exception as ex:
                        try:
                            msgtx.set_exception(ex)
                            msgtx = None
                        finally:
                            ex = None
                            del ex

                    else:
                        logging.debug(f"outgoing: {msgtx.message!r}")
                        try:
                            await self._Controller__sp.send(data)
                        except Exception as ex:
                            try:
                                logging.info(f"Exception while sending: {ex!r}")
                                await asyncio.sleep(0.05)
                                if msgtx.retransmission >= msgtx.maxRetransmissions:
                                    msgtx.set_exception(ex)
                                else:
                                    msgtx.retransmission += 1
                                    msgtx.pauseUntil = time.monotonic() + 1
                                    msgtx.transmitting = False
                                    self._Controller__mq.add(msgtx)
                                msgtx = None
                            finally:
                                ex = None
                                del ex

                        else:
                            tx_timeout = time.monotonic() + 5
            elif tx_timeout is not None and time.monotonic() >= tx_timeout:
                msgtx.retransmission += 1
                msgtx.pauseUntil = time.monotonic() + 1
                msgtx.transmitting = False
                self._Controller__mq.add(msgtx)
                msgtx = None
                tx_timeout = None

    def __sendMessage(self, message, **kwargs):
        msgtx = MessageTransmission(message, **kwargs)
        self._Controller__mq.add(msgtx)
        return msgtx

    def __setSupportedFunctions(self, message_classes):
        self._Controller__supportedFunctions = message_classes = frozenset(message_classes)
        for msgclass in MessageClass:
            try:
                cl = outboundMessageClass(MessageType.REQUEST, msgclass)
            except KeyError:
                continue

            name = toCamelCase(msgclass.name)
            if msgclass in message_classes:
                if cl.NodeIdField is None:

                    def node_id_func(msg):
                        pass

                else:
                    node_id_func = lambda nif: lambda msg: getattr(msg, nif)(cl.NodeIdField)
                resp_handler = self._Controller__responseHandler.get(msgclass)
                func = self._Controller__makeCallFunction(cl, node_id_func, resp_handler)
                implfunc = getattr(self, f"_{name}Impl", None)
                if implfunc is not None:
                    func = functools.partial(implfunc, func)
            else:
                func = raise_not_implemented
            setattr(self, name, func)

    def __makeCallFunction(self, cl, node_id_func, resp_handler):

        def func(PRIORITY=Priority.DEFAULT, **kwargs):
            msg = cl(**kwargs)
            logging.debug(f"makeCallFunction func : {msg!r}")
            node_id = node_id_func(msg)
            return self._Controller__sendMessage(msg,
              nodeId=node_id,
              priority=PRIORITY,
              response_handler=resp_handler)

        return func

    def _getNode(self, id):
        if not 1 <= id <= 232:
            raise Exception(f"Bogus node id: {id}")
        node = self._Controller__node[id]
        if node is None:
            raise Exception(f"Unknown node id: {id}")
        return node

    def __handleSerialApiGetInitDataResponse(self, req, resp):
        self._Controller__apiInitData = resp

    def __handleApplicationUpdateRequest(self, msg):
        if msg.nodeId == 0:
            yield msg
        else:
            node = self._getNode(msg.nodeId)
            yield from node.setCommandClasses(0, msg.commandClasses)
            node.nodeActive()

    def __handleSendDataRequest(self, msg):
        try:
            self._funcIdManager.set_result(msg.funcId, msg.txStatus)
        except Exception as ex:
            try:
                logging.warning(f"Controller.__handleSendDataRequest: {ex!r}")
            finally:
                ex = None
                del ex

        yield msg

    def __handleApplicationCommandHandlerRequest(self, msg):
        try:
            node = self._getNode(msg.nodeId)
        except Exception:
            yield msg
        else:
            for x in node.handleApplicationCommandHandlerRequest(msg):
                yield x

    async def __nodeInitializationTaskImpl(self):
        while 1:
            while not self._Controller__initializationNodeQueue:
                logging.info('No nodes require initialization')
                self.initializationRequiredEvent.clear()
                await self.initializationRequiredEvent.wait()

            idx = 0
            while idx < len(self._Controller__initializationNodeQueue):
                if self._Controller__initializationNodeQueue[idx].attemptInitializationTime is None:
                    self._Controller__initializationNodeQueue.pop(idx)
                else:
                    idx += 1

            if not self._Controller__initializationNodeQueue:
                continue
            elif not self._Controller__initializationNodeQueue:
                continue
            else:
                logging.info(f"Number of nodes requiring initialization: {len(self._Controller__initializationNodeQueue)}")
            node = None
            now = time.monotonic()
            earliest = None
            for idx, n in enumerate(self._Controller__initializationNodeQueue):
                if n.sendsWakeUpNotifications and n.wakeUpNotificationEvent.is_set():
                    if n.attemptInitializationTime <= now:
                        node = self._Controller__initializationNodeQueue.pop(idx)
                        self._Controller__initializationNodeQueue.append(node)
                        break
                    elif earliest is None or earliest > n.attemptInitializationTime:
                        earliest = n.attemptInitializationTime

            if node is None:
                for idx, n in enumerate(self._Controller__initializationNodeQueue):
                    if not n.sendsWakeUpNotifications:
                        if n.attemptInitializationTime <= now:
                            node = self._Controller__initializationNodeQueue.pop(idx)
                            self._Controller__initializationNodeQueue.append(node)
                            break
                        else:
                            if earliest is None or earliest > n.attemptInitializationTime:
                                pass
                            earliest = n.attemptInitializationTime

            if node is None:
                if earliest is not None:
                    self.initializationRequiredEvent.clear()
                    await waitForOne((self.initializationRequiredEvent.wait()),
                      timeout=(earliest - now + 0.05))
                    continue
                if node.sendsWakeUpNotifications:
                    await node.attemptInitialization()
                else:
                    node_wakeup = [n.wakeUpNotificationEvent.wait() for n in self._Controller__initializationNodeQueue if n is not node]
                    await waitForOne(node.attemptInitialization(), *node_wakeup)

    def wakeUpNotification(self, node):
        if node.attemptInitializationTime is not None:
            self.initializationRequiredEvent.set()

    @property
    def homeId(self):
        return self._Controller__homeId

    @property
    def controllerNodeId(self):
        return self._Controller__controllerNodeId

    @property
    def nodeIds(self):
        return set(self._Controller__apiInitData.nodes)


def raise_not_implemented(**kwargs):
    raise NotImplementedError('ZWave controller does not implement function')