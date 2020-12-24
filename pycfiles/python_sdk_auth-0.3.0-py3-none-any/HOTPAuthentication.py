# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/HologramAuth/HOTPAuthentication.py
# Compiled at: 2019-10-24 15:30:15
# Size of source mod 2**32: 3238 bytes
import Hologram.Authentication.HologramAuthentication as HologramAuthentication
TOPIC_TYPE = b'T'
BINARY_TYPE = b'B'
METADATA_COMPACT_TYPE = b'M'
DEFAULT_MODULUS = 1000000

class HOTPAuthentication(HologramAuthentication):

    def __init__(self, credentials, last_sequence_number=-1, to_validate_sequence_number=True, modulus=DEFAULT_MODULUS):
        self._last_sequence_number = last_sequence_number
        self._to_validate_sequence_number = to_validate_sequence_number
        self._modulus = modulus
        self._payload = ''
        super().__init__(credentials)

    def buildPayloadString(self, messages, topics=None, modem_type=None, modem_id=None, version=None):
        super().buildPayloadString(messages, topics=topics,
          modem_type=modem_type,
          modem_id=modem_id,
          version=version)
        return self._payload

    def buildAuthString(self, timestamp=None, sequence_number=None):
        raise NotImplementedError('Internal Authentication error: Must define a HOTPAuthentication type')

    def buildMetadataString(self, modem_type, modem_id, version):
        formatted_string = f"{self.build_modem_type_id_str(modem_type, modem_id)}-{version}"
        self._payload += METADATA_COMPACT_TYPE + self.metadata_version + formatted_string.encode('ascii') + bytes([0])

    def buildTopicString(self, topics):
        if isinstance(topics, str):
            topics = [
             topics]
        for topic in topics:
            self._payload += TOPIC_TYPE + topic.encode() + bytes([0])

    def buildMessageString(self, messages):
        if isinstance(messages, str):
            messages = [
             messages]
        for message in messages:
            self._payload += BINARY_TYPE + message.encode() + bytes([0])

        self._payload += bytes([0])

    def enforce_sequence_number(self, sequence_number):
        if not self._to_validate_sequence_number or sequence_number is None:
            return
        if sequence_number <= self._last_sequence_number:
            raise ValueError('HOTP Assertion Failure: Sequence number must always                              be greater than last sequence number for                              cryptographically secure transport')

    def generate_timestamp(self, timestamp):
        self.time = None
        if timestamp is None:
            if self.time is None:
                self.time = __import__('time')
            timestamp = int(self.time.mktime(self.time.localtime()))
        timestamp = int(timestamp)
        if timestamp is None:
            raise ValueError('HOTP Assertion Failure: Timestamp must be specified')
        return timestamp