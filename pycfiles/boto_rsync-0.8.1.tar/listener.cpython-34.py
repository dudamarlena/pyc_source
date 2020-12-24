# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/ec2/elb/listener.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 3377 bytes
from boto.ec2.elb.listelement import ListElement

class Listener(object):
    """Listener"""

    def __init__(self, load_balancer=None, load_balancer_port=0, instance_port=0, protocol='', ssl_certificate_id=None, instance_protocol=None):
        self.load_balancer = load_balancer
        self.load_balancer_port = load_balancer_port
        self.instance_port = instance_port
        self.protocol = protocol
        self.instance_protocol = instance_protocol
        self.ssl_certificate_id = ssl_certificate_id
        self.policy_names = ListElement()

    def __repr__(self):
        r = "(%d, %d, '%s'" % (self.load_balancer_port, self.instance_port, self.protocol)
        if self.instance_protocol:
            r += ", '%s'" % self.instance_protocol
        if self.ssl_certificate_id:
            r += ', %s' % self.ssl_certificate_id
        r += ')'
        return r

    def startElement(self, name, attrs, connection):
        if name == 'PolicyNames':
            return self.policy_names

    def endElement(self, name, value, connection):
        if name == 'LoadBalancerPort':
            self.load_balancer_port = int(value)
        else:
            if name == 'InstancePort':
                self.instance_port = int(value)
            else:
                if name == 'InstanceProtocol':
                    self.instance_protocol = value
                else:
                    if name == 'Protocol':
                        self.protocol = value
                    else:
                        if name == 'SSLCertificateId':
                            self.ssl_certificate_id = value
                        else:
                            setattr(self, name, value)

    def get_tuple(self):
        return (
         self.load_balancer_port, self.instance_port, self.protocol)

    def get_complex_tuple(self):
        return (
         self.load_balancer_port, self.instance_port, self.protocol, self.instance_protocol)

    def __getitem__(self, key):
        if key == 0:
            return self.load_balancer_port
        if key == 1:
            return self.instance_port
        if key == 2:
            return self.protocol
        if key == 3:
            return self.instance_protocol
        if key == 4:
            return self.ssl_certificate_id
        raise KeyError