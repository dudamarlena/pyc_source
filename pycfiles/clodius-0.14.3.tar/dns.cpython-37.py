# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/MyKings/Documents/github/clocwalk/clocwalk/dns.py
# Compiled at: 2020-02-25 03:22:55
# Size of source mod 2**32: 246 bytes
from pydnserver import DNSServer
ip = '192.168.199.173'
dns = DNSServer(interface=ip, port=5353)
dns.start()
try:
    while True:
        pass

except KeyboardInterrupt:
    dns.stop()