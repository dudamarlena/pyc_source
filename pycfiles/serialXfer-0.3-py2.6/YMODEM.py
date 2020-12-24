# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/serialXfer/YMODEM.py
# Compiled at: 2013-03-27 09:51:07
from XMODEM import *

class YMODEM(XMODEM):

    def __init__(self, *args, **kw):
        self.filename = ''
        self.meta = ''
        super(YMODEM, self).__init__(*args, **kw)

    def _send(self, stream, retry=16, timeout=60, quiet=0):
        """
    Send a stream via the YMODEM protocol.
    
    >>> stream = file('/etc/issue', 'rb')
    >>> print modem.send(stream)
    True
    
    Returns ``True`` upon succesful transmission or ``False`` in case of
    failure.
    """
        error_count = 0
        cancel = 0
        while True:
            char = self.getc(1)
            if char:
                if char == CRC:
                    break
                if char == CAN:
                    if not quiet:
                        print >> sys.stderr, 'received CAN'
                    if cancel:
                        self.retval = False
                        return False
                    cancel = 1
                else:
                    self.log.error('send ERROR expected CRC, got %s' % (ord(char),))
            error_count += 1
            if error_count >= retry:
                self.abort(timeout=timeout)
                self.retval = False
                return False

        error_count = 0
        packet_size = 128
        sequence = 0
        while True:
            if sequence == 0:
                data = stream.name + chr(0)
                data += '%d\x00' % os.stat(stream.name).st_size
                data += chr(0) * (pack_size - len(data))
            else:
                data = stream.read(packet_size)
            if not data:
                self.log.info('sending EOS')
                break
            data = data.ljust(packet_size, b'\xff')
            crc = self.calc_crc(data)
            while True:
                self.putc(SOH)
                self.putc(chr(sequence))
                self.putc(chr(255 - sequence))
                self.putc(data)
                self.putc(chr(crc >> 8))
                self.putc(chr(crc & 255))
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

    def _recv(self, stream, crc_mode, retry=16, timeout=60, delay=1, quiet=0):
        """
    Receive a stream via the YMODEM protocol.
    
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
            if error_count >= retry:
                self.abort(timeout=timeout)
                self.retval = None
                return
                if error_count < retry / 2:
                    if not self.putc(CRC):
                        time.sleep(delay)
                        error_count += 1
                char = self.getc(1, timeout)
                char or error_count += 1
                continue
            elif char in [SOH, STX]:
                break
            elif char == CAN:
                if cancel:
                    self.retval = None
                    return
                cancel = 1
            else:
                error_count += 1

        error_count = 0
        expected_size = 0
        income_size = 0
        packet_size = 128
        sequence = 0
        cancel = 0
        while True:
            while True:
                if char == SOH:
                    packet_size = 128
                    break
                elif char == STX:
                    packet_size = 1024
                    break
                elif char == EOT:
                    self.putc(ACK)
                    if expected_size > 0 and income_size >= expected_size:
                        self.retval = expected_size
                        return expected_size
                    self.retval = income_size
                    return income_size
                elif char == CAN:
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
                data = self.getc(packet_size + 2)
                csum = (ord(data[(-2)]) << 8) + ord(data[(-1)])
                data = data[:-2]
                self.log.debug('CRC (%04x <> %04x)' % (
                 csum, self.calc_crc(data)))
                valid = csum == self.calc_crc(data)
                if valid:
                    self.putc(ACK)
                    if seq1 == seq2 == 0:
                        self.putc(CRC)
                        filename = data.split(chr(0), 1)[0]
                        if len(filename) > 0:
                            meta = data[len(filename) + 1:].split(chr(0), 1)[0]
                            try:
                                meta = map(int, meta.split(' '))
                            except ValueError:
                                pass
                            else:
                                if len(meta) > 0:
                                    expected_size = int(meta[0])
                                self.log.debug(('').join(x for x in data if ord(x) > 31))
                                self.filename = filename
                                self.meta = meta
                    else:
                        income_size += len(data)
                        if expected_size > 0 and income_size > expected_size:
                            remain_size = expected_size - income_size
                        else:
                            remain_size = len(data)
                        stream.write(data[:remain_size])
                    sequence = (sequence + 1) % 256
                    char = self.getc(1, timeout)
                    continue
            else:
                self.getc(packet_size + 2)
                self.log.debug('expecting sequence %d, got %d/%d' % (sequence, seq1, seq2))
            self.putc(NAK)

        return