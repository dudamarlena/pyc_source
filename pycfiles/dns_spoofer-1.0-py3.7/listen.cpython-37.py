# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spoofer/listen.py
# Compiled at: 2019-10-19 23:58:06
# Size of source mod 2**32: 1056 bytes
import argparse, sys, socket, dns.message, dns.exception

def listen_udp(port, address, timeout=3):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout)
    sock.bind((address, port))
    print(('Listening on port {} and address {}...'.format(port, address)), file=(sys.stderr))
    while True:
        try:
            wire, addr = sock.recvfrom(65535)
        except socket.timeout:
            continue
        else:
            print('Got {} bytes from {}'.format(len(wire), addr))
        try:
            answer = dns.message.from_wire(wire)
        except dns.exception.DNSException as e:
            try:
                print(('got DNS exception "{}": {}'.format(type(e), e)), file=(sys.stderr))
            finally:
                e = None
                del e

        else:
            print(answer)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('port', type=int)
    parser.add_argument('--addr', '--address', dest='address', default='')
    args = parser.parse_args()
    listen_udp(args.port, args.address)


if __name__ == '__main__':
    main()