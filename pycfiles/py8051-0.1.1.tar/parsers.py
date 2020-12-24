# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/py80211/parsers.py
# Compiled at: 2012-12-06 20:22:00
import pcap, sys, struct

class InformationElements(object):
    """
    Parsing 802.11 frame information elements
    """

    def __init__(self):
        """
        build parser for IE tags
        """
        self.tagdata = {'unparsed': []}
        self.parser = {'\x00': self.ssid, 
           '\x01': self.rates, 
           '\x03': self.channel, 
           '0': self.rsn, 
           '2': self.exrates}

    def parseIE(self, rbytes):
        """
        takes string of raw bytes splits them into tags
        passes those tags to the correct parser
        retruns parsed tags as a dict, key is tag number
        rbytes = string of bytes to parse
        """
        self.tagdata = {'unparsed': []}
        while len(rbytes) > 0:
            try:
                fbyte = rbytes[0]
                blen = ord(rbytes[1]) + 2
                if fbyte in self.parser.keys():
                    prebytes = rbytes[0:blen]
                    if blen == len(prebytes):
                        self.parser[fbyte](prebytes)
                    else:
                        return -1
                else:
                    self.tagdata['unparsed'].append(rbytes[0:blen])
                rbytes = rbytes[blen:]
            except IndexError:
                return -1

    def exrates(self, rbytes):
        """
        parses extended supported rates
        exrates IE tag number is 0x32
        retruns exrates in a list
        """
        exrates = []
        for exrate in tuple(rbytes[2:]):
            exrates.append(ord(exrate))

        self.tagdata['exrates'] = exrates

    def channel(self, rbytes):
        """
        parses channel
        channel IE tag number is 0x03
        returns channel as int
        last byte is channel
        """
        self.tagdata['channel'] = ord(rbytes[2])

    def ssid(self, rbytes):
        """
        parses ssid IE tag
        ssid IE tag number is 0x00
        returns the ssid as a string
        """
        self.tagdata['ssid'] = unicode(rbytes[2:], errors='replace')

    def rates(self, rbytes):
        """
        parses rates from ie tag
        rates IE tag number is 0x01
        returns rates as in a list
        """
        rates = []
        for rate in tuple(rbytes[2:]):
            rates.append(ord(rate))

        self.tagdata['rates'] = rates

    def rsn(self, rbytes):
        """
        parses robust security network ie tag
        rsn ie tag number is 0x30
        returns rsn info in nested dict
        gtkcs is group temportal cipher suite
        akm is auth key managment, ie either wpa, psk ....
        ptkcs is pairwise temportal cipher suite
        """
        rsn = {}
        ptkcs = []
        akm = []
        cipherS = {1: 'WEP-40/64', 
           2: 'TKIP', 
           3: 'RESERVED', 
           4: 'CCMP', 
           5: 'WEP-104/128'}
        authKey = {1: '802.1x or PMK', 
           2: 'PSK'}
        try:
            version = struct.unpack('h', rbytes[2:4])[0]
            rsn['gtkcsOUI'] = rbytes[4:7]
            gtkcsTypeI = ord(rbytes[7])
            if gtkcsTypeI in cipherS.keys():
                gtkcsType = cipherS[gtkcsTypeI]
            else:
                gtkcsType = gtkcsTypeI
            rsn['gtkcsType'] = gtkcsType
            ptkcsTypeL = struct.unpack('h', rbytes[8:10])[0]
            counter = ptkcsTypeL
            cbyte = 10
            while counter >= ptkcsTypeL:
                ptkcsTypeOUI = rbytes[cbyte:cbyte + 3]
                ptkcsTypeI = ord(rbytes[(cbyte + 3)])
                if ptkcsTypeI in cipherS.keys():
                    ptkcsType = cipherS[ptkcsTypeI]
                else:
                    ptkcsType = ptkcsTypeI
                cbyte += 4
                ptkcs.append({'ptkcsOUI': ptkcsTypeOUI, 'ptkcsType': ptkcsType})
                counter -= 1

            akmTypeL = struct.unpack('h', rbytes[cbyte:cbyte + 2])[0]
            cbyte += 2
            counter = akmTypeL
            while counter >= akmTypeL:
                akmTypeOUI = rbytes[cbyte:cbyte + 3]
                akmTypeI = ord(rbytes[(cbyte + 3)])
                if akmTypeI in authKey.keys():
                    akmType = authKey[akmTypeI]
                else:
                    akmType = akmTypeI
                cbyte += 4
                akm.append({'akmOUI': akmTypeOUI, 'akmType': akmType})
                counter -= 1

            capabil = rbytes[cbyte:cbyte + 2]
            cbyte += 3
            rsn['pmkidcount'] = rbytes[cbyte:cbyte + 2]
            rsn['pmkidlist'] = rbytes[cbyte + 3:]
            rsn['ptkcs'] = ptkcs
            rsn['akm'] = akm
            rsn['capabil'] = capabil
            self.tagdata['rsn'] = rsn
        except IndexError:
            return -1


class Common(object):
    """
    Class file for parsing
    several common 802.11 frames
    """

    def __init__(self, dev):
        """
        open up the libpcap interface
        open up the device to sniff from
        dev = device name as a string
        """
        self.mangled = False
        self.mangledcount = 0
        self.IE = InformationElements()
        self.parser = {0: {0: self.placedef, 
               1: self.placedef, 
               2: self.placedef, 
               3: self.placedef, 
               4: self.probeReq, 
               5: self.probeResp, 
               8: self.beacon, 
               9: self.placedef, 
               10: self.placedef, 
               11: self.placedef, 
               12: self.placedef}, 
           1: {}, 2: {0: self.data, 
               1: self.data, 
               2: self.data, 
               3: self.data, 
               5: self.data, 
               6: self.data, 
               7: self.data, 
               8: self.data, 
               9: self.data, 
               10: self.data, 
               11: self.data, 
               12: self.data, 
               14: self.data, 
               15: self.data}}
        self.packetBcast = {'oldbcast': '\x00\x00\x00\x00\x00\x00', 
           'l2': b'\xff\xff\xff\xff\xff\xff', 
           'ipv6m': '33\x00\x00\x00\x16', 
           'stp': b'\x01\x80\xc2\x00\x00\x00', 
           'cdp': b'\x01\x00\x0c\xcc\xcc\xcc', 
           'cstp': b'\x01\x00\x0c\xcc\xcc\xcd', 
           'stpp': b'\x01\x80\xc2\x00\x00\x08', 
           'oam': b'\x01\x80\xc2\x00\x00\x02', 
           'ipv4m': b'\x01\x00^\x00\x00\xcd', 
           'ota': b'\x01\x0b\x85\x00\x00\x00'}
        self.openSniff(dev)

    def openSniff(self, dev):
        """
        open up a libpcap object
        return object and radio tap boolen
        """
        packet = None
        self.lp = pcap.pcapObject()
        snap_lenght = 1600
        promisc_flag = 0
        timeout = 100
        self.lp.open_live(dev, snap_lenght, promisc_flag, timeout)
        if self.lp.datalink() == 127:
            self.rth = True
            while packet is None:
                frame = self.getFrame()
                if frame is not None:
                    packet = frame[1]

            self.headsize = struct.unpack('h', packet[2:4])[0]
        else:
            self.rth = False
        return

    def isBcast(self, mac):
        """
        returns boolen if mac is a broadcast/multicast mac
        """
        if mac in self.packetBcast.values():
            return True
        else:
            if mac[:2] == self.packetBcast['ipv6m'][:2]:
                return True
            return False

    def placedef(self, data):
        pass

    def getFrame(self):
        """
        return a frame from libpcap
        """
        return self.lp.next()

    def parseFrame(self, frame):
        """
        Determine the type of frame and
        choose the right parser
        """
        if frame is not None:
            data = frame[1]
            if data is None:
                return
            if self.rth:
                self.rt = struct.unpack('h', data[2:4])[0]
                if self.rt != self.headsize:
                    self.rt = 0
            else:
                self.rt = 0
        else:
            return
        ptype = ord(data[self.rt])
        ftype = ptype >> 2 & 3
        stype = ptype >> 4
        if ftype in self.parser.keys():
            if stype in self.parser[ftype].keys():
                parsedFrame = self.parser[ftype][stype](data[self.rt:])
                if parsedFrame in (None, -1):
                    return parsedFrame
                parsedFrame['type'] = ftype
                parsedFrame['stype'] = stype
                parsedFrame['rtap'] = self.rt
                parsedFrame['raw'] = data
                return parsedFrame
            else:
                return

        else:
            return
        return

    def data(self, data):
        """
        parse the src,dst,bssid from a data frame
        """
        try:
            dsbits = ord(data[1]) & 3
            if dsbits == 1:
                bssid = data[4:10]
                src = data[10:16]
                dst = data[16:22]
            elif dsbits == 2:
                dst = data[4:10]
                bssid = data[10:16]
                src = data[16:22]
            else:
                if dsbits == 3:
                    return None
                else:
                    self.mangled = True
                    self.mangledcount += 1
                    return -1

        except IndexError:
            self.mangled = True
            self.mangledcount += 1
            return -1

        return {'src': src, 'dst': dst, 'bssid': bssid, 'ds': dsbits}

    def probeResp(self, data):
        """
        Parse out probe response
        return a dict of with keys of
        src, dst, bssid, probe request
        """
        try:
            dsbits = ord(data[1]) & 3
            dst = data[4:10]
            src = data[10:16]
            bssid = data[16:22]
            self.IE.parseIE(data[36:])
            if 'ssid' not in self.IE.tagdata.keys():
                self.mangled = True
                self.mangledcount += 1
                return -1
            essid = self.IE.tagdata['ssid']
            if 'channel' not in self.IE.tagdata.keys():
                self.mangled = True
                self.mangledcount += 1
                return -1
            channel = self.IE.tagdata['channel']
        except IndexError:
            self.mangled = True
            self.mangledcount += 1
            return -1

        return {'bssid': bssid, 'essid': essid, 'src': src, 'dst': dst, 
           'channel': channel, 'extended': self.IE.tagdata, 'ds': dsbits}

    def probeReq(self, data):
        """
        Parse out probe requests
        return a dict of with keys of
        src, dst, bssid, probe request
        """
        try:
            dsbits = ord(data[1]) & 3
            dst = data[4:10]
            src = data[10:16]
            bssid = data[16:22]
            self.IE.parseIE(data[24:])
            if 'ssid' not in self.IE.tagdata.keys():
                self.mangled = True
                self.mangledcount += 1
                return -1
            essid = self.IE.tagdata['ssid']
            if 'channel' not in self.IE.tagdata.keys():
                self.mangled = True
                self.mangledcount += 1
                return -1
            channel = self.IE.tagdata['channel']
        except IndexError:
            self.mangled = True
            self.mangledcount += 1
            return -1

        return {'bssid': bssid, 'essid': essid, 'src': src, 'dst': dst, 
           'channel': channel, 'extended': self.IE.tagdata, 'ds': dsbits}

    def beacon(self, data):
        """
        Parse out beacon packets
        return a dict with the keys of
        src, dst, bssid, essid, channel ....
        going to need to add more
        """
        try:
            dsbits = ord(data[1]) & 3
            dst = data[4:10]
            src = data[10:16]
            bssid = data[16:22]
            self.IE.parseIE(data[36:])
            if 'ssid' not in self.IE.tagdata.keys():
                self.mangled = True
                self.mangledcount += 1
                return -1
            essid = self.IE.tagdata['ssid']
            if 'channel' not in self.IE.tagdata.keys():
                self.mangled = True
                self.mangledcount += 1
                return -1
            channel = self.IE.tagdata['channel']
        except IndexError:
            self.mangled = True
            self.mangledcount += 1
            return -1

        return {'bssid': bssid, 'essid': essid, 'src': src, 'dst': dst, 'channel': channel, 
           'extended': self.IE.tagdata, 'ds': dsbits}


if __name__ == '__main__':
    x = Common(sys.argv[1])
    while True:
        frame = x.parseFrame(x.getFrame())
        print x.parseFrame(x.getFrame())