# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cloud_admin/hosts/eucalyptusconf.py
# Compiled at: 2018-01-31 14:44:08
from argparse import Namespace
import re

class EucalyptusConf(Namespace):

    def __init__(self, lines=None, **kwargs):
        self.set_defaults()
        self.unparsedlines = None
        if 'lines' in kwargs:
            kwargs.pop('lines')
        super(EucalyptusConf, self).__init__(**kwargs)
        if lines:
            self.update_from_string(lines)
        return

    def set_defaults(self):
        self.EUCALYPTUS = ''
        self.LOGLEVEL = ''
        self.EUCA_USER = ''
        self.CLOUD_OPTS = ''
        self.CC_PORT = ''
        self.SCHEDPOLICY = ''
        self.NODES = ''
        self.NC_SERVICE = ''
        self.NC_PORT = ''
        self.NC_WORK_SIZE = ''
        self.NC_CACHE_SIZE = ''
        self.HYPERVISOR = ''
        self.MAX_CORES = ''
        self.INSTANCE_PATH = ''
        self.USE_VIRTIO_ROOT = ''
        self.USE_VIRTIO_DISK = ''
        self.USE_VIRTIO_NET = ''
        self.VNET_MODE = ''
        self.VNET_PRIVINTERFACE = ''
        self.VNET_PUBINTERFACE = ''
        self.VNET_BRIDGE = ''
        self.VNET_DHCPDAEMON = ''
        self.VNET_PUBLICIPS = ''
        self.VNET_SUBNET = ''
        self.VNET_NETMASK = ''
        self.VNET_ADDRSPERNET = ''
        self.VNET_DNS = ''
        self.VNET_BROADCAST = ''
        self.VNET_ROUTER = ''
        self.VNET_DOMAINNAME = ''
        self.LOGLEVEL = ''
        self.METADATA_USE_VM_PRIVATE = ''
        self.METADATA_IP = ''
        self.NC_ROUTER = ''
        self.DISABLE_TUNNELING = ''

    def update_from_string(self, lines):
        self.set_defaults()
        if not lines:
            return
        else:
            unparsedlines = ''
            if not isinstance(lines, list):
                lines = str(lines).splitlines()
            unparsedlines = ''
            for line in lines:
                line.strip()
                if not re.match('^#', line):
                    match = re.search('^(\\w+)=\\s*(\\S+)$', line)
                if not match:
                    unparsedlines += line + '\n'
                else:
                    key = match.group(1)
                    value = match.group(2)
                    value = str(value).strip('"').strip("'")
                    self.__setattr__(key, value)

            self.unparsedlines = unparsedlines or None
            return self