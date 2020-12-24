# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/arprequest.py
# Compiled at: 2009-05-09 19:17:00
import socket
from struct import pack, unpack
import signal
ARP_GRATUITOUS = 1
ARP_STANDARD = 2

def val2int(val):
    """Retourne une valeur sous forme d'octet en valeur sous forme 
       d'entier."""
    return int(('').join([ '%02d' % ord(c) for c in val ]), 16)


class TimeoutError(Exception):
    """Exception levée après un timeout."""
    pass


def timeout(function, timeout=10):
    u"""Exécute la fonction function (référence) et stoppe son exécution
       au bout d'un certain temps déterminé par timeout.
       
       Retourne None si la fonction à été arretée par le timeout, et 
       la valeur retournée par la fonction si son exécution se 
       termine."""

    def raise_timeout(num, frame):
        raise TimeoutError

    signal.signal(signal.SIGALRM, raise_timeout)
    signal.alarm(timeout)
    try:
        retvalue = function()
    except TimeoutError:
        return

    signal.alarm(0)
    return retvalue
    return


class ArpRequest:
    """Génère une requête ARP et attend la réponse"""

    def __init__(self, ipaddr, if_name, arp_type=ARP_GRATUITOUS):
        self.arp_type = arp_type
        self.if_ipaddr = socket.gethostbyname(socket.gethostname())
        self.socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.SOCK_RAW)
        self.socket.bind((if_name, socket.SOCK_RAW))
        self.ipaddr = ipaddr

    def request(self):
        u"""Envois une requête arp et attend la réponse"""
        for _ in range(5):
            self._send_arp_request()

        if timeout(self._wait_response, 3):
            return True
        else:
            return False

    def _send_arp_request(self):
        u"""Envois une requête ARP pour la machine"""
        if self.arp_type == ARP_STANDARD:
            saddr = pack('!4B', *[ int(x) for x in self.if_ipaddr.split('.') ])
        else:
            saddr = pack('!4B', *[ int(x) for x in self.ipaddr.split('.') ])
        frame = [
         pack('!6B', *(255, 255, 255, 255, 255, 255)),
         self.socket.getsockname()[4],
         pack('!H', 2054),
         pack('!HHBB', 1, 2048, 6, 4),
         pack('!H', 1),
         self.socket.getsockname()[4],
         saddr,
         pack('!6B', *(0, 0, 0, 0, 0, 0)),
         pack('!4B', *[ int(x) for x in self.ipaddr.split('.') ])]
        self.socket.send(('').join(frame))

    def _wait_response(self):
        u"""Attend la réponse de la machine"""
        while 1:
            frame = self.socket.recv(1024)
            proto_type = val2int(unpack('!2s', frame[12:14])[0])
            if proto_type != 2054:
                continue
            op = val2int(unpack('!2s', frame[20:22])[0])
            if op != 2:
                continue
            arp_headers = frame[18:20]
            arp_headers_values = unpack('!1s1s', arp_headers)
            (hw_size, pt_size) = [ val2int(v) for v in arp_headers_values ]
            total_addresses_byte = hw_size * 2 + pt_size * 2
            arp_addrs = frame[22:22 + total_addresses_byte]
            (src_hw, src_pt, dst_hw, dst_pt) = unpack('!%ss%ss%ss%ss' % (
             hw_size, pt_size, hw_size, pt_size), arp_addrs)
            if src_pt == pack('!4B', *[ int(x) for x in self.ipaddr.split('.') ]):
                return True