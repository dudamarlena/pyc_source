# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/aio_dprcon/protocol.py
# Compiled at: 2017-12-08 15:33:26
# Size of source mod 2**32: 3699 bytes
import asyncio, hashlib, hmac, time
QUAKE_PACKET_HEADER = b'\xff\xff\xff\xff'
RCON_RESPONSE_HEADER = QUAKE_PACKET_HEADER + 'n'
CHALLENGE_PACKET = QUAKE_PACKET_HEADER + 'getchallenge'
CHALLENGE_RESPONSE_HEADER = QUAKE_PACKET_HEADER + 'challenge '
MASTER_RESPONSE_HEADER = QUAKE_PACKET_HEADER + 'getserversResponse'
PING_Q2_PACKET = QUAKE_PACKET_HEADER + 'ping'
PONG_Q2_PACKET = QUAKE_PACKET_HEADER + 'ack'
PING_Q3_PACKET = 'ping'
PONG_Q3_PACKET = QUAKE_PACKET_HEADER + 'disconnect'
QUAKE_STATUS_PACKET = QUAKE_PACKET_HEADER + 'getstatus'
STATUS_RESPONSE_HEADER = QUAKE_PACKET_HEADER + 'statusResponse\n'
RCON_NOSECURE = 0
RCON_SECURE_TIME = 1
RCON_SECURE_CHALLENGE = 2

def ensure_bytes(something):
    if not isinstance(something, bytes):
        return str(something).encode('utf8')
    else:
        return something


def md4(*args, **kwargs):
    return (hashlib.new)('MD4', *args, **kwargs)


def hmac_md4(key, msg):
    return hmac.new(key, msg, md4)


def rcon_nosecure_packet(password, command):
    return QUAKE_PACKET_HEADER + ensure_bytes('rcon {password} {command}'.format(password=password, command=command))


def rcon_secure_time_packet(password, command):
    password = ensure_bytes(password)
    cur_time = time.time()
    key = hmac_md4(password, ensure_bytes('{time:6f} {command}'.format(time=cur_time,
      command=command))).digest()
    return ''.join([
     QUAKE_PACKET_HEADER,
     'srcon HMAC-MD4 TIME ',
     key,
     ensure_bytes(' {time:6f} {command}'.format(time=cur_time, command=command))])


def parse_challenge_response(response):
    l = len(CHALLENGE_RESPONSE_HEADER)
    return response[l:l + 11]


def rcon_secure_challenge_packet(password, challenge, command):
    password = ensure_bytes(password)
    challenge = ensure_bytes(challenge)
    command = ensure_bytes(command)
    hmac_key = ' '.join([challenge, command])
    key = hmac_md4(password, hmac_key).digest()
    return ''.join([
     QUAKE_PACKET_HEADER,
     'srcon HMAC-MD4 CHALLENGE ',
     key,
     ' ',
     challenge,
     ' ',
     command])


def parse_rcon_response(packet):
    return packet[len(RCON_RESPONSE_HEADER):]


def create_rcon_protocol(password, secure, received_callback=None, connection_made_callback=None):

    class RconProtocol(asyncio.DatagramProtocol):

        def __init__(self):
            self.challenge = None
            self.transport = None
            self.local_host = None
            self.local_port = None

        def connection_made(self, transport):
            self.transport = transport
            _, self.local_port = self.transport.get_extra_info('sockname')
            if connection_made_callback:
                connection_made_callback(self)

        def datagram_received(self, data, addr):
            if data.startswith(CHALLENGE_RESPONSE_HEADER):
                self.challenge = parse_challenge_response(data)
            if data.startswith(RCON_RESPONSE_HEADER):
                decoded = parse_rcon_response(data)
                if received_callback:
                    received_callback(decoded, addr)

        def error_received(self, exc):
            pass

        def send(self, command):
            msg = None
            if secure == RCON_SECURE_CHALLENGE:
                raise NotImplementedError()
            else:
                if secure == RCON_SECURE_TIME:
                    msg = rcon_secure_time_packet(password, command)
                else:
                    if secure == RCON_NOSECURE:
                        msg = rcon_nosecure_packet(password, command)
            self.transport.sendto(msg)

    return RconProtocol