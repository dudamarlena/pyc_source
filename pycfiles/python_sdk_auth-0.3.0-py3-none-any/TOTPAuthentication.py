# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/HologramAuth/TOTPAuthentication.py
# Compiled at: 2019-10-24 15:30:15
# Size of source mod 2**32: 2065 bytes
import hashlib, hmac, struct
from .HOTPAuthentication import HOTPAuthentication
DEFAULT_TIME_WINDOW = 30
DEVICE_ID_TYPE = 'C'

class TOTPAuthentication(HOTPAuthentication):

    def __init__(self, credentials, time_window=DEFAULT_TIME_WINDOW):
        self.time_window = time_window
        super().__init__(credentials=credentials)

    def buildAuthString(self, timestamp=None, sequence_number=None):
        timestamp = self.generate_timestamp(timestamp)
        sequence_number = timestamp // self.time_window
        self._TOTPAuthentication__update_sequence_number(sequence_number)
        self.generate_auth_payload(timestamp, sequence_number)

    def __update_sequence_number(self, sequence_number):
        if sequence_number is None:
            self._last_sequence_number = self._last_sequence_number + 1
        else:
            self._last_sequence_number = sequence_number

    def generate_auth_payload(self, timestamp, sequence_number):
        hmac_digest = hmac.new(self.credentials['private_key'].encode('ascii'), struct.pack('>Q', sequence_number), hashlib.sha1).digest()
        i = hmac_digest[19] & 15
        modulo_hmac = (struct.unpack('>I', hmac_digest[i:i + 4])[0] & 2147483647) % self._modulus
        formatted_string = f"{DEVICE_ID_TYPE}{self.credentials['device_id']} {timestamp} {modulo_hmac} "
        self._payload = formatted_string.encode('ascii')

    @property
    def time_window(self):
        return self._time_window

    @time_window.setter
    def time_window(self, time_window):
        self._time_window = time_window