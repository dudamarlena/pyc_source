# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pywavez/ControllerNode.py
# Compiled at: 2019-12-28 13:45:33
# Size of source mod 2**32: 19063 bytes
import asyncio, logging, random, time, traceback
import pywavez.NodeUpdate as NodeUpdate
from pywavez.zwave import getCommandClassVersion
from pywavez.zwave.Constants import CommandClass, TransmitComplete, TransmitOption
from pywavez.util import spawnTask, waitForOne
import pywavez.ReceivedCommand as ReceivedCommand
from pywavez.Transmission import Priority, CommandTransmission, MessageQueue

class ControllerNode:

    def __init__(self, id, controller):
        self._ControllerNode__id = id
        self._ControllerNode__controller = controller
        self.protocolInfo = None
        self.manufacturerInfo = None
        self.commandClassCodes = {}
        self.commandQueue = MessageQueue()
        self.commandClassVersion = {}
        self.commandClass = {}
        self.endPointReport = None
        self.nodeActiveEvent = asyncio.Event()
        self.noAckCount = 0
        self.noAckCountThreshold = 3
        self.wakeUpNotificationEvent = asyncio.Event()
        self.sendsWakeUpNotifications = False
        self.attemptInitializationTime = 0
        self._ControllerNode__initializationWait = 0
        self.commandDispatcherTask = spawnTask(self._ControllerNode__commandDispatcherTaskImpl())
        self.commandHandler = {(
 CommandClass.VERSION, 20): self.versionReportHandler, 
         (
 CommandClass.MANUFACTURER_SPECIFIC,
 5): self.manufacturerSpecificReportHandler, 
         
         (
 CommandClass.MULTI_CHANNEL,
 8): self.multiChannelEndpointReportHandler, 
         
         (
 CommandClass.MULTI_CHANNEL,
 10): self.multiChannelCapabilityReportHandler, 
         
         (
 CommandClass.MULTI_CHANNEL,
 13): self.multiChannelCmdEncapHandler, 
         
         (
 CommandClass.WAKE_UP, 7): self.wakeUpNotificationHandler}

    @property
    def id(self):
        return self._ControllerNode__id

    def shutdown(self):
        if self.commandDispatcherTask is not None:
            self.commandDispatcherTask.cancel()
            self.commandDispatcherTask = None

    def nodeActive(self):
        self.nodeActiveEvent.set()

    def sendCommand(self, command, *, endpoint=0, priority=Priority.DEFAULT):
        cmdtx = CommandTransmission(command,
          nodeId=(self._ControllerNode__id), endpoint=endpoint, priority=priority)
        self.commandQueue.add(cmdtx)
        return cmdtx

    def setCommandClasses(self, endpoint, cc_codes):
        try:
            cc_codes = cc_codes[0:cc_codes.index(239)]
        except ValueError:
            pass

        cc = []
        for code in cc_codes:
            try:
                cc.append(CommandClass(code))
            except ValueError:
                cc.append(code)

        cc = tuple(cc)
        self.commandClassCodes[endpoint] = cc
        for i in cc:
            vers = self.commandClassVersion.get((endpoint, i))
            cc_class = self.commandClass.get((endpoint, i))
            yield NodeUpdate.CommandClass(self._ControllerNode__id, endpoint, cc_class, i, vers)

        if self.attemptInitializationTime is None:
            if self._ControllerNode__needCommandClassVersion():
                self.attemptInitializationTime = 0
                self._ControllerNode__controller.initializationRequiredEvent.set()

    def handleApplicationCommandHandlerRequest(self, msg, endpoint=0):
        try:
            try:
                parsed_command = self.parse_command(msg.payload, endpoint)
            except Exception as ex:
                try:
                    logging.warning(f"Error parsing APPLICATION_COMMAND_HANDLER payload: {msg.payload!r} node={self._ControllerNode__id} exception: {ex!r}")
                    yield msg
                    return
                finally:
                    ex = None
                    del ex

            else:
                if parsed_command is None:
                    yield msg
                else:
                    yield from self.handleCommand(parsed_command, endpoint)
        finally:
            self.nodeActive()

    def parse_command(self, payload, endpoint):
        if len(payload) < 2:
            raise Exception(f"Short command: {payload!r}")
        cc_code, cmd_code = payload[0:2]
        cmd = None
        cc_enum = CommandClass(cc_code)
        try:
            cc = self.commandClass[(endpoint, cc_enum)]
        except KeyError:
            if (cc_code, cmd_code) not in (
             (
              CommandClass.VERSION.value, 20),
             (
              CommandClass.WAKE_UP.value, 7)):
                return
            cc = getCommandClassVersion(cc_code, 1)

        cmd = cc.commands[cmd_code]
        return cmd.fromBytes(payload)

    def handleCommand(self, cmd, endpoint):
        handler = self.commandHandler.get((
         cmd.CommandClassCode, cmd.CommandCode))
        if handler is None:
            yield ReceivedCommand(self._ControllerNode__id, endpoint, cmd)
        else:
            try:
                yield from handler(cmd, endpoint)
                return
            except Exception as ex:
                try:
                    logging.warning(f"Command handler raised exception: {ex!r} (endpoint: {endpoint} cmd: {cmd!r})")
                finally:
                    ex = None
                    del ex

    def versionReportHandler(self, cmd, endpoint):
        reqcc = cmd.requestedCommandClass
        try:
            reqcc = CommandClass(reqcc)
        except ValueError:
            pass

        vers = cmd.commandClassVersion
        self.commandClassVersion[(endpoint, reqcc)] = vers
        try:
            cc_class = getCommandClassVersion(reqcc, vers)
            self.commandClass[(endpoint, reqcc)] = cc_class
        except KeyError:
            cc_class = None

        yield NodeUpdate.CommandClass(self._ControllerNode__id, endpoint, cc_class, reqcc, vers)

    def manufacturerSpecificReportHandler(self, cmd, endpoint):
        if endpoint == 0:
            self.manufacturerInfo = cmd
            yield NodeUpdate.ManufacturerInfo(self._ControllerNode__id, cmd)

    def multiChannelEndpointReportHandler(self, cmd, endpoint):
        self.endPointReport = cmd
        return ()

    def multiChannelCapabilityReportHandler(self, cmd, endpoint):
        yield from self.setCommandClasses(cmd.endPoint, cmd.commandClass)
        if False:
            yield None

    def multiChannelCmdEncapHandler(self, cmd, endpoint):
        if cmd.bitAddress:
            to_us = bool(1 & cmd.destinationEndPoint)
        else:
            to_us = cmd.destinationEndPoint == 0
        if not to_us:
            yield ReceivedCommand(self._ControllerNode__id, 0, cmd)
            return
        payload = bytes((cmd.commandClass, cmd.command)) + cmd.parameter
        endpoint = cmd.sourceEndPoint
        try:
            parsed_command = self.parse_command(payload, endpoint)
        except Exception as ex:
            try:
                logging.warning(f"Error parsing MULTI_CHANNEL_CMD_ENCAP payload: {payload!r} node={self._ControllerNode__id} endpoint={endpoint} exception: {ex!r}")
                yield ReceivedCommand(self._ControllerNode__id, 0, cmd)
                return
            finally:
                ex = None
                del ex

        yield from self.handleCommand(parsed_command, endpoint)

    def wakeUpNotificationHandler(self, cmd, endpoint):
        if not self.sendsWakeUpNotifications:
            self.sendsWakeUpNotifications = True
            self.commandQueue.add(CommandTransmission(None, priority=(Priority.WAKE_UP)))
        if self.attemptInitializationTime is not None:
            self.attemptInitializationTime = 0
        self.nodeActive()
        self.wakeUpNotificationEvent.set()
        self._ControllerNode__controller.wakeUpNotification(self)
        return (ReceivedCommand(self._ControllerNode__id, endpoint, cmd),)

    async def __commandDispatcherTaskImpl(self):
        while True:
            if self.sendsWakeUpNotifications:
                await self.wakeUpNotificationEvent.wait()
                await self.commandQueue.waitForMessage(0.2)
                if self.commandQueue.hasMessage():
                    cmdtx = self.commandQueue.takeMessage()
                else:
                    for i in (1, 2, 3):
                        if await self._ControllerNode__transmitCommand(b'\x84\x08'):
                            break

                    self.wakeUpNotificationEvent.clear()
                    continue
            else:
                await waitForOne((self.nodeActiveEvent.wait()),
                  timeout=(random.gauss(30, 3)))
                cmdtx = await self.commandQueue.getMessage()
            if cmdtx.message is None:
                continue
            else:
                cmdtx.transmitting = True
                command = cmdtx.message
                if cmdtx.endpoint > 0:
                    multi_channel = self.commandClass.get((
                     0, CommandClass.MULTI_CHANNEL))
                    if multi_channel is None:
                        cmdtx.set_exception(Exception('Node does not support multi channel'))
                        continue
                    command = multi_channel.MultiChannelCmdEncap(sourceEndPoint=0,
                      destinationEndPoint=(cmdtx.endpoint),
                      bitAddress=False,
                      commandClass=(command.CommandClassCode),
                      command=(command.CommandCode),
                      parameter=(command.toBytes()[2:]))
                else:
                    command = command.toBytes()
                    if await self._ControllerNode__transmitCommand(command):
                        cmdtx.cancelled() or cmdtx.set_result(None)
                    else:
                        cmdtx.retransmission += 1
                        cmdtx.pauseUntil = time.monotonic() + 5
                        cmdtx.transmitting = False
                        self.commandQueue.addFirst(cmdtx)
            await asyncio.sleep(abs(random.gauss(0.2, 0.04)))

    async def __transmitCommand(self, command_bytes):
        func_id = await self._ControllerNode__controller._funcIdManager.get()
        if self.noAckCount % 2:
            tx_options = TransmitOption.ACK | TransmitOption.EXPLORE
        else:
            tx_options = TransmitOption.ACK | TransmitOption.AUTO_ROUTE
        try:
            retval = (await self._ControllerNode__controller.sendData(nodeId=(self._ControllerNode__id),
              data=command_bytes,
              txOptions=tx_options,
              funcId=(func_id.value))).retVal
        except Exception as ex:
            try:
                retval = False
                logging.warning(f"sendData(nodeId={self._ControllerNode__id}) raised exception: {ex!r}")
            finally:
                ex = None
                del ex

        if not retval:
            func_id.release()
            return False
        try:
            try:
                tx_complete = await asyncio.wait_for((func_id.future), timeout=65)
            except Exception:
                tx_complete = None

        finally:
            func_id.release()

        if tx_complete == TransmitComplete.OK:
            self.noAckCount = 0
            self.nodeActiveEvent.set()
            return True
        if tx_complete == TransmitComplete.NO_ACK:
            self.noAckCount += 1
            if self.noAckCount >= self.noAckCountThreshold:
                self.nodeActiveEvent.clear()
        return False

    async def attemptInitialization(self):
        add = 4
        try:
            if await self._ControllerNode__attemptInitializationImpl():
                self.attemptInitializationTime = None
                return
        except asyncio.CancelledError:
            self.attemptInitializationTime = time.monotonic() + 5
        except asyncio.TimeoutError:
            add = 2
        except Exception:
            traceback.print_exc()

        wait = self._ControllerNode__initializationWait = (self._ControllerNode__initializationWait + add) * 1.5
        self.attemptInitializationTime = time.monotonic() + abs(random.gauss(wait, wait / 5))

    async def __attemptInitializationImpl(self):
        logging.info(f"Attempt initialization: {self.id}")
        if self.protocolInfo is None:
            self.protocolInfo = await asyncio.wait_for(self._ControllerNode__controller.getNodeProtocolInfo(nodeId=(self._ControllerNode__id)),
              timeout=5)
            self._ControllerNode__controller._receivedMessages.append(NodeUpdate.ProtocolInfo(self._ControllerNode__id, self.protocolInfo))
            self._ControllerNode__initializationWait = 0
        if 0 not in self.commandClassCodes:
            while 0 not in self.commandClassCodes:
                self.nodeActiveEvent.clear()
                try:
                    await asyncio.wait_for(self._ControllerNode__controller.requestNodeInfo(nodeId=(self._ControllerNode__id)),
                      timeout=5)
                except asyncio.CancelledError:
                    raise
                except Exception:
                    pass

                await asyncio.wait_for((self.nodeActiveEvent.wait()), timeout=2)

            self._ControllerNode__initializationWait = 0
        CommandClassVersionV1 = getCommandClassVersion(CommandClass.VERSION, 1)
        while 1:
            init_tasks = []
            for endpoint, cc in set(((endpoint, cc) for endpoint, cc_codes in self.commandClassCodes.items() for cc in cc_codes)).difference(self.commandClassVersion):
                priority = 0 if endpoint != 0 else self._ControllerNode__initCCVersionPriority.get(cc, 0)
                self._ControllerNode__addInitTaskTo(init_tasks, f"getCommandClassVersion-{endpoint}-{cc}", (lambda endpoint, cc: lambda : (
                 endpoint, cc) not in self.commandClassVersion)(endpoint, cc), (lambda endpoint, cc: lambda : self.sendCommand(CommandClassVersionV1.CommandClassGet(requestedCommandClass=cc),
                  endpoint=endpoint,
                  priority=(priority + Priority.INITALIZATION)))(endpoint, cc))

            self._ControllerNode__addInitTaskTo(init_tasks, 'getMultiChannelEndpoints', lambda : self.endPointReport is None and hasattr(self.commandClass.get((0, CommandClass.MULTI_CHANNEL)), 'EndPointGet'), lambda : self.sendCommand(self.commandClass[(
             0, CommandClass.MULTI_CHANNEL)].EndPointGet()))
            self._ControllerNode__addInitTaskTo(init_tasks, 'getManufacturerInfo', lambda : self.manufacturerInfo is None and hasattr(self.commandClass.get((
             0, CommandClass.MANUFACTURER_SPECIFIC)), 'Get'), lambda : self.sendCommand(self.commandClass[(
             0, CommandClass.MANUFACTURER_SPECIFIC)].Get()))
            if self.endPointReport is not None:
                for ep in range(1, self.endPointReport.individualEndPoints + 1):
                    self._ControllerNode__addInitTaskTo(init_tasks, f"getMultiChannelEndpointCapabilities-{ep}", lambda ep: lambda : ep <= self.endPointReport.individualEndPoints and ep not in self.commandClassCodes(ep), lambda ep: lambda : self.sendCommand(self.commandClass[(
                     0, CommandClass.MULTI_CHANNEL)].CapabilityGet(endPoint=ep))(ep))

            if not init_tasks:
                return True
            random.shuffle(init_tasks)
            for t in init_tasks:
                if not await t.run():
                    return False

    _ControllerNode__initCCVersionPriority = {CommandClass.MANUFACTURER_SPECIFIC: 2, 
     CommandClass.MULTI_CHANNEL: 1, 
     CommandClass.VERSION: -1, 
     CommandClass.WAKE_UP: -1}

    def __needCommandClassVersion(self):
        return any(((endpoint, cc) not in self.commandClassVersion for endpoint, cc_codes in self.commandClassCodes.items() for cc in cc_codes))

    def __addInitTaskTo(self, list, key, condition, action):
        t = InitTask(self, key, condition, action)
        if t.check_condition():
            list.append(t)


class InitTask:

    def __init__(self, node, key, condition, action):
        self.node = node
        self.key = key
        self.condition = condition
        self.action = action

    def check_condition(self):
        try:
            return self.condition()
        except asyncio.CancelledError:
            raise
        except Exception:
            return True

    async def run(self):
        if not self.check_condition():
            return True
        logging.debug(f"Run init task {self.key!r} (node {self.node.id})")
        await asyncio.wait_for((self.action()), timeout=5)
        timeout = time.monotonic() + 2
        while 1:
            if not self.check_condition():
                return True
                if time.monotonic() >= timeout:
                    return False
                self.node.nodeActiveEvent.clear()
                try:
                    await asyncio.wait_for((self.node.nodeActiveEvent.wait()),
                      timeout=(timeout - time.monotonic()))
                except asyncio.CancelledError:
                    raise
                except Exception:
                    pass