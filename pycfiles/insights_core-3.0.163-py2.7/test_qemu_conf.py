# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_qemu_conf.py
# Compiled at: 2019-05-16 13:41:33
from insights.tests import context_wrap
from insights.parsers.qemu_conf import QemuConf
qemu_conf_content = '\n   vnc_listen = "0.0.0.0"\n\n   vnc_auto_unix_socket = 1\n   vnc_tls = 1\n   # comment line\n   vnc_tls_x509_cert_dir = "/etc/pki/libvirt-vnc"\n   security_driver = "selinux"    #inline comment\n   cgroup_device_acl = [\n    "/dev/null", "/dev/full", "/dev/zero",\n    "/dev/random", "/dev/urandom",\n    "/dev/ptmx", "/dev/kvm", "/dev/kqemu",\n    "/dev/rtc","/dev/hpet", "/dev/vfio/vfio"\n    ]\n'
qemu_conf_comment = '\n    # comment line\n    # comment line\n'

def test_sssd_conf():
    result = QemuConf(context_wrap(qemu_conf_content))
    assert result.get('vnc_listen') == '0.0.0.0'
    assert result.get('vnc_tls') == '1'
    assert '/dev/zero' in result.get('cgroup_device_acl')
    assert result.get('security_driver') == 'selinux'
    assert isinstance(result.get('cgroup_device_acl'), list)
    result = QemuConf(context_wrap(qemu_conf_comment))
    assert result.data == {}