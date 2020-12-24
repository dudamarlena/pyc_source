# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/site-packages/canteen/logic/realtime.py
# Compiled at: 2014-09-26 04:50:19
__doc__ = '\n\n  realtime logic\n  ~~~~~~~~~~~~~~\n\n  :author: Sam Gammon <sg@samgammon.com>\n  :copyright: (c) Sam Gammon, 2014\n  :license: This software makes use of the MIT Open Source License.\n            A copy of this license is included as ``LICENSE.md`` in\n            the root of the project.\n\n'
import time, hashlib
from ..base import logic
from ..util import struct
from ..util import decorators
_ORIGIN_ENV_ITEM = 'HTTP_ORIGIN'
_SOCKET_KEY_ENV_ITEM = 'HTTP_SEC_WEBSOCKET_KEY'
_FORWARDED_FOR_ENV_ITEM = 'HTTP_X_FORWARDED_FOR'
TERMINATE = struct.Sentinel('TERMINATE')

class TerminateSocket(Exception):
    """ Exception that can be raised from the inner receive/send coroutine to
      gracefully (or non-gracefully) close an active realtime communication
      session. """
    __graceful__ = False

    def __init__(self, graceful=False):
        """ Initialize this ``TerminateSocket`` exception.

        :param graceful: ``bool`` flag indicating whether to gracefully close
          the connection or force a close. ``True`` tries to close the socket
          gracefully, ``False`` does not. """
        self.__graceful__ = graceful

    graceful = property(lambda self: self.__graceful__)


class RealtimeSocket(object):
    """ Specifies a structure for keeping track of socket details during a
      live realtime communication session. Simple things like the local/remote
      address/port pairs are used to make a socket ID that can be passed around
      and used as a reference. """
    __slots__ = ('__id__', '__state__', '__local__', '__remote__', '__runtime__', '__established__')

    class State(struct.BidirectionalEnum):
        """ Enumerates available ``RealtimeSocket`` states, or the phases of a
        realtime communication session. """
        INIT = 0
        OPEN = 1
        ACTIVE = 2
        CLOSED = 3
        ERROR = 4

    def __init__(self, runtime, local, remote):
        """ Initialize this ``RemoteSocket`` object with details about the current
        ``runtime`` and the connection's ``local`` and ``remote`` peers.

        :param runtime: Currently-active Canteen runtime.

        :param local: Local (server) address & port pair that is handling the
          connection.

        :param remote: Remote (client) address & port pair that is on the other
          side of the connection. """
        self.__local__, self.__remote__ = local, remote
        self.__id__, self.__runtime__, self.__established__ = hashlib.sha1(('::').join((local, remote))).hexdigest(), runtime, int(time.time())

    def __hash__(self):
        """ Return the local socket's ID.

        :returns: This ``RealtimeSocket``'s ID for hashability. """
        return self.__id__

    def __repr__(self):
        """ Return a humanized string representation of this ``RealtimeSocket``.

        :returns: This ``RealtimeSocket``'s humanized ``repr``. """
        return '%s(id=%s, state=%s, local=%s, remote=%s, established=%s)' % (
         self.__class__.__name__,
         self.__id__,
         self.State.reverse_resolve(self.__state__),
         self.__local__,
         self.__remote__,
         self.__established__)

    def set_state(self, state):
        """ Set the current state of this ``RealtimeSocket``. Available states are
        enumerated in a ``BidirectionalEnum`` at ``self.State``. Current state
        is stored in the object-private ``__state__``.

        :param state: ``State`` to set the current socket to.
        :returns: ``self``, for chainability. """
        return setattr(self, '__state__', state) or self

    def receive(self):
        """ Callable to reach through to the currently-active runtime and attempt
        to receive communication from the client-side of an active realtime
        communication session.

        :returns: Next message from the client (in a blocking/nonblocking way
         depending on the runtime's implementation). """
        return self.__runtime__.receive()

    def send(self, payload):
        """ Send a payload, via the currently-active runtime, to the client-side of
        the current realtime communication session.

        :param payload: Package of data to send to the client via the currently
          active realtime communication session.

        :returns: ``None``. """
        self.__runtime__.send(buffer(payload) if isinstance(payload, bytearray) else payload, binary=isinstance(payload, bytearray))

    def close(self, graceful=True):
        """ Close the current realtime communication session (``graceful``ly or not,
        at the end of this function, it shall be closed).

        :param graceful: Attempt to close the connection with a ``FIN`` packet
          instead of simply resetting it.

        :returns: ``self``, for chainability. """
        self.__runtime__.close(graceful)
        return self

    id, state, local, remote, runtime, established = (
     property(lambda self: self.__id__),
     property(lambda self: self.__state__),
     property(lambda self: self.__local__),
     property(lambda self: self.__remote__),
     property(lambda self: self.__runtime__),
     property(lambda self: self.__established__))


@decorators.bind('realtime', namespace=True)
class RealtimeSemantics(logic.Logic):
    """ Provides logic structure to handle realtime-style (acyclic) dispatch
      flows, as opposed to HTTP-style (cyclic) ones. Used in cases like
      WebSockets that provide a live bidirectional link. """
    hint = _SOCKET_KEY_ENV_ITEM

    def stream(self, target, send):
        """ Prepare to consume a stream of packets/messages from ``target``, using
        ``send`` as a callback to transmit messages back to the client.

        Returns a ``responder`` generator that acts as a coroutine-style Python
        generator. Consumes messages via ``send`` and ``yield``s messages to be
        sent.

        :param target: Callable for consuming/receiving/blocking on new data
          from the client.

        :param send: Callable for sending data to the client.

        :returns: Prepared ``responder`` generator. """

        def responder(dispatch):
            """ Inner closure ``responder``, acts as a coroutine-style Python
          generator to consume packets from a realtime-enabled client
          connection, ``dispatch`` for a potential response, and forward
          outbound messages back to the client.

          :param dispatch: Application callable that should handle the inbound
            message, potentially ``yield``ing messages to be sent.

          :returns: Never. """
            while True:
                inbound = yield
                if inbound is TERMINATE:
                    raise TerminateSocket(graceful=True)
                if inbound is not None:
                    for outbound in dispatch(inbound):
                        if outbound is TERMINATE:
                            raise TerminateSocket(graceful=True)
                        send(outbound)

            return

        gen = responder(target)
        gen.next()
        return gen

    def on_connect(self, handler):
        """ Top-level ``on_connect`` logic that provides initialization for a
        ``RealtimeSocket`` session.

        :param handler: Active ``RealtimeHandler`` instance that is handling
          this realtime session.

        :returns: :py:class:`RealtimeSocket` instance describing the
          newly-active realtime session. """
        handler.runtime.handshake(*(
         handler.request.environ[self.hint],
         handler.request.environ.get(_ORIGIN_ENV_ITEM, '')))
        sock = RealtimeSocket(handler.runtime, **{'local': handler.request.host, 
           'remote': handler.request.remote_addr})
        sock.set_state(sock.State.INIT)
        handler.on_connect()
        sock.set_state(sock.State.OPEN)
        return sock

    def on_message(self, handler, socket):
        """ Top-level ``on_message` logic that provides dispatch for inbound
        realtime messages.

        :param handler: Active ``RealtimeHandler`` instance that is handling
          this realtime session.

        :param socket: Active ``RealtimeSocket`` instance for the currently-
          active realtime session.

        :returns: ``None``, upon connection close. """
        responder = self.stream(handler.on_message, socket.send)
        socket.set_state(socket.State.ACTIVE)
        _terminate = False
        try:
            try:
                while not _terminate:
                    try:
                        inbound = socket.receive()
                        if inbound == TERMINATE:
                            raise TerminateSocket(graceful=True)
                        elif inbound:
                            responder.send(inbound)
                    except TerminateSocket as e:
                        if e.graceful:
                            _terminate = True
                        else:
                            raise
                    except (GeneratorExit, StopIteration):
                        break

            except TerminateSocket:
                pass

        finally:
            if not _terminate:
                socket.set_state(socket.State.ERROR)
            self.on_close(handler, socket)

    def on_close(self, handler, socket):
        """ Top-level ``on_close`` logic that provides cleanup logic for realtime
        communication sessions.

        :param handler: Currently-active ``RealtimeHandler`` instance that is
          managing this realtime session.

        :param socket: ``RealtimeSocket`` object describing the currently-
          active realtime session.

        :returns: ``self``, for chainability. """
        if socket.state is not socket.State.ERROR:
            socket.set_state(socket.State.CLOSED)
        handler.on_close(socket.state is not socket.State.ERROR)
        return self


__all__ = ('RealtimeSocket', 'RealtimeSemantics')