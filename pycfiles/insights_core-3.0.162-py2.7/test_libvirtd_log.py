# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_libvirtd_log.py
# Compiled at: 2019-11-14 13:57:46
import doctest
from datetime import datetime
from insights.parsers import libvirtd_log
from insights.tests import context_wrap
LIBVIRTD_LOG = ("\n2013-10-23 17:32:19.909+0000: 14069: debug : do_open:1174 : trying driver 0 (Test) ...\n2013-10-23 17:32:19.909+0000: 14069: debug : do_open:1180 : driver 0 Test returned DECLINED\n2013-10-23 17:32:19.909+0000: 14069: debug : do_open:1174 : trying driver 1 (ESX) ...\n2013-10-23 17:32:19.909+0000: 14069: debug : do_open:1180 : driver 1 ESX returned DECLINED\n2013-10-23 17:32:19.909+0000: 14069: debug : do_open:1174 : trying driver 2 (remote) ...\n2013-10-23 17:32:19.957+0000: 14069: error : virNetTLSContextCheckCertDN:418 : Certificate [session] owner does not match the hostname AA.BB.CC.DD <============= IP Address\n2013-10-23 17:32:19.957+0000: 14069: warning : virNetTLSContextCheckCertificate:1102 : Certificate check failed Certificate [session] owner does not match the hostname AA.BB.CC.DD\n2013-10-23 17:32:19.957+0000: 14069: error : virNetTLSContextCheckCertificate:1105 : authentication failed: Failed to verify peer's certificate\n").strip()
INSTANCE_001 = ('\n2019-06-04 05:33:22.280743Z qemu-kvm: -vnc 10.xxx.xxx.xxx:0: Failed to start VNC server: Failed to bind socket: Cannot assign requested address\n2019-06-04 05:33:2.285+0000: shutting down\n').strip()
INSTANCE_002 = ('\n2019-04-26 06:55:20.388+0000: starting up libvirt version: 2.0.0, package: 10.el7_3.9 (Red Hat, Inc. <http://bugzilla.redhat.com/bugzilla>, 2017-05-04-06:48:37, x86-034.build.example.com), qemu version: 2.6.0 (qemu-kvm-rhev-2.6.0-28.el7_3.9), hostname: f1.example.com\n2019-04-26 06:55:21.280743Z qemu-kvm: -vnc 10.xxx.xxx.xxx:0: Failed to start VNC server: Failed to bind socket: Cannot assign requested address\n').strip()

def test_libvirtd_log():
    log = libvirtd_log.LibVirtdLog(context_wrap(LIBVIRTD_LOG))
    assert 'Certificate check failed Certificate' in log
    assert log.get("authentication failed: Failed to verify peer's certificate")[0]['raw_message'] == "2013-10-23 17:32:19.957+0000: 14069: error : virNetTLSContextCheckCertificate:1105 : authentication failed: Failed to verify peer's certificate"
    assert len(list(log.get_after(datetime(2013, 10, 23, 17, 32, 19)))) == 8


def test_libvirtd_qemu_log():
    log = libvirtd_log.LibVirtdQemuLog(context_wrap(INSTANCE_001, path='/var/log/libvirt/qemu/bb912729-fa51-443b-bac6-bf4c795f082d.log'))
    assert 'shutting down' in log
    log = libvirtd_log.LibVirtdQemuLog(context_wrap(INSTANCE_002, path='/var/log/libvirt/qemu/bb912729-fa51-443b-bac6-bf4c795f081d.log'))
    assert log.file_name == 'bb912729-fa51-443b-bac6-bf4c795f081d.log'
    assert len(list(log.get_after(datetime(2019, 4, 26, 6, 55, 20)))) == 2


def test_documentation():
    failed_count, tests = doctest.testmod(libvirtd_log, globs={'libvirtd_log': libvirtd_log.LibVirtdLog(context_wrap(LIBVIRTD_LOG)), 'libvirtd_qemu_log': libvirtd_log.LibVirtdQemuLog(context_wrap(INSTANCE_001, path='/var/log/libvirt/qemu/bb912729-fa51-443b-bac6-bf4c795f081d.log'))})
    assert failed_count == 0