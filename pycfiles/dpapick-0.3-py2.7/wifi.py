# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/DPAPI/Probes/wifi.py
# Compiled at: 2014-09-22 08:18:52
import datetime
from DPAPI.Core import eater
from DPAPI.Core import blob
from DPAPI import probe

class WirelessInfo(probe.DPAPIProbe):

    class WifiStruct(eater.DataStruct):

        def __init__(self, raw=None):
            self.bssid = None
            self.ssid = None
            eater.DataStruct.__init__(self, raw)
            return

        _networktype = ['Freq hopping', 'Direct Sequence', '802.11a', '802.11b/g']
        _networkinfra = ['Ad-hoc', 'Infrastructure', 'Automatic']
        _authmode = ['Open', 'Shared', 'AutoSwitch', 'WPA', 'WPA-PSK', 'WPA None', 'WPA2', 'WPA2-PSK']
        _wifichans = {2412000: 1, 
           2417000: 2, 
           2422000: 3, 
           2427000: 4, 
           2432000: 5, 
           2437000: 6, 
           2442000: 7, 
           2447000: 8, 
           2452000: 9, 
           2457000: 10, 
           2462000: 11, 
           2467000: 12, 
           2472000: 13, 
           2484000: 14, 
           5180000: 26, 
           5200000: 40, 
           5220000: 44, 
           5240000: 48, 
           5260000: 52, 
           5280000: 56, 
           5300000: 60, 
           5320000: 64, 
           5745000: 149, 
           5765000: 153, 
           5785000: 157, 
           5805000: 161}

        def __repr__(self):
            s = [
             'WifiStruct']
            flags = []
            if self.flags & 1:
                flags.append('WEP key present')
            if self.flags & 2:
                flags.append('WEP key in hex form')
            if self.flags & 4:
                flags.append('volatile')
            if self.flags & 8:
                flags.append('enforced by policy')
            if self.flags & 16:
                flags.append('802.1x should be enabled')
            s.append('        flags            = %s' % (', ').join(flags))
            s.append('        bssid            = %s' % self.bssid)
            s.append('        ssid             = %s' % self.ssid)
            s.append('        privacy          = 0x%x' % self.privacy)
            s.append('        rssi             = %i' % self.rssi)
            s.append('        network type     = %s' % self._networktype[self.nettype])
            s.append('        channel          = %s' % self._wifichans[self.configuration[3]])
            s.append('        infrastructure   = %s' % self._networkinfra[self.infrastructuremode])
            s.append('        rates            = %s' % repr(self.supportedrates))
            s.append('        key index        = %u' % self.keyindex)
            s.append('        key              = %s' % self.key.encode('hex'))
            s.append('        authentication   = %s' % self._authmode[self.authmode])
            s.append('        802.1x           = %r' % (self.ieee8021xEnabled != 0))
            s.append('        eap flags        = 0x%x' % self.eapflags)
            eap = '0x%s' % self.eaptype
            if self.eaptype == 19:
                eap = 'EAP-TLS'
            if self.eaptype == 38:
                eap = 'PEAP'
            s.append('        eap type         = %s' % eap)
            s.append('        wpa mcast cipher = 0x%x' % self.wpamcastcipher)
            s.append('        media type       = 0x%x' % self.mediatype)
            tmp = datetime.datetime.utcfromtimestamp(self.timestamp).ctime()
            s.append('        timestamp        = %s' % tmp)
            return ('\n').join(s)

        def parse(self, data):
            self.flags = data.eat('L')
            self.bssid = '%02x:%02x:%02x:%02x:%02x:%02x' % data.eat('6B')
            data.eat('2B')
            l = data.eat('L')
            self.ssid = data.eat('32s')
            self.ssid = self.ssid[:l]
            self.privacy = data.eat('L')
            self.rssi = data.eat('l')
            self.nettype = data.eat('L')
            self.configuration = data.eat('8L')
            self.infrastructuremode = data.eat('L')
            self.supportedrates = data.eat('8B')
            self.keyindex = data.eat('L')
            self.keylen = data.eat('L')
            self.key = data.eat('32s')
            self.key = self.key[:self.keylen]
            self.authmode = data.eat('L')
            data.eat('2L')
            self.ieee8021xEnabled = data.eat('L') != 0
            self.eapflags = data.eat('L')
            self.eaptype = data.eat('L')
            self.authdatalen = data.eat('L')
            self.authdata = data.eat('L')
            data.eat('2L')
            self.wpamcastcipher = data.eat('L')
            self.mediatype = data.eat('L')
            data.eat('500B')
            self.timestamp = data.eat('Q')
            if self.timestamp > 0:
                self.timestamp /= 10000000
                self.timestamp -= 11644473600

    def parse(self, data):
        l = data.eat('L') - 4
        self.wifiStruct = WirelessInfo.WifiStruct(data.eat('%us' % l))
        self.dpapiblob = blob.DPAPIBlob(data.remain())

    def postprocess(self, **k):
        xorKey = ('56660942080398014d67086611' * 5).decode('hex')
        if self.dpapiblob.decrypted:
            self.cleartext = ('').join([ chr(ord(x) ^ ord(y)) for x, y in zip(self.dpapiblob.cleartext, xorKey) ])
            self.cleartext = self.cleartext[:self.wifiStruct.keylen]

    def __repr__(self):
        s = ['Wirelesskey block']
        s.append('        BSSID      = %s' % self.wifiStruct.bssid)
        s.append('        SSID       = %s' % self.wifiStruct.ssid)
        if self.dpapiblob.decrypted:
            s.append('        hexKey     = %s' % self.cleartext.encode('hex'))
        s.append('    %r' % self.wifiStruct)
        s.append('    %r' % self.dpapiblob)
        return ('\n').join(s)