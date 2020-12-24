# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/steppirlib.py
# Compiled at: 2015-02-21 17:08:34
import string, serial, sys, os
from lxml import etree
from time import sleep
CONFIGFILE = '~/.rigcontrol/steppir.xml'

class Bits:
    DVR_MASK = 4
    REFL_MASK = 16
    DIR1_MASK = 8
    DIR2_MASK = 32
    S1 = 64
    S2 = 65
    S3 = 0
    S7_AC = 0
    S8_DIR_NORM = 0
    S8_DIR_REV = 64
    S8_DIR_BIDI = 128
    S8_DIR_THREE_QUARTER_VERTICAL = 32
    S8_DIR_ALL = S8_DIR_NORM | S8_DIR_REV | S8_DIR_BIDI | S8_DIR_THREE_QUARTER_VERTICAL
    S9_CMD_SET_FREQ_AND_DIR = '1'
    S9_CMD_REENABLE_FREQ_UPDATE = 'R'
    S9_CMD_HOME = 'S'
    S9_CMD_DISABLE_FREQUENCY_UPDATE = 'U'
    S9_CMD_CALIBRATE = 'V'
    S10_VERSION = '0'
    S11 = 13


class Steppir:

    def __init__(self):
        configfile = os.path.expanduser(CONFIGFILE)
        if not os.path.exists(configfile):
            raise 'Please create %s' % configfile
        self.config = etree.parse(os.path.expanduser(configfile)).getroot()
        assert self.config.tag == 'steppir'
        self.device = self.config.findtext('port/device')
        self.baudrate = int(self.config.findtext('port/baud'))
        self.elts = int(self.config.findtext('elements'))
        self.serio = None
        return

    def open(self):
        self.serio = serial.Serial(self.device, self.baudrate)
        self.serio.setDTR(level=True)
        self.serio.setRTS(level=True)

    def close(self):
        if self.serio != None:
            self.serio.close()
        return

    def setfreqdir(self, freq, dir_bits):
        self.output(Bits.S1)
        self.output(Bits.S2)
        self.output(Bits.S3)
        Fh = freq / 65536
        Fm = freq % 65536 / 256 & 255
        Fl = freq % 256 & 255
        self.output(Fh)
        self.output(Fm)
        self.output(Fl)
        self.output(Bits.S7_AC)
        self.output(dir_bits)
        self.output(Bits.S9_CMD_SET_FREQ_AND_DIR)
        self.output(Bits.S10_VERSION)
        self.output(Bits.S11)
        sleep(0.5)

    def home(self):
        self.output(Bits.S1)
        self.output(Bits.S2)
        self.output(Bits.S3)
        Fh = 0
        Fm = 0
        Fl = 0
        self.output(Fh)
        self.output(Fm)
        self.output(Fl)
        self.output(Bits.S7_AC)
        self.output(0)
        self.output(Bits.S9_CMD_HOME)
        self.output(Bits.S10_VERSION)
        self.output(Bits.S11)

    def output(self, c):
        self.serio.write('%c' % c)
        self.serio.flush()

    def input(self):
        c = self.serio.read(1)
        c = ord(c)
        return c

    def status(self):
        self.output('?')
        self.output('A')
        self.output(13)

    def readin(self):
        c = self.input()
        c = self.input()
        c = self.input()
        c = self.input()
        frequency = c * 256 * 256
        c = self.input()
        frequency += c * 256
        c = self.input()
        frequency += c
        frequency = frequency / 100
        c = self.input()
        ac_bits = c
        c = self.input()
        current_dir_bits = c & Bits.S8_DIR_ALL
        c = self.input()
        c = self.input()
        c = self.input()
        dir = self.formatDir(current_dir_bits)
        return (frequency, dir, self.formatElts(ac_bits))

    def formatElts(self, ac_bits):
        if self.elts == 4:
            return '(%c-%c-%c-%c)' % (self.formatElt(ac_bits, Bits.DIR2_MASK), self.formatElt(ac_bits, Bits.DIR1_MASK), self.formatElt(ac_bits, Bits.DVR_MASK), self.formatElt(ac_bits, Bits.REFL_MASK))
        if self.elts == 3:
            return '(%c-%c-%c)' % (self.formatElt(ac_bits, Bits.DIR1_MASK), self.formatElt(ac_bits, Bits.DVR_MASK), self.formatElt(ac_bits, Bits.REFL_MASK))
        if self.elts == 2:
            return '(%c-%c)' % (self.formatElt(ac_bits, Bits.REFL_MASK), self.formatElt(ac_bits, Bits.DVR_MASK))
        if self.elts == 1:
            return '(%c)' % self.formatElt(ac_bits, Bits.DVR_MASK)

    def formatElt(self, bits, mask):
        if bits & mask == 0:
            return '|'
        else:
            return '+'

    def formatDir(self, bits):
        if bits == Bits.S8_DIR_NORM:
            return 'N'
        else:
            if bits == Bits.S8_DIR_REV:
                return 'R'
            else:
                if bits == Bits.S8_DIR_BIDI:
                    return 'B'
                if bits == Bits.S8_DIR_THREE_QUARTER_VERTICAL:
                    return 'V'
                return

            return

    def parseFrequency(self, s, frequency):
        if s == 'home':
            return
        else:
            if s == '.':
                return frequency
            else:
                return 100 * int(s)

            return

    def parseDir(self, s, dir):
        s = string.upper(s)
        if s == '.':
            return dir
        else:
            if s == 'N':
                return Bits.S8_DIR_NORM
            if s == 'R':
                return Bits.S8_DIR_REV
            if s == 'B':
                return Bits.S8_DIR_BIDI
            if s == 'V':
                return Bits.S8_DIR_THREE_QUARTER_VERTICAL
            return s