# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.4/lib/python3.4/site-packages/org/py4grid/multicast/daemons/DiscoverDaemons.py
# Compiled at: 2014-09-03 21:26:43
# Size of source mod 2**32: 3504 bytes
__doc__ = '\nPY4GRID : a little framework to simule multiprocessing over a lot of computers\nCopyright (C) 2014  João Jorge Pereira Farias Junior\nThis program is free software: you can redistribute it and/or modify\nit under the terms of the GNU General Public License as published by\nthe Free Software Foundation, either version 3 of the License, or\n(at your option) any later version.\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the\nGNU General Public License for more details.\nYou should have received a copy of the GNU General Public License\nalong with this program. If not, see <http://www.gnu.org/licenses/>.\n'
__author__ = 'dev'
import multiprocessing as multi, os, threading as trd, time, socket, org.py4grid.multicast.utils as mcast
from org.py4grid.multicast.daemons.DiscoverServers import Talker, Listener, ServerDaemon

def OnlineServer(adr):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        sock.connect(adr)
        sock.close()
        return True
    except Exception as ex:
        return False


class DiscoverDaemon(trd.Thread, Talker, Listener):
    MHOST = mcast.MCAST_DISCOVER
    MPORT = mcast.MCAST_DISCOVER_PORT

    def __init__(self, onlylisten=False):
        trd.Thread.__init__(self, daemon=True)
        Talker.__init__(self)
        self.onlylisten = onlylisten
        self.HostsRlock = multi.RLock()
        self.Hosts = []
        self.servers = ServerDaemon(onlylisten=True)
        self.servers.register_listener(self)
        self.servers.start()
        self.sock = mcast.getsocket(DiscoverDaemon.MHOST, DiscoverDaemon.MPORT)
        if not self.onlylisten:
            trd.Thread(target=DiscoverDaemon.discoverservers, args=(self,), daemon=True).start()

    def __del__(self):
        self.servers = None
        self.sock.stop()
        self.sock = None

    def listen(self, arg):
        with self.HostsRlock:
            hostname = arg.hostname
            hostip = socket.gethostbyname(hostname)
            adr = (hostip, arg.port)
            if adr not in self.Hosts:
                self.Hosts.append(adr)
                print('HOSTS UPDATE', self.Hosts)

    def gethosts(self):
        copy = []
        with self.HostsRlock:
            copy = self.Hosts[:]
        return copy

    def ProcessRequest(self):
        if not self.onlylisten:
            msg = mcast.Response()
            msg.pid = os.getpid()
            msg.ips = self.gethosts()
            self.sock.send(msg)

    @staticmethod
    def process(daemon, msg):
        if isinstance(msg, mcast.Request):
            daemon.ProcessRequest()
        elif isinstance(msg, mcast.Response):
            daemon.talk(msg)

    @staticmethod
    def discoverservers(daemon):
        while daemon.servers:
            daemon.servers.SendRequest()
            time.sleep(0.64)

    def sendrequest(self):
        try:
            msg = mcast.Request()
            self.sock.send(msg)
        except Exception as ex:
            raise

    def run(self):
        try:
            for msg in self.sock:
                trd.Thread(target=DiscoverDaemon.process, args=(self, msg), daemon=True).start()

        except Exception as ex:
            raise