# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/k3lib.py
# Compiled at: 2011-05-01 16:28:09
import string, serial, time, os
from lxml import etree
CONFIGFILE = '~/.rigcontrol/k3.xml'

class K3:

    def __init__(self):
        configfile = os.path.expanduser(CONFIGFILE)
        if not os.path.exists(configfile):
            raise 'Please create %s' % configfile
        config = etree.parse(configfile).getroot()
        assert config.tag == 'rig'
        device = config.findtext('port/device')
        baudrate = config.findtext('port/baud')
        init = config.findtext('init')
        self.ser = serial.Serial(device, baudrate=baudrate)
        self.write(init)
        self.ser.flushInput()
        self.ser.flushOutput()

    def close(self):
        self.ser.flushInput()
        self.ser.close()

    def write(self, str):
        self.ser.write(str)

    def read(self, n):
        return self.ser.read(n)

    def qsy(self, freq):
        if freq < 10000000.0:
            cmd = 'FA0000%d;' % freq
        else:
            cmd = 'FA000%d;' % freq
        self.write(cmd)
        return self.qsyq()

    def qsy2(self, freq):
        if freq < 10000000.0:
            cmd = 'FB0000%d;' % freq
        else:
            cmd = 'FB000%d;' % freq
        self.write(cmd)
        return self.qsyq()

    def qsyq(self):
        self.write('FA;')
        result = self.read(14)
        if len(result) != 14:
            return 0
        return float(result[2:10] + '.' + result[10:13])

    def qsyq2(self):
        self.write('FB;')
        result = self.read(14)
        if len(result) != 14:
            return 0
        return float(result[2:10] + '.' + result[10:13])

    def fiq(self):
        self.write('FI;')
        result = self.read(7)
        if len(result) != 7:
            return 0
        return float('821' + result[2:3] + '.' + result[3:6])

    def nb(self, level, thresh):
        self.write('NB%s;' % level)

    def nbq(self):
        self.write('NB;')
        result = self.read(5)
        if len(result) != 5:
            return 0
        level = result[2]
        thresh = result[3]
        return 'NB: %c %c' % (level, thresh)

    def mode(self, str):
        if str == 'lsb' or str == 'l':
            modenum = 1
        if str == 'usb' or str == 'u':
            modenum = 2
        if str == 'cw' or str == 'c':
            modenum = 3
        if str == 'cwr':
            modenum = 5
        if str == 'rtty' or str == 'r':
            modenum = 6
        if str == 'rttyr':
            modenum = 9
        cmd = 'MD%d;' % modenum
        self.write(cmd)
        return self.modeq()

    def modeq(self):
        self.write('K22;MD;')
        result = self.read(4)
        if len(result) != 4:
            return '???: ' + result
        modenum = string.atoi(result[2])
        if modenum == 1:
            return 'lsb'
        if modenum == 2:
            return 'usb'
        if modenum == 3:
            return 'cw'
        if modenum == 5:
            return 'cwr'
        if modenum == 6:
            return 'rtty'
        if modenum == 9:
            return 'rttyr'
        return '???'

    def pa(self, str):
        if str == 'off':
            modenum = 0
        if str == 'on':
            modenum = 1
        cmd = 'PA%d;' % modenum
        self.write(cmd)
        return self.paq()

    def paq(self):
        self.write('PA;')
        result = self.read(4)
        if len(result) != 4:
            return 0
        else:
            if result == 'PA1;':
                return 'on'
            return 'off'

    def power(self, watts):
        cmd = 'PC%03d;' % watts
        self.write(cmd)
        return self.powerq()

    def powerq(self):
        self.write('PC;')
        result = self.read(6)
        if len(result) != 6:
            return 0
        return int(result[2:5])

    def vfoa(self):
        self.write('FT0;FR0;')
        return self.vfoq()

    def vfob(self):
        self.write('FT1;FR1;')
        return self.vfoq()

    def vfoq(self):
        self.write('FT;FR;')
        result = self.read(8)
        if len(result) != 8:
            return 0
        return 'TX: %c; RX: %c' % (65 + string.atoi(result[2]), 65 + string.atoi(result[6]))

    def sendcw(self, str):
        cmd = 'KY %s;' % str
        self.write(cmd)

    def cwspeedq(self):
        cmd = 'K0;'
        self.write(cmd)
        result = self.read(2)
        if len(result) != 5:
            return 0
        return result[1:3]

    def cwspeed(self, speed):
        cmd = 'K%3d;'
        self.write(cmd)
        return self.cwspeedq()

    def ra(self, offon):
        if offon == 'off':
            offon = 0
        elif offon == 'on':
            offon = 1
        self.write('RA0%s;' % offon)
        return self.raq()

    def raq(self):
        self.write('RA;')
        result = self.read(5)
        if len(result) != 5:
            return 0
        offon = result[3]
        return 'RA: %s' % ['off', 'on'][(ord(offon) - ord('0'))]

    def filter(self, n):
        cmd = 'FW0000%d;' % n
        self.write(cmd)

    def filtern(self):
        self.write('FW;')
        result = self.read(9)
        if len(result) != 9:
            return 0
        return string.atoi(result[6])

    def filterq(self):
        self.write('FW;')
        result = self.read(9)
        if len(result) != 9:
            return 0
        return result[2:6] + 'Hz ' + result[7]

    def displayq(self):
        self.write('DS;')
        result = self.read(13)
        if len(result) != 13:
            return 0
        return result

    def verq(self, x):
        self.write('RV%c;' % x)
        result = self.read(9)
        if len(result) != 9:
            return 0
        else:
            ver = result[3:8]
            if ver == '99.99':
                ver = None
            return ver

    def showtext(self, text):
        for letter in text:
            self.write('DB%s;' % letter)

    def timeq(self):

        def k3LcdChar(c):
            if ord(c) > 127:
                return ':' + chr(ord(c) & 127)
            else:
                return c

        self.write('K31;MN073;')
        time.sleep(0.05)
        self.write('DS;')
        result = self.read(13)
        self.write('MN255;')
        if len(result) != 13:
            return None
        else:
            return ('').join([ k3LcdChar(c) for c in result[4:10] ])

    def fixtime(self):

        def k3LcdChar(c):
            return chr(ord(c) & 127)

        self.write('K31;MN073;')
        time.sleep(0.05)
        self.write('DS;')
        time.sleep(0.05)
        result = self.read(13)
        if len(result) != 13:
            self.write('MN255;')
            return None
        else:
            k3hour = int(('').join([ k3LcdChar(c) for c in result[4:6] ]))
            k3minute = int(('').join([ k3LcdChar(c) for c in result[6:8] ]))
            k3second = int(('').join([ k3LcdChar(c) for c in result[8:10] ]))
            year, month, day, hour, minute, second, x, y, z = time.gmtime()
            self.write('SWT13;')
            time.sleep(0.05)
            while k3second < second:
                self.write('UP;')
                k3second = k3second + 1

            while k3second > second:
                self.write('DN;')
                k3second = k3second - 1

            self.write('SWT12;')
            time.sleep(0.05)
            while k3minute < minute:
                self.write('UP;')
                k3minute = k3minute + 1

            while k3minute > minute:
                self.write('DN;')
                k3minute = k3minute - 1

            self.write('SWT11;')
            time.sleep(0.05)
            while k3hour < hour:
                self.write('UP;')
                k3hour = k3hour + 1

            while k3hour > hour:
                self.write('DN;')
                k3hour = k3hour - 1

            self.write('MN255;')
            return self.timeq()