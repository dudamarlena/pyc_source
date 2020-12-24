# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pi/Desktop/tests/lib/python2.7/site-packages/uuidreader/utils.py
# Compiled at: 2017-07-29 03:54:45
import uuid, datetime

def debug_print(msg, debug=False):
    if debug:
        timestamp = ('<%Y-%m-%d %H:%M:%S>').format(datetime.datetime.now())
        print timestamp + ' ' + msg


def rfid_code_to_uuid(rfid_code, debug=False):
    """
    Convert the RFID Code to a UUID in the format
    6ba7b810-9dad-11d1-80b4-00c04fd430c8

    :param rfid_code:
    :param debug:
    :return:
    """
    debug_print('Convert RFID Code to UUID', debug)
    rfid_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, str(rfid_code)))
    debug_print(str(rfid_code) + ' -> ' + rfid_uuid, debug)
    return rfid_uuid