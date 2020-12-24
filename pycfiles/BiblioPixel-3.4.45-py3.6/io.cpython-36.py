# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/drivers/serial/io.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 623 bytes
import serial
from ...drivers.return_codes import RETURN_CODES
from ...util import log, util

def send_packet(cmd, size, dev, baudrate, timeout, more_data=None):
    packet = util.generate_header(cmd, size)
    if more_data:
        packet.append(more_data)
    com = serial.Serial(dev, baudrate=baudrate, timeout=timeout)
    com.write(packet)
    code = read_byte(com)
    ok = code == RETURN_CODES.SUCCESS
    return (com, code, ok)


def read_byte(com):
    try:
        resp = com.read(1)
        if resp:
            return ord(resp)
    except Exception as e:
        log.error('Serial exception %s in read', e)