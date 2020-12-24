# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/arch/api/utils/core_utils.py
# Compiled at: 2020-04-28 09:19:05
# Size of source mod 2**32: 2930 bytes
import base64, json, os, pickle, socket, time, uuid

def fate_uuid():
    return uuid.uuid1().hex


def get_commit_id():
    return fate_uuid()


def string_to_bytes(string):
    if isinstance(string, bytes):
        return string
    return string.encode(encoding='utf-8')


def bytes_to_string(byte):
    return byte.decode(encoding='utf-8')


def json_dumps(src, byte=False):
    if byte:
        return string_to_bytes(json.dumps(src))
    return json.dumps(src)


def json_loads(src):
    if isinstance(src, bytes):
        return json.loads(bytes_to_string(src))
    return json.loads(src)


def current_timestamp():
    return int(time.time() * 1000)


def timestamp_to_date(timestamp, format_string='%Y-%m-%d %H:%M:%S'):
    timestamp = int(timestamp) / 1000
    time_array = time.localtime(timestamp)
    str_date = time.strftime(format_string, time_array)
    return str_date


def base64_encode(src):
    return bytes_to_string(base64.b64encode(src.encode('utf-8')))


def base64_decode(src):
    return bytes_to_string(base64.b64decode(src))


def serialize_b64(src, to_str=False):
    dest = base64.b64encode(pickle.dumps(src))
    if not to_str:
        return dest
    return bytes_to_string(dest)


def deserialize_b64(src):
    return pickle.loads(base64.b64decode(string_to_bytes(src) if isinstance(src, str) else src))


def get_lan_ip():
    if os.name != 'nt':
        import fcntl, struct

        def get_interface_ip(ifname):
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 35093, struct.pack('256s', string_to_bytes(ifname[:15])))[20:24])

    ip = socket.gethostbyname(socket.getfqdn())
    if ip.startswith('127.'):
        if os.name != 'nt':
            interfaces = [
             'bond1',
             'eth0',
             'eth1',
             'eth2',
             'wlan0',
             'wlan1',
             'wifi0',
             'ath0',
             'ath1',
             'ppp0']
            for ifname in interfaces:
                try:
                    ip = get_interface_ip(ifname)
                    break
                except IOError as e:
                    try:
                        pass
                    finally:
                        e = None
                        del e

    return ip or ''