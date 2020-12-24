# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/serialXfer/XMODEM.py
# Compiled at: 2013-03-27 08:39:35
"""
===============================
XMODEM file transfer protocol
===============================

.. $Id$

This is a literal implementation of XMODEM.TXT_, XMODEM1K.TXT_ and
XMODMCRC.TXT_, support for YMODEM and ZMODEM is pending. YMODEM should
be fairly easy to implement as it is a hack on top of the XMODEM
protocol using sequence bytes ``0x00`` for sending file names (and some
meta data).

.. _XMODEM.TXT: doc/XMODEM.TXT
.. _XMODEM1K.TXT: doc/XMODEM1K.TXT
.. _XMODMCRC.TXT: doc/XMODMCRC.TXT

Data flow example including error recovery
==========================================

Here is a sample of the data flow, sending a 3-block message.
It includes the two most common line hits - a garbaged block,
and an ``ACK`` reply getting garbaged. ``CRC`` or ``CSUM`` represents
the checksum bytes.

XMODEM 128 byte blocks
----------------------

::

SENDER                                      RECEIVER

<-- NAK
SOH 01 FE Data[128] CSUM                -->
<-- ACK
SOH 02 FD Data[128] CSUM                -->
<-- ACK
SOH 03 FC Data[128] CSUM                -->
<-- ACK
SOH 04 FB Data[128] CSUM                -->
<-- ACK
SOH 05 FA Data[100] CPMEOF[28] CSUM     -->
<-- ACK
EOT                                     -->
<-- ACK

XMODEM-1k blocks, CRC mode
--------------------------

::

SENDER                                      RECEIVER

<-- C
STX 01 FE Data[1024] CRC CRC            -->
<-- ACK
STX 02 FD Data[1024] CRC CRC            -->
<-- ACK
STX 03 FC Data[1000] CPMEOF[24] CRC CRC -->
<-- ACK
EOT                                     -->
<-- ACK

Mixed 1024 and 128 byte Blocks
------------------------------

::

SENDER                                      RECEIVER

<-- C
STX 01 FE Data[1024] CRC CRC            -->
<-- ACK
STX 02 FD Data[1024] CRC CRC            -->
<-- ACK
SOH 03 FC Data[128] CRC CRC             -->
<-- ACK
SOH 04 FB Data[100] CPMEOF[28] CRC CRC  -->
<-- ACK
EOT                                     -->
<-- ACK

"""
__author__ = 'Wijnand Modderman <maze@pyth0n.org>'
__copyright__ = ['Copyright (c) 2010 Wijnand Modderman',
 'Copyright (c) 1981 Chuck Forsberg']
__license__ = 'MIT'
__version__ = '0.2.4'
import logging, time, sys, threading
SOH = chr(1)
STX = chr(2)
EOT = chr(4)
ACK = chr(6)
NAK = chr(21)
CAN = chr(24)
CRC = chr(67)

class LogXfer(object):

    def __init__(self, log, func):
        self.func = func
        self.log = log
        self.istr = ''
        self.ostr = ''

    def __call__(self, *args, **kw):
        if self.log and isinstance(args[0], (str, unicode)):
            self.istr += args[0]
        ret = self.func(*args, **kw)
        if self.log:
            if isinstance(ret, (str, unicode)):
                self.ostr += ret
            if len(self.istr) > 1 or len(self.ostr) > 128:
                self.dump('IN :', self.istr)
                self.istr = ''
                self.dump('OUT:', self.ostr)
                self.ostr = ''
        return ret

    def dump(self, prefix, s, linelen=16):
        dmp = ''
        while len(s) > 0:
            d = s[:linelen]
            s = s[linelen:]
            h = (' ').join('%02X' % ord(x) for x in d)
            h = h + ' ' * (linelen * 3 - len(h))
            asc = ('').join((x if ord(x) < 128 else '.') for x in d if ord(x) > 31)
            asc = asc + ' ' * (linelen - len(asc))
            dmp += h + ' ' + asc + '\n'

        if len(dmp) > 0:
            self.log.debug(prefix + '\n' + dmp)

    def flush(self):
        self.dump('OUT:', self.ostr)
        self.dump('IN :', self.istr)


class XMODEM(object):
    """
  XMODEM Protocol handler, expects an object to read from and an object to
  write to.
  
  >>> def getc(size, timeout=1):
  ...     return data or None
  ...
  >>> def putc(data, timeout=1):
  ...     return size or None
  ...
  >>> modem = XMODEM(getc, putc)
  
  """
    crctable = [
     0, 4129, 8258, 12387, 16516, 20645, 24774, 28903,
     33032, 37161, 41290, 45419, 49548, 53677, 57806, 61935,
     4657, 528, 12915, 8786, 21173, 17044, 29431, 25302,
     37689, 33560, 45947, 41818, 54205, 50076, 62463, 58334,
     9314, 13379, 1056, 5121, 25830, 29895, 17572, 21637,
     42346, 46411, 34088, 38153, 58862, 62927, 50604, 54669,
     13907, 9842, 5649, 1584, 30423, 26358, 22165, 18100,
     46939, 42874, 38681, 34616, 63455, 59390, 55197, 51132,
     18628, 22757, 26758, 30887, 2112, 6241, 10242, 14371,
     51660, 55789, 59790, 63919, 35144, 39273, 43274, 47403,
     23285, 19156, 31415, 27286, 6769, 2640, 14899, 10770,
     56317, 52188, 64447, 60318, 39801, 35672, 47931, 43802,
     27814, 31879, 19684, 23749, 11298, 15363, 3168, 7233,
     60846, 64911, 52716, 56781, 44330, 48395, 36200, 40265,
     32407, 28342, 24277, 20212, 15891, 11826, 7761, 3696,
     65439, 61374, 57309, 53244, 48923, 44858, 40793, 36728,
     37256, 33193, 45514, 41451, 53516, 49453, 61774, 57711,
     4224, 161, 12482, 8419, 20484, 16421, 28742, 24679,
     33721, 37784, 41979, 46042, 49981, 54044, 58239, 62302,
     689, 4752, 8947, 13010, 16949, 21012, 25207, 29270,
     46570, 42443, 38312, 34185, 62830, 58703, 54572, 50445,
     13538, 9411, 5280, 1153, 29798, 25671, 21540, 17413,
     42971, 47098, 34713, 38840, 59231, 63358, 50973, 55100,
     9939, 14066, 1681, 5808, 26199, 30326, 17941, 22068,
     55628, 51565, 63758, 59695, 39368, 35305, 47498, 43435,
     22596, 18533, 30726, 26663, 6336, 2273, 14466, 10403,
     52093, 56156, 60223, 64286, 35833, 39896, 43963, 48026,
     19061, 23124, 27191, 31254, 2801, 6864, 10931, 14994,
     64814, 60687, 56684, 52557, 48554, 44427, 40424, 36297,
     31782, 27655, 23652, 19525, 15522, 11395, 7392, 3265,
     61215, 65342, 53085, 57212, 44955, 49082, 36825, 40952,
     28183, 32310, 20053, 24180, 11923, 16050, 3793, 7920]

    def __init__(self, getc, putc):
        self.log = logging.getLogger(self.__class__.__name__)
        con = logging.StreamHandler(stream=sys.stdout)
        fmt = logging.Formatter('%(module)s-%(levelname)s: %(message)s')
        con.setFormatter(fmt)
        self.log.setLevel(logging.DEBUG)
        self.log.addHandler(con)
        self.quit = False
        self.retval = None
        self.thread = None
        self.getc = LogXfer(self.log, getc)
        self.putc = LogXfer(self.log, putc)
        return

    def abort(self, count=2, timeout=60):
        """
    Send an abort sequence using CAN bytes.
    """
        for counter in xrange(0, count):
            self.putc(CAN, timeout)

    def send(self, stream, retry=16, timeout=60, quiet=0, background=False):
        if self.thread is not None:
            print 'Oops, Thread running'
            return
        else:
            self.thread = threading.Thread(target=_send, args=(stream, retry, timeout, quiet))
            self.thread.join()
            self.thread = None
            self.putc.flush()
            self.getc.flush()
            return self.retval

    def recv(self, stream, crc_mode=1, retry=16, timeout=60, delay=1, quiet=0, background=False):
        if self.thread is not None:
            print 'Oops, Thread running'
            return
        else:
            self.thread = threading.Thread(target=_recv, args=(stream, crc_mode, retry, timeout, delay, quiet))
            self.thread.join()
            self.thread = None
            self.putc.flush()
            self.getc.flush()
            return self.retval

    def _send(self, stream, retry=16, timeout=60, quiet=0):
        """
    Send a stream via the XMODEM protocol.
    
    >>> stream = file('/etc/issue', 'rb')
    >>> print modem.send(stream)
    True
    
    Returns ``True`` upon succesful transmission or ``False`` in case of
    failure.
    """
        error_count = 0
        crc_mode = 0
        cancel = 0
        while True:
            if self.quit:
                self.abort()
                self.retval = None
                return
            char = self.getc(1)
            if char:
                if char == NAK:
                    crc_mode = 0
                    break
                elif char == CRC:
                    crc_mode = 1
                    break
                elif char == CAN:
                    if not quiet:
                        print >> sys.stderr, 'received CAN'
                    if cancel:
                        self.retval = False
                        return False
                    cancel = 1
                else:
                    self.log.error('send ERROR expected NAK/CRC, got %s' % (
                     ord(char),))
            error_count += 1
            if error_count >= retry:
                self.abort(timeout=timeout)
                self.retval = False
                return False

        error_count = 0
        packet_size = 128
        sequence = 1
        while True:
            if self.quit:
                self.abort()
                self.retval = None
                return
            data = stream.read(packet_size)
            if not data:
                self.log.info('sending EOS')
                break
            data = data.ljust(packet_size, b'\xff')
            if crc_mode:
                crc = self.calc_crc(data)
            else:
                crc = self.calc_checksum(data)
            while True:
                if crc_mode:
                    self.putc(SOH)
                else:
                    self.putc(STX)
                self.putc(chr(sequence))
                self.putc(chr(255 - sequence))
                self.putc(data)
                if crc_mode:
                    self.putc(chr(crc >> 8))
                    self.putc(chr(crc & 255))
                else:
                    self.putc(chr(crc))
                char = self.getc(1, timeout)
                if char == ACK:
                    break
                if char == NAK:
                    error_count += 1
                    if error_count >= retry:
                        self.abort(timeout=timeout)
                        self.log.warning('excessive NAKs, transfer aborted')
                        self.retval = False
                        return False
                    continue
                self.abort(timeout=timeout)
                self.log.error('protocol error')
                self.retval = False
                return False

            sequence = (sequence + 1) % 256

        self.putc(EOT)
        self.retval = True
        return True

    def _recv(self, stream, crc_mode=1, retry=16, timeout=60, delay=1, quiet=0):
        """
    Receive a stream via the XMODEM protocol.
    
    >>> stream = file('/etc/issue', 'wb')
    >>> print modem.recv(stream)
    2342
    
    Returns the number of bytes received on success or ``None`` in case of
    failure.
    """
        error_count = 0
        char = 0
        cancel = 0
        while True:
            if self.quit:
                self.abort()
                self.retval = None
                return
                if error_count >= retry:
                    self.abort(timeout=timeout)
                    self.retval = None
                    return
                    if crc_mode and error_count < retry / 2:
                        self.putc(CRC) or time.sleep(delay)
                        error_count += 1
                else:
                    crc_mode = 0
                    if not self.putc(NAK):
                        time.sleep(delay)
                        error_count += 1
                char = self.getc(1, timeout)
                char or error_count += 1
                continue
            elif char == SOH:
                break
            elif char in [STX, CAN]:
                break
            elif char == CAN:
                if cancel:
                    self.retval = None
                    return
                cancel = 1
            else:
                error_count += 1

        error_count = 0
        income_size = 0
        packet_size = 128
        sequence = 1
        cancel = 0
        while True:
            if self.quit:
                self.abort()
                self.retval = None
                return
            while True:
                if char == SOH:
                    packet_size = 128
                    break
                elif char == STX:
                    packet_size = 1024
                    break
                else:
                    if char == EOT:
                        self.putc(ACK)
                        self.retval = income_size
                        return income_size
                    if char == CAN:
                        if cancel:
                            self.retval = None
                            return
                        cancel = 1
                    else:
                        if not quiet:
                            print >> sys.stderr, 'recv ERROR expected SOH/EOT, got', ord(char)
                        error_count += 1
                        if error_count >= retry:
                            self.abort()
                            self.retval = None
                            return

            error_count = 0
            cancel = 0
            seq1 = ord(self.getc(1))
            seq2 = 255 - ord(self.getc(1))
            if seq1 == sequence and seq2 == sequence:
                data = self.getc(packet_size + 1 + crc_mode)
                if crc_mode:
                    csum = (ord(data[(-2)]) << 8) + ord(data[(-1)])
                    data = data[:-2]
                    self.log.debug('CRC (%04x <> %04x)' % (csum, self.calc_crc(data)))
                    valid = csum == self.calc_crc(data)
                else:
                    csum = data[(-1)]
                    data = data[:-1]
                    self.log.debug('checksum (checksum(%02x <> %02x)' % (ord(csum), self.calc_checksum(data)))
                    valid = ord(csum) == self.calc_checksum(data)
                if valid:
                    income_size += len(data)
                    stream.write(data)
                    self.putc(ACK)
                    sequence = (sequence + 1) % 256
                    char = self.getc(1, timeout)
                    continue
            else:
                self.getc(packet_size + 1 + crc_mode)
                self.log.debug('expecting sequence %d, got %d/%d' % (sequence, seq1, seq2))
            self.putc(NAK)

        return

    def calc_checksum(self, data, checksum=0):
        """
    Calculate the checksum for a given block of data, can also be used to
    update a checksum.
    
    >>> csum = modem.calc_checksum('hello')
    >>> csum = modem.calc_checksum('world', csum)
    >>> hex(csum)
    '0x3c'
    
    """
        return (sum(map(ord, data)) + checksum) % 256

    def calc_crc(self, data, crc=0):
        """
    Calculate the Cyclic Redundancy Check for a given block of data, can
    also be used to update a CRC.
    
    >>> crc = modem.calc_crc('hello')
    >>> crc = modem.calc_crc('world', crc)
    >>> hex(crc)
    '0xd5e3'
    
    """
        for char in data:
            crc = crc << 8 ^ self.crctable[((crc >> 8 ^ ord(char)) & 255)]

        return crc & 65535