# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/tests/test_scannable.py
# Compiled at: 2019-05-16 13:41:33
from insights.core import Scannable
from insights.tests import context_wrap
import pytest
ANACONDA_LOG = '\n02:22:11,538 DEBUG   : readNetInfo /tmp/s390net not found, early return\n02:22:11,538 INFO    : anaconda version 13.21.149 on x86_64 starting\n02:22:14,695 DEBUG   : Saving module iscsi_boot_sysfs\n02:22:14,695 DEBUG   : Saving module pcspkr\n02:22:14,695 DEBUG   : Saving module edd\n02:22:14,695 DEBUG   : Saving module mlx4_ib\n02:22:14,695 DEBUG   : Saving module mlx4_en\n02:22:14,695 DEBUG   : Saving module mlx4_core\n02:22:14,695 DEBUG   : Saving module ib_ipoib\n02:22:14,695 DEBUG   : Saving module ib_cm\n02:22:14,695 DEBUG   : Saving module ib_sa\n02:22:14,695 DEBUG   : Saving module ib_mad\n02:22:14,695 DEBUG   : Saving module ib_core\n02:22:14,695 DEBUG   : Saving module ipv6\n02:22:14,695 DEBUG   : Saving module iscsi_tcp\n02:22:14,695 DEBUG   : Saving module libiscsi_tcp\n02:22:14,695 DEBUG   : Saving module libiscsi\n02:22:14,695 DEBUG   : Saving module scsi_transport_iscsi\n02:22:14,695 DEBUG   : Saving module squashfs\n02:22:14,695 DEBUG   : Saving module cramfs\n02:22:14,695 DEBUG   : probing buses\n02:22:14,705 DEBUG   : waiting for hardware to initialize\n02:22:17,661 INFO    : Trying to detect vendor driver discs\n02:22:17,717 DEBUG   : probing buses\n02:22:17,728 DEBUG   : waiting for hardware to initialize\n02:22:20,853 INFO    : getting kickstart file\n02:22:20,862 INFO    : doing kickstart... setting it up\n02:22:20,862 DEBUG   : activating device eth0\n02:22:25,869 INFO    : wait_for_iface_activation (2289): device eth0 activated\n02:22:28,045 INFO    : kickstart network command - unspecified device\n02:22:28,045 INFO    : activating first device from kickstart because network is needed\n02:22:28,050 INFO    : device eth0 is already activated\n02:22:28,050 INFO    : disconnecting device eth0\n02:22:30,056 INFO    : wait_for_iface_disconnection (2366): device eth0 disconnected\n02:22:30,056 INFO    : doing kickstart... setting it up\n02:22:30,056 DEBUG   : activating device eth0\n02:22:35,064 INFO    : wait_for_iface_activation (2289): device eth0 activated\n02:22:35,065 ERROR   : got to setupCdrom without a CD device\n02:22:35,806 INFO    : Loading SELinux policy\n02:22:36,099 INFO    : getting ready to spawn shell now\n02:22:36,327 INFO    : Running anaconda script /usr/bin/anaconda\n02:22:37,781 INFO    : using only installclass Red Hat Enterprise Linux Server\n02:22:37,835 INFO    : ISCSID is /usr/sbin/iscsid\n02:22:37,835 INFO    : no initiator set\n02:22:37,869 WARNING : \'/usr/libexec/fcoe/fcoe_edd.sh\' specified as full path\n02:22:37,876 INFO    : No FCoE EDD info found: No FCoE boot disk information is found in EDD!\n\n02:22:37,877 INFO    : no /etc/zfcp.conf; not configuring zfcp\n02:22:38,120 INFO    : created new libuser.conf at /tmp/libuser.vg7G_T with instPath="/mnt/sysimage"\n'

class FakeAnacondaLog(Scannable):
    pass


def warnings(line):
    if 'WARNING' in line:
        return line[23:]


def has_fcoe_edd(line):
    return '/usr/libexec/fcoe/fcoe_edd.sh' in line


def has_kernel_panic(line):
    return 'kernel panic' in line


FakeAnacondaLog.any('has_fcoe', has_fcoe_edd)
FakeAnacondaLog.any('panic', has_kernel_panic)
FakeAnacondaLog.collect('warnings', warnings)

def test_scannable():
    ctx = context_wrap(ANACONDA_LOG, path='/root/anaconda.log')
    log = FakeAnacondaLog(ctx)
    assert hasattr(log, 'has_fcoe')
    assert log.has_fcoe is True
    assert hasattr(log, 'panic')
    assert log.panic is False
    assert hasattr(log, 'warnings')
    assert type(log.warnings) == list
    assert len(log.warnings) == 1
    assert log.warnings[0] == "'/usr/libexec/fcoe/fcoe_edd.sh' specified as full path"


def test_duplicate_scanner():
    with pytest.raises(ValueError) as (exc):
        assert FakeAnacondaLog.collect('warnings', lambda x: x + 'extra stuff')
    assert 'is already a registered scanner key' in str(exc)