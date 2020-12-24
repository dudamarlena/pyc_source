# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Dean\Documents\Python\python-elgato-streamdeck\src\StreamDeck\Transport\Dummy.py
# Compiled at: 2020-04-11 03:12:02
# Size of source mod 2**32: 1512 bytes
import logging, binascii
from .Transport import Transport, TransportError

class Dummy(Transport):
    __doc__ = '\n    Dummy transport layer, for testing.\n    '

    class Device(Transport.Device):

        def __init__(self, device_id):
            self.id = device_id

        def open(self):
            logging.info('Deck opened')

        def close(self):
            logging.info('Deck closed')

        def connected(self):
            return True

        def path(self):
            return self.id

        def write_feature(self, payload):
            logging.info('Deck feature write (length %s): %s', len(payload), binascii.hexlify(payload))
            return True

        def read_feature(self, report_id, length):
            logging.info('Deck feature read (length %s)', length)
            raise TransportError('Dummy device!')

        def write(self, payload):
            logging.info('Deck report write (length %s): %s', len(payload), binascii.hexlify(payload))
            return True

        def read(self, length):
            logging.info('Deck report read (length %s)', length)
            raise TransportError('Dummy device!')

    @staticmethod
    def probe():
        pass

    def enumerate(self, vid, pid):
        return [
         Dummy.Device('{}:{}'.format(vid, pid))]