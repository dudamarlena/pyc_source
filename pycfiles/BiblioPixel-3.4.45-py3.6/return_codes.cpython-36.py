# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/drivers/return_codes.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 1123 bytes
from ..util import log

class RETURN_CODES:
    SUCCESS = 255
    REBOOT = 42
    ERROR = 0
    ERROR_SIZE = 1
    ERROR_UNSUPPORTED = 2
    ERROR_PIXEL_COUNT = 3
    ERROR_BAD_CMD = 4


RETURN_CODE_ERRORS = {RETURN_CODES.SUCCESS: 'Success!', 
 RETURN_CODES.REBOOT: 'Device reboot needed after configuration.', 
 RETURN_CODES.ERROR: 'Generic error', 
 RETURN_CODES.ERROR_SIZE: 'Data packet size incorrect.', 
 RETURN_CODES.ERROR_UNSUPPORTED: 'Unsupported configuration attempted.', 
 RETURN_CODES.ERROR_PIXEL_COUNT: 'Wrong number of pixels for device.', 
 RETURN_CODES.ERROR_BAD_CMD: 'Unsupported protocol command. Check your device version.'}

class BiblioSerialError(Exception):
    pass


def print_error(error):
    msg = RETURN_CODE_ERRORS.get(error, 'Unknown error occured.')
    log.error('%s: %s', error, msg)


def raise_error(error):
    raise BiblioSerialError(print_error(error))