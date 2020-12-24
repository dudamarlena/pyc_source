# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/qemu_conf.py
# Compiled at: 2019-05-16 13:41:33
"""
QemuConf - file ``/etc/libvirt/qemu.conf``
==========================================

The ``/etc/libvirt/qemu.conf`` file is in a key-value format, but there are several lines for one value.

Given a file containing the following test data::

   vnc_listen = "0.0.0.0"
   vnc_auto_unix_socket = 1
   vnc_tls = 1
   vnc_tls_x509_cert_dir = "/etc/pki/libvirt-vnc"
   security_driver = "selinux"
   cgroup_device_acl = [
    "/dev/null", "/dev/full", "/dev/zero",
    "/dev/random", "/dev/urandom",
    "/dev/ptmx", "/dev/kvm", "/dev/kqemu",
    "/dev/rtc","/dev/hpet", "/dev/vfio/vfio"
    ]

Example:
    >>> config = shared[QemuConf]
    >>> config.get('vnc_listen')
    '0.0.0.0'
    >>> config.get('vnc_tls')
    '1'
    >>> "/dev/random" in config.get('cgroup_device_acl')
    True
"""
import json
from .. import parser, Parser, get_active_lines, LegacyItemAccess
from insights.specs import Specs

@parser(Specs.qemu_conf)
class QemuConf(LegacyItemAccess, Parser):
    """
    A dict of the content of the ``qemu.conf`` configuration file.

    Attributes:
        data (dict): Dictionary of parsed data that splits by '='
    """

    def parse_content(self, content):
        """Parse file content of qemu.conf"""
        _lines = get_active_lines(content, comment_char='#')
        self.data = {}
        current_key = ''
        for line in _lines:
            if '=' in line:
                k, v = line.split('=')
                current_key = k.strip()
                self.data[current_key] = v.strip('"\' ')
            else:
                self.data[current_key] = self.data[current_key] + line
            if self.data[current_key].endswith(']'):
                self.data[current_key] = json.loads(self.data[current_key])