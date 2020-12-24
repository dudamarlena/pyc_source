# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/HologramAuth/SIMOTPAuthentication.py
# Compiled at: 2019-10-24 15:30:15
# Size of source mod 2**32: 2240 bytes
from .Holohash import Holohash
from .HOTPAuthentication import HOTPAuthentication
DEVICE_ID_TYPE = b'H'
NONCE_REQUEST_TYPE = b'N'
DEFAULT_TIME_WINDOW = 30

class SIMOTPAuthentication(HOTPAuthentication):

    def __init__(self, credentials, time_window=DEFAULT_TIME_WINDOW):
        self.time_window = time_window
        self.holohash_client = Holohash()
        self.iccid = None
        self.sim_otp_token = None
        super().__init__(credentials=credentials)

    def buildAuthString(self, timestamp=None, sequence_number=None):
        formatted_string = f"{self.iccid} {self.timestamp} {self.sim_otp_token} "
        self._payload = DEVICE_ID_TYPE + formatted_string.encode('ascii')

    def buildNonceRequestPayloadString(self):
        return NONCE_REQUEST_TYPE

    def generate_sim_otp_command(self, imsi=None, iccid=None, nonce=None, timestamp=None):
        self.timestamp = str(self.generate_timestamp(timestamp))
        self.iccid = iccid
        return self.holohash_client.generate_sim_gsm_milenage_command(imsi, iccid, nonce, self.timestamp)

    def generate_sim_otp_token(self, response):
        self.sim_otp_token = self.holohash_client.generate_milenage_token(response, self.timestamp)

    @property
    def time_window(self):
        return self._time_window

    @time_window.setter
    def time_window(self, time_window):
        self._time_window = time_window