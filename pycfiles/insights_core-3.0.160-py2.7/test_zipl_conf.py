# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_zipl_conf.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.zipl_conf import ZiplConf
from insights.tests import context_wrap
from insights.parsers import ParseException
import pytest
ZIPL_CONF = ('\n[defaultboot]\ndefaultauto\nprompt=1\ntimeout=5\ndefault=linux\ntarget=/boot\n[linux]\n    image=/boot/vmlinuz-3.10.0-693.el7.s390x\n    ramdisk=/boot/initramfs-3.10.0-693.el7.s390x.img\n    parameters="root=/dev/mapper/rhel_gss5-root crashkernel=auto rd.dasd=0.0.0100 rd.dasd=0.0.0101 rd.dasd=0.0.0102 rd.lvm.lv=rhel_gss5/root rd.lvm.lv=rhel_gss5/swap net.ifnames=0 rd.znet=qeth,0.0.0600,0.0.0601,0.0.0602,layer2=0,portname=gss5,portno=0 LANG=en_US.UTF-8"\n[linux-0-rescue-a27932c8d57248e390cee3798bbd3709]\n    image=/boot/vmlinuz-0-rescue-a27932c8d57248e390cee3798bbd3709\n    ramdisk=/boot/initramfs-0-rescue-a27932c8d57248e390cee3798bbd3709.img\n    parameters="root=/dev/mapper/rhel_gss5-root crashkernel=auto rd.dasd=0.0.0100 rd.dasd=0.0.0101 rd.dasd=0.0.0102 rd.lvm.lv=rhel_gss5/root rd.lvm.lv=rhel_gss5/swap net.ifnames=0 rd.znet=qeth,0.0.0600,0.0.0601,0.0.0602,layer2=0,portname=gss5,portno=0"\n[other]\n    image=/boot/vmlinuz\n    ramdisk=/boot/initramfs.img\n    parameters="root=/dev/mapper/rhel_gss5-root crashkernel=auto rd.dasd=0.0.0100\n\n# Configuration for dumping to SCSI disk\n# Separate IPL and dump partitions\n[dumpscsi]\ntarget=/boot\ndumptofs=/dev/sda2\nparameters="dump_dir=/mydumps dump_compress=none dump_mode=auto"\n\n# Menu containing two DASD boot configurations\n:menu1\n1=linux\n2=linux-0-rescue-a27932c8d57248e390cee3798bbd3709\ndefault=1\nprompt=1\ntimeout=30\n').strip()
ZIPL_CONF_INVALID = ('\nprompt=1\ntimeout=5\ndefault=linux\n[linux]\n    image=/boot/vmlinuz-3.10.0-693.el7.s390x\n    ramdisk=/boot/initramfs-3.10.0-693.el7.s390x.img\n    parameters="root=/dev/mapper/rhel_gss5-root crashkernel=auto rd.dasd=0.0.0100 rd.dasd=0.0.0101 rd.dasd=0.0.0102 rd.lvm.lv=rhel_gss5/root rd.lvm.lv=rhel_gss5/swap net.ifnames=0 rd.znet=qeth,0.0.0600,0.0.0601,0.0.0602,layer2=0,portname=gss5,portno=0 LANG=en_US.UTF-8"\n').strip()

def test_zipl_conf():
    res = ZiplConf(context_wrap(ZIPL_CONF))
    assert res.get('linux').get('image') == '/boot/vmlinuz-3.10.0-693.el7.s390x'
    assert res['linux']['image'] == '/boot/vmlinuz-3.10.0-693.el7.s390x'
    assert res[':menu1']['1'] == 'linux'
    assert 'defaultauto' in res['defaultboot']
    assert res['defaultboot']['defaultauto'] is True
    assert res['other']['parameters'] == '"root=/dev/mapper/rhel_gss5-root crashkernel=auto rd.dasd=0.0.0100'
    assert res.images == {'linux': '/boot/vmlinuz-3.10.0-693.el7.s390x', 
       'linux-0-rescue-a27932c8d57248e390cee3798bbd3709': '/boot/vmlinuz-0-rescue-a27932c8d57248e390cee3798bbd3709', 
       'other': '/boot/vmlinuz'}
    assert res.dumptofses == {'dumpscsi': '/dev/sda2'}


def test_zipl_conf_invalid():
    with pytest.raises(ParseException) as (pe):
        ZiplConf(context_wrap(ZIPL_CONF_INVALID))
    assert 'Invalid zipl configuration file is found.' in str(pe)