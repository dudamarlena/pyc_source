# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/firewall.py
# Compiled at: 2017-04-03 02:32:49
# Size of source mod 2**32: 2693 bytes
"""Firewall rule representation"""

class DNATRule(object):
    __doc__ = 'Definition of a DNAT Rule\n\n    :param proto:\n        Proto for the redirection\n    :type proto:\n        ``str``\n    :param orig_ip:\n        Original destination IP to be rewriten.\n    :type orig_ip:\n        ``str``\n    :param orig_port:\n        Original destination prot to be rewriten.\n    :type orig_port:\n        ``str``\n    :param new_ip:\n        New destination IP.\n    :type new_ip:\n        ``str``\n    :param new_port:\n        New destination port.\n    :type new_port:\n        ``str``\n    '
    __slots__ = ('proto', 'orig_ip', 'orig_port', 'new_ip', 'new_port')

    def __init__(self, proto, orig_ip, orig_port, new_ip, new_port):
        self.proto = proto
        self.orig_ip = orig_ip
        self.orig_port = orig_port
        self.new_ip = new_ip
        self.new_port = new_port

    def __repr__(self):
        return '{cls}({proto}:{origip}:{origport}->{newip}:{newport})'.format(cls=self.__class__.__name__, proto=self.proto, origip=self.orig_ip, origport=self.orig_port, newip=self.new_ip, newport=self.new_port)

    def __eq__(self, other):
        return self.proto == other.proto and self.orig_ip == other.orig_ip and self.orig_port == other.orig_port and self.new_ip == other.new_ip and self.new_port == other.new_port

    def __hash__(self):
        return hash((
         self.proto,
         self.orig_ip,
         self.orig_port,
         self.new_ip,
         self.new_port))


class PassThroughRule(object):
    __doc__ = 'Definition of a PassThrough rule\n\n    :param src_ip:\n        Source IP address for which to set the passthrough\n    :type src_ip:\n        ``str``\n    :param dst_ip:\n        Destination IP address for which to set the passthrough\n    :type dst_ip:\n        ``str``\n    '
    __slots__ = ('src_ip', 'dst_ip')

    def __init__(self, src_ip, dst_ip):
        self.src_ip = src_ip
        self.dst_ip = dst_ip

    def __repr__(self):
        return '{cls}({src_ip}->{dst_ip})'.format(cls=self.__class__.__name__, src_ip=self.src_ip, dst_ip=self.dst_ip)

    def __eq__(self, other):
        return self.src_ip == other.src_ip and self.dst_ip == other.dst_ip

    def __hash__(self):
        return hash((
         self.src_ip,
         self.dst_ip))