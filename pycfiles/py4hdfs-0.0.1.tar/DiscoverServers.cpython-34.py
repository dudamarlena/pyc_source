# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.4/lib/python3.4/site-packages/org/py4grid/multicast/daemons/DiscoverServers.py
# Compiled at: 2014-04-01 16:29:10
# Size of source mod 2**32: 3045 bytes
__doc__ = '\nPY4GRID : a little framework to simule multiprocessing over a lot of computers\nCopyright (C) 2014  João Jorge Pereira Farias Junior\nThis program is free software: you can redistribute it and/or modify\nit under the terms of the GNU General Public License as published by\nthe Free Software Foundation, either version 3 of the License, or\n(at your option) any later version.\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the\nGNU General Public License for more details.\nYou should have received a copy of the GNU General Public License\nalong with this program. If not, see <http://www.gnu.org/licenses/>.\n'
__author__ = 'dev'
import multiprocessing as multi, threading as trd, socket, org.py4grid.multicast.utils as mcast

class Talker:

    def __init__(self):
        self.listeners_rlock = multi.RLock()
        self.listeners = []

    def talk(self, arg):
        with self.listeners_rlock:
            for listener in self.listeners:
                listener.listen(arg)

    def register_listener(self, obj=None):
        if obj:
            with self.listeners_rlock:
                if obj not in self.listeners:
                    self.listeners.append(obj)


class Listener:

    def listen(self, arg):
        raise NotImplementedError


class ServerDaemon(trd.Thread, Talker):
    MHOST = mcast.MCAST_SERVERS
    MPORT = mcast.MCAST_SERVERS_PORT

    def __init__(self, onlylisten=False, port=4680):
        self.sock = mcast.getsocket(ServerDaemon.MHOST, ServerDaemon.MPORT)
        self.onlylisten = onlylisten
        self.port = port
        trd.Thread.__init__(self, daemon=True)
        Talker.__init__(self)

    def __del__(self):
        try:
            self.sock.stop()
        except:
            pass

    def StopDaemon(self):
        print('parando servidor discover...')
        self.sock.stop()
        self.sock = None
        print('servidor parado...')

    def run(self):
        try:
            for msg in self.sock:
                trd.Thread(target=ServerDaemon.process, args=(self, msg), daemon=True).start()

        except Exception as ex:
            raise

    def SendRequest(self):
        try:
            msg = mcast.Request()
            self.sock.send(msg)
        except Exception as ex:
            raise

    def ProcessRequest(self):
        if not self.onlylisten:
            hostname = socket.gethostname()
            ips = socket.gethostbyname_ex(hostname)[2]
            msg = mcast.Response(hostname=hostname, port=self.port, ips=ips)
            self.sock.send(msg)

    @staticmethod
    def process(daemon, msg):
        if isinstance(msg, mcast.Request):
            daemon.ProcessRequest()
        elif isinstance(msg, mcast.Response):
            if msg.hostname and msg.port:
                daemon.talk(msg)