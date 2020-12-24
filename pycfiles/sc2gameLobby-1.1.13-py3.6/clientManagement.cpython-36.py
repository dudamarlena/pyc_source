# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sc2gameLobby\clientManagement.py
# Compiled at: 2018-09-27 21:15:14
# Size of source mod 2**32: 5999 bytes
from s2clientprotocol import sc2api_pb2
from pysc2.lib import protocol
from pysc2.lib import remote_controller
import portpicker, queue, socket, sys, time, websocket
from sc2gameLobby import gameConstants as c

class ClientController(remote_controller.RemoteController):
    __doc__ = 'similar to pysc2 StarcratProcess, but without the process to enable multiple game connections'

    def __init__(self, url=None, port=None, timeout=c.INITIAL_TIMEOUT):
        sys.argv = sys.argv[:1]
        FLAGS = protocol.flags.FLAGS
        FLAGS(sys.argv)
        self._url = None
        self._port = None
        self._client = None
        self._name = ''
        if url != None or port != None:
            self.connect(url=url, port=port, timeout=timeout)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        url = ' %s' % self._url if self._url else ''
        port = ':%s' % self._port if self._port else ''
        try:
            stat = self.status
        except:
            stat = 'disconnected'

        return '<%s%s%s %s>' % (self.name, url, port, stat)

    def __nonzero__(self):
        """whether this ClientController is connected"""
        try:
            self.status
        except:
            return False
        else:
            return True

    @property
    def name(self):
        if not self._name:
            self._name = str(self.__class__).split('.')[(-1)].rstrip("'>")
        return self._name

    def close(self):
        """Shut down the socket connection, client and controller"""
        self._sock = None
        self._controller = None
        if hasattr(self, '_port'):
            if self._port:
                portpicker.return_port(self._port)
                self._port = None

    def __enter__(self):
        return self

    def __exit__(self, unused_exception_type, unused_exc_value, unused_traceback):
        self.close()

    def __del__(self):
        self.close()

    def connect(self, url=c.LOCALHOST, port=None, timeout=c.INITIAL_TIMEOUT, debug=False):
        """socket connect to an already running starcraft2 process"""
        if port != None:
            if self._port != None:
                portpicker.return_port(self._port)
            self._port = port
        else:
            if self._port == None:
                self._port = portpicker.pick_unused_port()
        self._url = url
        if ':' in url:
            if not url.startswith('['):
                url = '[%s]' % url
        for i in range(timeout):
            startTime = time.time()
            if debug:
                print('attempt #%d to websocket connect to %s:%s' % (i, url, port))
            try:
                finalUrl = 'ws://%s:%s/sc2api' % (url, self._port)
                ws = websocket.create_connection(finalUrl, timeout=timeout)
                self._client = protocol.StarcraftProtocol(ws)
                return self
            except socket.error:
                pass
            except websocket.WebSocketException as err:
                print(err, type(err))
                if 'Handshake Status 404' in str(err):
                    pass
                else:
                    raise
            except Exception as e:
                print(type(e), e)

            sleepTime = max(0, 1 - (time.time() - startTime))
            if sleepTime:
                time.sleep(sleepTime)

        raise websocket.WebSocketException('Could not connect to game at %s on port %s' % (url, port))

    @remote_controller.valid_status(remote_controller.Status.in_game)
    def debug(self, *debugReqs):
        """send a debug command to control the game state's setup"""
        return self._client.send(debug=sc2api_pb2.RequestDebug(debug=debugReqs))

    def getNewReplay(self):
        request = sc2api_pb2.RequestReplayInfo(replay_path='dummy.SC2Replay', download_data=True)
        return self._client.send(replay_info=request)


ClientController.__bool__ = ClientController.__nonzero__