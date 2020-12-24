# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\sake\network.py
# Compiled at: 2011-03-09 01:47:27
"""Network module

Implements RPC for client-server connections with session and access control
"""
import binascii, copy_reg, cPickle
from cStringIO import StringIO
from errno import ECONNRESET, ENOTCONN, ESHUTDOWN, ECONNABORTED
import logging, os, socket, struct, types, urllib, weakref, stackless
from stacklesslib.util import ValueEvent
from .const import ROLE_SERVICE, ROLE_ANY
from .errors import RpcTimeoutError, RpcError
from .process import Process
from . import util
from .util import Bunch
test = socket.socket()
try:
    test._sock.sendpacket
    HAVE_STACKLESSIO = True
except Exception:
    HAVE_STACKLESSIO = False

del test
HAVE_STACKLESSIO = False
RPC_API_VERSION = 14
PORT_ROOT = 10219
PORT_USER = 10211
RPC_CALL = 1
RPC_RETURN_OK = 2
RPC_RETURN_ERROR = 3
RPC_STREAM = 4
RPC_STREAMDATA = 5
RPC_PING = 6
SEGMENT_SIZE = 250000
DEFAULT_TIMEOUT = 3600.0
KEEPALIVE_PERIOD = 30.0
KEEPALIVE_TIMEOUT = 30.0
STATUS_WAIT_PERIOD = 10.0
ENDPOINT_OUTBOUND = 'Outbound'
ENDPOINT_INBOUND = 'Inbound'
MAX_CHUNKSIZE = 1024 * 1024
MAX_PACKETSIZE = 100 * 1024 * 1024
namespaceWhitelist = set([
 '__builtin__.dict',
 '__builtin__.tuple',
 '__builtin__.list',
 '__builtin__.set',
 '__builtin__.str',
 '__builtin__.unicode',
 'collections.defaultdict',
 'collections.deque',
 'copy_reg._reconstructor',
 'exceptions',
 'sake.errors',
 'sake.util.Bunch'])
namespaceSubstitutions = {}

def RegisterWhitelistAdditions(extras):
    """
    Register namespaces or classes that can be unpickled when they arrive
    in a networking packet.
    """
    global namespaceWhitelist
    namespaceWhitelist.update(extras)


def RegisterNamespaceSubstitution(fromNs, toNs):
    """
    Register a namespace transformation that should occur when unpickling
    objects that arrive in a networking packet.
    """
    ta = fromNs.rsplit('.', 1)
    tb = toNs.rsplit('.', 1)
    namespaceSubstitutions[tuple(ta)] = tuple(tb)


class HandlerExitEvent(Exception):
    pass


class DisconnectionEvent(HandlerExitEvent):
    pass


class Endpoint(object):
    """ The base endpoint class.  It cannot be used directly.  """

    def __init__(self, sock, service, origin):
        self.sock = sock
        self.service = service
        self.origin = origin
        self.addr, self.port = sock.getpeername()


class TextEndpoint(Endpoint):
    """
    This class is used to wrap incoming connections that are supposed to be
    RPC-based.  Before they can begin sending RPC-based packets, they need
    to pass at least a version check.
    """
    NEWLINE = '\r\n'
    ERROR_RESPONSE = 'ERROR'
    OKAY_RESPONSE = 'OK'
    PING_COMMAND = 'PING'
    RPC_COMMAND = 'RPC'
    STATUS_COMMAND = 'STATUS'
    lastStatusTime = None

    def __init__(self, sock, service, origin, rpcEndpointInfo=None):
        super(TextEndpoint, self).__init__(sock, service, origin)
        self.rfile = sock.makefile('rU')
        self.rpcEndpointInfo = rpcEndpointInfo
        if origin == ENDPOINT_INBOUND:
            self.service.New(self.Handler).name += ' - %s %s:%s' % (origin, self.addr, self.port)

    def Handler(self):
        try:
            while self.service.running and self.Pump():
                pass

        except socket.error as e:
            if e.args[0] not in [ECONNRESET, ENOTCONN, ESHUTDOWN, ECONNABORTED]:
                self.service.log.exception('Unexpected socket error')
            else:
                self.service.log.info('Unexpected %s.Handler disconnection (this is normal): %r', self.__class__.__name__, e)
        except Exception as e:
            self.service.log.exception('Unexpected network handler error')

    def Pump(self):
        bits = self.ReadLine()
        if len(bits) == 0:
            return False
        command = bits[0].upper()
        if command == self.STATUS_COMMAND:
            return self.CommandSTATUS(bits)
        if command == self.PING_COMMAND:
            return self.CommandPING(bits)
        if command == self.RPC_COMMAND:
            return self.CommandRPC(bits)
        self.SendResponse(self.ERROR_RESPONSE, 'unknown command')
        return True

    def SendCommand(self, commandName, *args):
        if self.service.logNetworkPackets:
            self.service.logNetworkPackets.info('%s:%s SendCommand %s %s', self.addr, self.port, commandName, args)
        argString = ''
        if len(args):
            argString += ' '
            argString += (' ').join(str(v) for v in args)
        self.sock.send(commandName + argString + self.NEWLINE)

    def SendResponse(self, responseType, *args):
        if self.service.logNetworkPackets:
            self.service.logNetworkPackets.info('%s:%s SendResponse %s %s', self.addr, self.port, responseType, args)
        argString = ''
        if len(args):
            argString += ' '
            argString += (' ').join(str(v) for v in args)
        self.sock.send(responseType + argString + self.NEWLINE)

    def ReadLine(self):
        line = self.rfile.readline()
        if line == '':
            return []
        bits = line.strip().split()
        if self.service.logNetworkPackets:
            self.service.logNetworkPackets.info('%s:%s ReadLine %s %s', self.addr, self.port, line, bits)
        return bits

    def Close(self):
        if self.sock:
            self.sock.close()
            self.sock = None
        return

    def Ping(self, time=1.0):
        """
        Send a :literal:`ping` command to the remote endpoint.
        """
        now = util.GetTime()
        iterations = 0
        while util.GetTime() < now + time:
            self.SendCommand(self.PING_COMMAND)
            bits = self.ReadLine()
            if len(bits) == 0 or bits[0] != self.OKAY_RESPONSE:
                return None
            iterations += 1

        elapsed = util.GetTime() - now
        return Bunch(ping=elapsed / iterations * 1000.0, iterations=iterations)

    def GetStatus(self):
        """
        Send a :literal:`command` command to the remote endpoint and return
        the result.
        """
        self.SendCommand(self.STATUS_COMMAND, *self.GetVersionArgs())
        bits = self.ReadLine()
        if len(bits) == 0 or bits[0] != self.OKAY_RESPONSE:
            return None
        status = bits[1]
        userCount = int(bits[2])
        motd = urllib.unquote(bits[3])
        return Bunch(userCount=userCount, status=status, motd=motd)

    def EngageRPCMode(self):
        """
        Send a :literal:`rpc` command to the remote endpoint.
        """
        self.SendCommand(self.RPC_COMMAND, *self.GetVersionArgs())
        bits = self.ReadLine()
        if len(bits) == 0:
            raise Exception('disconnected')
        if bits[0] != self.OKAY_RESPONSE:
            self.Close()
            raise Exception(*bits[1:])

    def GetVersionArgs(self):
        """
        Override this method to enable your application to negotiate an RPC
        connection with different or additional version arguments.

        The default behaviour is to pass the RPC API version.
        """
        return (
         RPC_API_VERSION,)

    def ParseVersionArgs(self, args):
        """
        Override this method to enable your application to negotiate an RPC
        connection with different or additional version arguments.

        The default behaviour is to extract the RPC API version.
        """
        try:
            return [
             int(args[1])]
        except (ValueError, IndexError):
            return [
             0]

    def _CheckAPIVersion(self, versionArgs):
        """
        Override this method to enable your application to negotiate an RPC
        connection with different or additional version arguments.
        
        The default behaviour is that clients can only engage in RPC with
        servers that have the same API version.
        """
        return versionArgs[0] == RPC_API_VERSION

    def CheckCompatibleVersion(self, versionArgs):
        """
        Override this method to enable your application to negotiate an RPC
        connection with different or additional version arguments.

        The default behaviour is to just check the RPC API version.
        """
        return self._CheckAPIVersion(versionArgs)

    def CommandRPCVersionCheck(self, versionArgs):
        """
        Override this method to enable your application to negotiate an RPC
        connection with different or additional version arguments.

        The default behaviour is to just check the RPC API version and to
        return a user targeted error message should it differ.
        """
        if not self._CheckAPIVersion(versionArgs):
            return 'Incompatible API version'

    def GetMOTD(self):
        """
        Override this method to enable your application to negotiate an RPC
        connection with different or additional version arguments.

        The default behaviour is to simply state the RPC version number
        (for what that's worth).
        """
        return urllib.quote('RPC %s' % RPC_API_VERSION)

    def CommandSTATUS(self, args):
        now = util.GetTime()
        if self.lastStatusTime is not None:
            nextPossibleNow = self.lastStatusTime + STATUS_WAIT_PERIOD
            if now < nextPossibleNow:
                self.service.app.Sleep(nextPossibleNow - now)
        self.lastStatusTime = now
        versionArgs = self.ParseVersionArgs(args)
        userCount = 0
        for ep in self.service.endpoints:
            if ep.session.userid:
                userCount += 1

        status = 'Online'
        if not self.CheckCompatibleVersion(versionArgs):
            status = 'Incompatible'
        self.SendResponse(self.OKAY_RESPONSE, status, userCount, self.GetMOTD())
        return True

    def CommandPING(self, args):
        self.SendResponse(self.OKAY_RESPONSE)
        return True

    def CommandRPC(self, args):
        versionArgs = self.ParseVersionArgs(args)
        failureMessage = self.CommandRPCVersionCheck(versionArgs)
        if failureMessage is None:
            endpointClass, endpointArgs, endpointKwArgs = self.rpcEndpointInfo
            ep = endpointClass(self.sock, self.service, self.origin, *endpointArgs, **endpointKwArgs)
            self.service.AddEndpoint(ep)
            self.SendResponse(self.OKAY_RESPONSE)
            return False
        else:
            self.SendResponse(self.ERROR_RESPONSE, failureMessage)
            return True


TextEndpointClass = TextEndpoint

class PacketEndpoint(Endpoint):
    """
    The packet-based endpoint that enables RPC connections.
    """

    def __init__(self, sock, service, origin, root):
        super(PacketEndpoint, self).__init__(sock, service, origin)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.rpcTimeout = DEFAULT_TIMEOUT
        self.session = service.sessionManager.CreateSession()
        if root:
            self.session.UpdateVariable(role=ROLE_SERVICE)
        self.session.ep = weakref.proxy(self)
        self.packetID = 1
        self.pending = {}
        self.streamID = 1
        self.streams = {}
        self.service.New(self.Handler).name += ' - %s %s:%s' % (origin, self.addr, self.port)
        self.service.log.debug('%s created', self)
        self.service.New(self.MonitorRemoteConnectivity)

    def __repr__(self):
        return 'Endpoint <%s %s:%s>' % (self.origin, self.addr, self.port)

    def MonitorRemoteConnectivity(self):
        try:
            self._MonitorRemoteConnectivity()
        except socket.error as e:
            if e.args[0] not in [ECONNRESET, ENOTCONN, ESHUTDOWN, ECONNABORTED]:
                self.service.log.exception('Unexpected socket error')
            else:
                self.service.log.info('Unexpected %s.Handler disconnection (this is normal): %r', self.__class__.__name__, e)
        except Exception as e:
            self.service.log.exception('Unexpected network handler error')

    def _MonitorRemoteConnectivity(self):
        self.service.log.info('MonitorRemoteConnectivity %s', self)
        lastTime = util.GetTime()
        while self.sock is not None:
            currentTime = util.GetTime()
            if currentTime - lastTime > KEEPALIVE_PERIOD:
                packetID = self.packetID
                self.packetID += 1
                rpcPacket = (
                 RPC_PING, packetID, currentTime)
                self.SendPacket(rpcPacket)
                lastTime = currentTime
            self.service.app.Sleep(1.0)

        return

    def _ReadExactly(self, size):
        bytes = bytearray(size)
        m = memoryview(bytes)
        pos = 0
        while pos < size:
            if self.sock is None:
                raise HandlerExitEvent('socket closed during reads')
            read = self.sock.recv_into(m[pos:])
            if not read:
                raise DisconnectionEvent('socket appeared to give EOF during packet read')
            pos += read

        return bytes

    def _ReadExactlyChunked(self, size):
        if size <= MAX_CHUNKSIZE:
            return self._ReadExactly(size)
        chunks = []
        while size:
            chunksize = min(size, MAX_CHUNKSIZE)
            chunks.append(self._ReadExactly(chunksize))
            size -= chunksize

        return ('').join(chunks)

    def _WriteExactly(self, data):
        bytesSent = self.sock.send(data)
        if bytesSent != len(data):
            raise RuntimeError('WriteExactly: Wanted to write %s bytes but only managed %s bytes' % (len(data), bytesSent))

    def SendPacket(self, packet, _inTasklet=False):
        if self.service.fakeLatency > 0.0:
            if not _inTasklet:
                self.service.New(self.SendPacket, packet, _inTasklet=True)
                return
            self.service.app.Sleep(self.service.fakeLatency)
        data = modified_cPickle_dumps(packet)
        if self.service.logNetworkPackets:
            logData = data[:1024]
            checksum = binascii.crc32(logData)
            self.service.logNetworkPackets.info('Sending packet to %s:%s length %d checksum %x data %r', self.addr, self.port, len(data), checksum, logData)
        if HAVE_STACKLESSIO:
            return self.sock._sock.sendpacket(data)
        data = struct.pack('!i', len(data)) + data
        self._WriteExactly(data)

    def ReceivePacket(self):
        if self.service.fakeLatency > 0.0:
            self.service.app.Sleep(self.service.fakeLatency)
        if HAVE_STACKLESSIO:
            packet = self.sock._sock.recvpacket()
            if packet is None:
                raise DisconnectionEvent('socket appeared to give EOF during packet read')
        else:
            header = self._ReadExactly(4)
            size = struct.unpack('!i', header)[0]
            if size < 0 or size > MAX_PACKETSIZE:
                raise DisconnectionEvent('Invalid packet header %r with size %d bytes received' % (struct.pack('!i', size), size))
            packet = self._ReadExactlyChunked(size)
        if self.service.logNetworkPackets:
            logData = packet[:1024]
            checksum = binascii.crc32(logData)
            self.service.logNetworkPackets.info('Received packet from %s:%s length %d checksum %x data %r', self.addr, self.port, len(packet), checksum, logData)

        def find_global(moduleName, className):
            t = namespaceSubstitutions.get((moduleName, className), None)
            if t is not None:
                moduleName, className = t
            mod = __import__(moduleName, globals(), locals(), [])
            idx = moduleName.rfind('.')
            if idx != -1:
                subModuleName = moduleName[idx + 1:]
                mod = getattr(mod, subModuleName)
            obj = getattr(mod, className)
            if moduleName + '.' + className in namespaceWhitelist or moduleName in namespaceWhitelist:
                return obj
            raise cPickle.UnpicklingError('%s.%s is not whitelisted for unpickling' % (moduleName, className))
            return

        unpickler = cPickle.Unpickler(StringIO(packet))
        unpickler.find_global = find_global
        return unpickler.load()

    def Call(self, method, *args, **kw):
        """Call(method, ...) -> value
        Calls the remote method and returns the value.
        'method' is of the form "serviceName.methodName".
        """
        return self._CallMethod(method, True, None, args, kw)

    def CallWithTimeoutOverride(self, method, timeout, *args, **kw):
        """Call(method, ...) -> value
        Calls the remote method and returns the value.
        'method' is of the form "serviceName.methodName".
        """
        return self._CallMethod(method, True, timeout, args, kw)

    def CallAsync(self, method, *args, **kw):
        """CallAsync(method, ...) -> value
        Calls the remote method and discards the return value. This function returns immediately.
        'method' is of the form "serviceName.methodName".
        """
        oldValue = stackless.getcurrent().block_trap
        stackless.getcurrent().block_trap = True
        try:
            self._CallMethod(method, False, None, args, kw)
        finally:
            stackless.getcurrent().block_trap = oldValue

        return

    def _CallMethod(self, method, synchronous, timeout, args, kw):
        assert type(synchronous) == types.BooleanType
        serviceName, methodName = method.rsplit('.', 1)
        if self.session is None:
            raise RpcError("Can't do RPC on a closed endpoint.")
        if timeout is None:
            timeout = self.rpcTimeout
        else:
            self.service.log.info("RPC call timeout override of %s for '%s'", timeout, method)
        if synchronous:
            packetID = self.packetID
            self.pending[packetID] = ValueEvent(timeout, RpcTimeoutError, (serviceName, methodName))
            if self.service.logNetworkRPC:
                self.service.logNetworkRPC.info('Call/OUT %d %s.%s to %s:%s', packetID, serviceName, methodName, self.addr, self.port)
            self.packetID += 1
        else:
            packetID = None
            if self.service.logNetworkRPC:
                self.service.logNetworkRPC.info('Notification/OUT %s.%s to %s:%s', serviceName, methodName, self.addr, self.port)
        rpcPacket = (
         RPC_CALL, serviceName, methodName, packetID, args, kw)
        if synchronous:
            self._SendPacketWrap(rpcPacket)
            return self.pending[packetID].wait()
        else:
            self.service.New(self._SendPacketWrap, rpcPacket).name += ' - RPC call to %s.%s' % (serviceName, methodName)
            return

    def SendFile(self, method, fileObject, *args, **kw):
        try:
            return self._SendFile(method, fileObject, *args, **kw)
        except socket.error as e:
            if e.args[0] not in [ECONNRESET, ENOTCONN, ESHUTDOWN, ECONNABORTED]:
                self.service.log.exception('Unexpected socket error')
            else:
                self.service.log.info('Unexpected %s.SendFile disconnection (this is normal): %r', self.__class__.__name__, e)
        except Exception as e:
            self.service.log.exception('Unexpected network handler error')

    def _SendFile(self, method, fileObject, *args, **kw):
        fileObject.seek(0, os.SEEK_END)
        fileSize = fileObject.tell()
        fileObject.seek(0, os.SEEK_SET)
        args = (
         fileSize,) + args
        serviceName, methodName = method.rsplit('.', 1)
        if self.session is None:
            raise RpcError("Can't do RPC on a closed endpoint.")
        streamID = self.streamID
        self.streamID += 1
        self.service.log.info('SendFile starting of stream %d to %s with args %s', streamID, method, args)
        rpcPacket = (
         RPC_STREAM, serviceName, methodName, streamID, args, kw)
        self._SendPacketWrap(rpcPacket)
        segmentID = 1
        while True:
            segment = fileObject.read(SEGMENT_SIZE)
            if segment == '':
                break
            rpcPacket = (
             RPC_STREAMDATA, streamID, segmentID, segment)
            self._SendPacketWrap(rpcPacket)
            segmentID += 1

        self.service.log.info('SendFile completed stream %d', streamID)
        return

    def _SendPacketWrap(self, rpcPacket):
        try:
            self.SendPacket(rpcPacket)
        except Exception as e:
            packetID = None
            if rpcPacket[0] == RPC_CALL:
                packetID = rpcPacket[3]
            if packetID:
                self.pending[packetID].abort(e.__class__, e.args)
            elif rpcPacket[0] == RPC_CALL:
                if isinstance(e, socket.error):
                    if e.args[0] not in [ECONNRESET, ENOTCONN, ESHUTDOWN, ECONNABORTED]:
                        self.service.log.exception('Unexpected socket error')
                    else:
                        self.service.log.info('Unexpected %s._SendPacketWrap disconnection (this is normal): %r', self.__class__.__name__, e)
                else:
                    self.service.log.exception('Unexpected network handler error')
            else:
                raise

        return

    def ReceiveAndDispatch(self):
        packet = self.ReceivePacket()
        packetType = packet[0]
        if packetType == RPC_CALL:
            self.service.New(self.Dispatch, packet)
        elif packetType == RPC_RETURN_OK:
            type, packetID, value = packet
            if self.service.logNetworkRPC:
                self.service.logNetworkRPC.info('CallResponse/IN %d', packetID)
            self.pending[packetID].set(value)
            del self.pending[packetID]
        elif packetType == RPC_RETURN_ERROR:
            type, packetID, exc, args = packet
            if self.service.logNetworkRPC:
                self.service.logNetworkRPC.info('CallResponseError/IN %d', packetID)
            self.pending[packetID].abort(exc, args)
            del self.pending[packetID]
        elif packetType == RPC_STREAM:
            self.OpenStream(packet)
        elif packetType == RPC_STREAMDATA:
            self.DeliverStreamData(packet)
        elif packetType == RPC_PING:
            self.ProcessPing(packet)
        else:
            raise RuntimeError('ReceiveCall:  Unknown packet type %s' % packetType)

    def ProcessPing(self, packet):
        packetType, packetID, remoteTime = packet

    def OpenStream(self, packet):
        packetType, serviceName, methodName, streamID, args, kw = packet
        generator = self.CallServiceMethod(serviceName, methodName, args, kw)
        generator.next()
        self.streams[streamID] = [
         generator, util.GetTime()]

    def DeliverStreamData(self, packet):
        packetType, streamID, chunkID, segment = packet
        streamHandler = self.streams[streamID][0]
        try:
            streamHandler.send((chunkID, segment))
            self.streams[streamID][1] = util.GetTime()
        except StopIteration:
            del self.streams[streamID]

    def Dispatch(self, packetIn):
        packetType, serviceName, methodName, packetID, args, kw = packetIn
        if self.service.logNetworkRPC:
            if packetID is not None:
                self.service.logNetworkRPC.info('Call/IN %d %s.%s from %s:%s', packetID, serviceName, methodName, self.addr, self.port)
            else:
                self.service.logNetworkRPC.info('Notification/IN %s.%s from %s:%s', serviceName, methodName, self.addr, self.port)
        stackless.getcurrent().name += ' - RPC dispatch of %s.%s' % (serviceName, methodName)
        try:
            ret = self.CallServiceMethod(serviceName, methodName, args, kw)
            packetOut = (RPC_RETURN_OK, packetID, ret)
        except Exception as e:
            self.service.log.exception('Dispatching of remote call on behalf of %s failed.', self.session)
            packetOut = (RPC_RETURN_ERROR, packetID, e.__class__, e.args)

        if packetID and self.sock is not None:
            self.SendPacket(packetOut)
            if self.service.logNetworkRPC:
                desc = 'result'
                if packetOut[0] == RPC_RETURN_ERROR:
                    desc = 'error'
                self.service.logNetworkRPC.info('Call/OUT %d %s', packetID, desc)
        return

    def FlushStaleStreams(self):
        for streamID, (stream, lastRecvTime) in self.streams.items():
            secondsSinceLastRecv = util.GetTime() - lastRecvTime
            if secondsSinceLastRecv > 20:
                del self.streams[streamID]
                stream.throw(Exception, 'Stale stream death')
                self.service.log.error('Flushed stream %d after %d seconds of inactivity', streamID, secondsSinceLastRecv)

    def CallServiceMethod(self, serviceName, methodName, args, kw):
        return self.session.CallServiceMethod(serviceName, methodName, args, kw)

    def Handler(self):
        try:
            while self.service.running:
                self.ReceiveAndDispatch()
                self.FlushStaleStreams()

        except HandlerExitEvent as e:
            self.service.log.info('Expected disconnection (this is normal): %r', e)
        except socket.error as e:
            if e.args[0] not in [ECONNRESET, ENOTCONN, ESHUTDOWN, ECONNABORTED]:
                self.service.log.exception('Unexpected socket error')
            else:
                self.service.log.info('Unexpected %s.Handler disconnection (this is normal): %r', self.__class__.__name__, e)
        except Exception as e:
            self.service.log.exception('Unexpected network handler error')

        self.Close()

    def Close(self):
        """ Close this endpoint. """
        if self.session:
            self.session.Close()

    def SessionClosing(self, session):
        self.service.RemoveEndpoint(self)
        self.session = None
        self.sock = None
        self.service.log.info('SessionClosing: destroyed %s', self)
        return

    def RequestObject(self, serviceName, objectName, objectID):
        remoteObjectID = self._CallMethod('connection', 'RemoteRequestObject', True, None, (serviceName, objectName, objectID), {})
        robject = RemoteObject(self, remoteObjectID)
        return robject

    def Ping(self, time=1.0):
        now = util.GetTime()
        iterations = 0
        while util.GetTime() < now + time:
            self.Call('connection.Pong')
            iterations += 1

        elapsed = util.GetTime() - now
        return Bunch(ping=elapsed / iterations * 1000.0, iterations=iterations)


class ConnectionService(Process):
    serviceName = 'connection'
    serviceIncludes = ['sessionManager']
    serviceAllowRPC = True

    def __init__(self):
        Process.__init__(self)

    def StartProcess(self):
        self.endpoints = []
        self.acceptors = []
        self.remotables = {}
        self.remotablesByObjectID = {}
        self.remoteObjectIDCounter = 1000
        self.fakeLatency = self.app.config.getfloat('Settings', 'fakeLatencySeconds')
        self.logNetworkPackets = None
        if self.app.config.getboolean('Logging', 'networkPackets'):
            self.logNetworkPackets = logging.getLogger('networkPackets')
        self.logNetworkRPC = None
        if self.app.config.getboolean('Logging', 'networkRPC'):
            self.logNetworkRPC = logging.getLogger('networkRPC')
        return

    def StopProcess(self):
        for ep in self.endpoints:
            ep.session.Close()

    def AddEndpoint(self, ep):
        self.endpoints.append(ep)

    def RemoveEndpoint(self, ep):
        self.endpoints.remove(ep)

    def SetFakeLatency(self, ms):
        self.fakeLatency = ms

    def StartAccepting(self, port, portType=None, endpointClass=PacketEndpoint):
        if portType is None:
            if port == PORT_ROOT:
                portType = 'root'
            elif port == PORT_USER:
                portType = 'user'
            else:
                portType = 'custom'
        s = socket.socket()
        try:
            s.bind(('0.0.0.0', port))
            s.listen(5)
        except socket.error as e:
            self.log.warning('Connection service not accepting connection on %s port %s because: %s', portType, port, e)
            return

        self.acceptors.append(s)
        self.log.info('Connection service now accepting on %s port %s', portType, port)
        self.New(self._Accept, s, port == PORT_ROOT, portType, endpointClass).name += ' - accepting on %s port %s' % (portType, port)
        return

    def _Accept(self, s, root, portType, endpointClass):
        rpcEndpointInfo = (endpointClass, (root,), {})
        while self.running:
            sock, addr = s.accept()
            self.log.info('Connection service: Accepted a %s connection from %s:%s', portType, addr[0], addr[1])
            TextEndpointClass(sock, self, ENDPOINT_INBOUND, rpcEndpointInfo)

    def Connect(self, addressTuple, remoteHostRole=ROLE_SERVICE, endpointClass=PacketEndpoint):
        sock = socket.socket()
        sock.connect(addressTuple)
        if issubclass(endpointClass, PacketEndpoint):
            ep = TextEndpointClass(sock, self, ENDPOINT_OUTBOUND)
            ep.EngageRPCMode()
            ep = endpointClass(sock, self, ENDPOINT_OUTBOUND, False)
            self.endpoints.append(ep)
            ep.session.LocalUpdateVariable(role=remoteHostRole)
            return weakref.proxy(ep)
        return endpointClass(sock, self, ENDPOINT_OUTBOUND)

    def RemoteRequestObject(self, _session, serviceName, objectName, objectID):
        """Called by clients, returns remoteObjectID"""
        objectKey = (
         serviceName, objectName, objectID)
        if objectKey in self.remotables:
            object = self.remotables[objectKey]
        else:
            object = _session.CallServiceMethod(serviceName, 'RequestObject', (objectName, objectID), {})
            if not isinstance(object, Remotable):
                raise RuntimeError("GetRemoteHandle: Object '%s' must inherit from Remotable" % object)
            object.connectService = self
            object.sessions = []
            object.remoteObjectID = self.remoteObjectIDCounter
            object.objectKey = objectKey
            self.remoteObjectIDCounter += 1
            self.remotables[objectKey] = object
            self.remotablesByObjectID[object.remoteObjectID] = object
        _session.AttachToRemotable(object)
        return object.remoteObjectID

    RemoteRequestObject.access = ROLE_ANY

    def RemoteObjectCall(self, _session, remoteObjectID, methodName, args, kw):
        if remoteObjectID not in self.remotablesByObjectID:
            raise RuntimeError("RemoteObjectCall: Object with id %s doesn't exist" % remoteObjectID)
        object = self.remotablesByObjectID[remoteObjectID]
        _session.AttachToRemotable(object)
        return _session.CallBoundMethod(object.__class__.__name__, getattr(object, methodName), args, kw)

    RemoteObjectCall.access = ROLE_ANY

    def Pong(self):
        """Pong() -> None
        This method does nothing. Used by Endpoint.Ping() to measure roundtrip time.
        """
        pass

    Pong.access = ROLE_ANY


class Remotable(object):

    def SessionAttach(self, session):
        logging.root.info('--> SessionAttach %r', session)

    def SessionDetach(self, session):
        logging.root.info('--> SessionDetach %r', session)

    def SessionChanges(self, session, changes):
        logging.root.info('--> SessionChanges %r %r', session, changes)
        for key, change in changes.iteritems():
            self.SessionChange(session, key, change[0])

    def SessionChange(self, session, key, oldValue):
        logging.root.info('--> SessionChange %r %r', session, key)

    def Teardown(self):
        """Call this to tear down all remotable object bookkeeping and session attachments"""
        del self.connectService.remotables[self.objectKey]
        del self.connectService.remotablesByObjectID[self.remoteObjectID]
        while self.sessions:
            self.sessions[0].DetachFromRemotable(self)


class RemoteObjectCall(object):

    def __init__(self, remoteObject, name):
        self.remoteObject = remoteObject
        self.name = name

    def __call__(self, *args, **kw):
        return self.remoteObject.ep.Call('connection.RemoteObjectCall', self.remoteObject.remoteObjectID, self.name, args, kw)


class RemoteObject(object):

    def __init__(self, ep, remoteObjectID):
        self.ep = ep
        self.remoteObjectID = remoteObjectID

    def __repr__(self):
        return 'RemoteObject <id=%s ep=%s>' % (self.remoteObjectID, self.ep)

    def __getattr__(self, name):
        return RemoteObjectCall(self, name)

    def Call(self, methodName, *args, **kw):
        return self.ep.Call('connection.RemoteObjectCall', self.remoteObjectID, methodName, args, kw)

    def CallAsync(self, methodName, *args, **kw):
        return self.ep.CallAsync('connection.RemoteObjectCall', self.remoteObjectID, methodName, args, kw)


reducers = {}

def register_pickle_convertor(source_type, convertor_func):
    """
    Programmers writing code making use of objects created outside this mini-framework
    may wish to be able to be able to have them be passed across the wire to RPC callers
    without any extra work.  This can be done by registering a conversion function
    using the following logic.

    .. code-block:: python

        from sake import network
        network.register_pickle_convertor(dbutil.CRowset, crowset_pickler)

    The object will be converted into a form that can be deserialised on the other side
    of the connection, and sent for use there.  In the current use cases, these
    objects tend to be Python implementations with almost exact API and usage semantics
    as the source C++ implemented object.

    When unpickling an object, an :py:class:`Unpickler <pickle.Unpickler>` object can be
    used and its :py:func:`find_global <pickle.Unpickler.find_global>` method can be
    overriden to give localised white listing behaviour.  However, there is no similar
    localised conversion for :py:class:`Pickler <pickle.Pickler>` objects.  And as
    :py:func:`copy_reg.pickle` puts a convertor into play for all pickling operations, it
    is unsuitable for use.  We only want to apply these transformations to objects
    serialised to go over the wire, so we are forced to install and remove our
    convertors for each pickling operation.
    """
    global reducers
    copy_reg.pickle(source_type, convertor_func)
    del copy_reg.dispatch_table[source_type]
    logging.root.info('Registered sake RPC convertor for objects of type %r', source_type)
    reducers[source_type] = convertor_func


def modified_cPickle_dumps(obj):
    copy_reg.dispatch_table.update(reducers)
    try:
        return cPickle.dumps(obj, cPickle.HIGHEST_PROTOCOL)
    finally:
        for source_type in reducers:
            del copy_reg.dispatch_table[source_type]