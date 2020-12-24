# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/py80211/tools.py
# Compiled at: 2012-12-07 03:05:18
import threading, time, sys, os, fcntl, struct
from py80211 import parsers
import PyLorcon2

class Interface(object):
    """
    handle 80211 interfacs
    """

    def __init__(self):
        self.tun = ''
        self.moniface = ''
        self.TUNSETIFF = 1074025674
        self.TUNSETOWNER = self.TUNSETIFF + 2
        self.IFF_TUN = 1
        self.IFF_TAP = 2
        self.IFF_NO_PI = 4096

    def check_tun(self, path):
        """
        check for tuntap support
        """
        return True

    def open_tun(self):
        """
        open up a tuntap interface
        path is /dev/net/tun in TAP (ether) mode
        returns false if failed
        """
        path = '/dev/net/tun'
        if self.check_tun(path) is not False:
            self.tun = os.open(path, os.O_RDWR)
            ifr = struct.pack('16sH', 'tun%d', self.IFF_TAP | self.IFF_NO_PI)
            ifs = fcntl.ioctl(self.tun, self.TUNSETIFF, ifr)
            ifname = ifs[:16].strip('\x00')
            print 'Interface %s created. Configure it and use it' % ifname
            os.system('ifconfig %s up' % ifname)
            return ifname
        else:
            return False

    def inject(self, packet):
        """
        send bytes to pylorcon interface
        """
        if self.moniface is not None:
            self.moniface['ctx'].send_bytes(packet)
        return

    def readTun(self):
        """
        read a packet from tun interface
        """
        return os.read(self.tun, 1526)

    def writeTun(self, packet):
        """
        write a packet to tun interface
        """
        os.write(self.tun, packet)

    def monitor(self, interface):
        """
        open a monitor mode interface and create a vap
        interface = string
        currently assumes all cards are to be opened in monitor mode
        """
        try:
            self.moniface = {'ctx': PyLorcon2.Context(interface)}
        except PyLorcon2.Lorcon2Exception as exception:
            print '%s is the %s interface there?' % (exception, interface)
            sys.exit(-1)

        self.moniface['ctx'].open_injmon()
        self.moniface['name'] = self.moniface['ctx'].get_vap()

    @property
    def monitor_interface(self):
        """
        retruns mon interface object
        """
        return self.moniface

    def exit(self):
        """
        Close card context
        """
        self.moniface['ctx'].close()


class ChannelHop(threading.Thread):
    """
    Control a card and cause it to hop channels
    Only one card per instance
    """

    def __init__(self, interface, channels=False):
        """
        set the channel hopping sequence
        expects lorcon injmon() context
        """
        self.lock = 0
        threading.Thread.__init__(self)
        threading.Thread.daemon = True
        self.iface = interface
        self.pause = False
        self.channellist = channels
        self.hopList = []
        self.current = 0
        self.checkChannels()

    def checkChannels(self):
        """
        card drivesr suck, determine what channels
        a card supports before we start hopping
        """
        for ch in self.channellist:
            try:
                self.iface.set_channel(ch)
            except PyLorcon2.Lorcon2Exception:
                continue

            self.hopList.append(ch)

    def pause(self):
        """
        Pause the channel hopping
        """
        self.pause = True

    def unpause(self):
        """
        Unpause the channel hopping
        """
        self.pause = False

    def setchannel(self, channel):
        """
        Set a single channel
        expects channel to be an int
        returns -1 if channel isnt supported
        #should raise an exception if this is the case
        """
        while self.lock == 1:
            print '!!!!!!!!!!!!!!Waiting for lock...!!!!!!!!!!!!'
            time.sleep(2)

        if channel in self.hopList:
            self.iface.set_channel(channel)
            return 0
        else:
            return -1

    def hop(self, dwell=0.4):
        """
        Hop channels
        """
        while True:
            if self.pause == True | self.lock == 1:
                continue
            for ch in self.hopList:
                try:
                    self.iface.set_channel(ch)
                except PyLorcon2.Lorcon2Exception:
                    continue

                self.current = ch
                if ch in (1, 6, 11):
                    time.sleep(dwell)
                else:
                    time.sleep(0.2)

    def run(self):
        """
        start the channel hopper
        """
        self.hop()


class Airview(threading.Thread):
    """
        Grab a snapshot of the air
        whos connected to who
        whats looking for what
        # note right now expecting to deal with only one card
        # will need to refactor code to deal with more then one in the future
        # dong this for time right now
    """

    def __init__(self, interface_, mon=False, channels=[
 1, 6, 11, 14, 2, 7, 3, 8, 4, 9, 5, 10,
 36, 40, 44, 48, 52, 56, 60, 64, 149, 153, 157, 161, 165]):
        """
            Open up a packet parser for a given interface and create monitor mode interface
            Thread the instance
            interface = interface as string
            if mon = True then interface = to the dicitionary object from the interface
        """
        self.channels = channels
        self.stop = False
        self.hopper = ''
        threading.Thread.__init__(self)
        threading.Thread.daemon = True
        if not mon:
            self.interface = Interface()
            self.interface.monitor(interface_)
            monif = self.interface.monitor_interface
        else:
            monif = interface_
        self.iface = monif['name']
        self.ctx = monif['ctx']
        self.rd = parsers.Common(self.iface)
        self.bss = {}
        self.apData = {}
        self.ess = {}
        self.clientProbes = {}
        self.client_list = ClientList(self.iface)
        self.view = {}
        self.vSSID = {}
        self.capr = {}

    @staticmethod
    def pformatMac(hexbytes):
        """
        Take in hex bytes and pretty format them
        to the screen in the xx:xx:xx:xx:xx:xx format
        """
        mac = []
        for byte in hexbytes:
            mac.append(byte.encode('hex'))

        return (':').join(mac)

    def verifySSID(self, bssid, uessid):
        """
        its possible to get a mangled ssid
        this allows us to check last 5 seen
        to see if they are mangled or its been changed
        bssid = bssid in hex of ap in question
        uessid = essid in hex to verify
        if all 5 dont match return False, else return True
        """
        for essid in self.vSSID[bssid]:
            if uessid != essid:
                self.vSSID[bssid] = []
                return False

        return True

    @property
    def clients(self):
        return self.client_list.clients

    @property
    def clients_extra(self):
        return self.client_list.clients_extra

    def parse(self):
        """
        Grab a packet, call the parser then update
        The airview state vars
        """
        while self.stop is False:
            self.hopper.lock = 1
            self.channel = self.hopper.current
            frame = self.rd.parseFrame(self.rd.getFrame())
            self.hopper.lock = 0
            if frame == None:
                continue
            if frame == -1:
                continue
            if frame['type'] == 0 and frame['stype'] == 8:
                bssid = frame['bssid']
                essid = frame['essid']
                self.bss[bssid] = essid
                if essid in self.ess.keys():
                    self.ess[essid].append(bssid)
                else:
                    self.ess[essid] = [
                     bssid]
                self.apData[bssid] = frame
                if bssid in self.vSSID.keys():
                    ssidList = self.vSSID[bssid]
                    if len(ssidList) > 3:
                        ssidList.pop(0)
                        ssidList.append(essid)
                        self.vSSID[bssid] = ssidList
                    else:
                        self.vSSID[bssid].append(essid)
                else:
                    self.vSSID[bssid] = [
                     essid]
                continue
            elif frame['type'] == 2 and frame['stype'] in range(0, 16):
                self.client_list.add(frame)
            if frame['type'] == 0 and frame['stype'] in (4, ):
                self.client_list.add(frame)
                src = frame['src']
                essid = frame['essid']
                if frame['src'] in self.clientProbes.keys():
                    if essid != '':
                        self.clientProbes[src][essid] = ''
                elif essid != '':
                    self.clientProbes[src] = {essid: ''}
            self.getCapr()

        return

    def getCapr(self, wiredc=False):
        """
        Parse clients list to build current list
        of bssids and their clients
        set wiredc to True to include wired devices discovered by broadcast
        """
        for client in self.clients.keys():
            if wiredc is False:
                if client in self.clients_extra.keys():
                    if self.clients_extra[client]['wired'] is False:
                        continue
            bssid = self.clients[client]
            if bssid != 'Not Associated':
                if bssid not in self.capr.keys():
                    self.capr[bssid] = [
                     client]
                elif client not in self.capr[bssid]:
                    self.capr[bssid].append(client)

    def getProbes(self, cmac):
        """
        return a list of probe requests
        for a given client
        """
        if cmac in self.clientProbes.keys():
            return self.clientProbes[cmac].keys()
        else:
            return
            return

    def run(self):
        """
        start the parser
        """
        self.hopper = ChannelHop(self.ctx, self.channels)
        self.hopper.start()
        self.parse()

    def kill(self):
        """
        stop the parser
        """
        self.stop = True
        self.interface.exit()


class ClientList(object):

    def __init__(self, iface):
        self.clients = {}
        self.clients_extra = {}
        self.rd = parsers.Common(iface)

    def add(self, frame):
        """
            Update self.clients var based on ds bits
        """
        bssid = frame['bssid']
        src = frame['src']
        dst = frame['dst']
        ds = frame['ds']
        if ds == 0:
            self.clients[src] = 'Not Associated'
            if src in self.clients_extra.keys():
                self.clients_extra[src]['wired'] = False
            else:
                self.clients_extra[src] = {'wired': False}
        else:
            if ds == 1:
                self.clients[src] = bssid
                if src in self.clients_extra.keys():
                    self.clients_extra[src]['wired'] = False
                else:
                    self.clients_extra[src] = {'wired': False}
                return
            if ds == 2:
                if self.rd.isBcast(dst) is True:
                    self.clients[src] = bssid
                    if src in self.clients_extra.keys():
                        if self.clients_extra[src]['wired'] is not False:
                            self.clients_extra[src]['wired'] = True
                    else:
                        self.clients_extra[src] = {'wired': True}
                elif self.rd.isBcast(dst) is True:
                    self.clients[src] = bssid
                    if src in self.clients_extra.keys():
                        if self.clients_extra[src]['wired'] is not False:
                            self.clients_extra[src]['wired'] = True
                    else:
                        self.clients_extra[src] = {'wired': True}
                else:
                    self.clients[dst] = bssid
                    if src in self.clients_extra.keys():
                        self.clients_extra[src]['wired'] = False
                    else:
                        self.clients_extra[src] = {'wired': False}
                return
            if ds == 3:
                return
            return