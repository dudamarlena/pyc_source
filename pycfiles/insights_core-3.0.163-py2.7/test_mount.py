# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_mount.py
# Compiled at: 2019-11-14 13:57:46
""""
test mount
==========
"""
from insights.parsers import ParseException, SkipException
from insights.parsers import mount
from insights.parsers.mount import Mount, ProcMounts
from insights.tests import context_wrap
import pytest, doctest
MOUNT_DATA = ('\ntmpfs on /tmp type tmpfs (rw,seclabel)\nhugetlbfs on /dev/hugepages type hugetlbfs (rw,relatime,seclabel)\nnfsd on /proc/fs/nfsd type nfsd (rw,relatime)\n/dev/sda1 on /boot type ext4 (rw,relatime,seclabel,data=ordered)\n/dev/mapper/fedora-home on /home type ext4 (rw,relatime,seclabel,data=ordered)\n/dev/mapper/fedora-root on / type ext4 (rw,relatime,seclabel,data=ordered)\nsunrpc on /var/lib/nfs/rpc_pipefs type rpc_pipefs (rw,relatime)\ntmpfs on /run/user/42 type tmpfs (rw,nosuid,nodev,relatime,seclabel,size=1605428k,mode=700,uid=42,gid=42)\ntmpfs on /run/user/1000 type tmpfs (rw,nosuid,nodev,relatime,seclabel,size=1605428k,mode=700,uid=1000,gid=1000)\ngvfsd-fuse on /run/user/1000/gvfs type fuse.gvfsd-fuse (rw,nosuid,nodev,relatime,user_id=1000,group_id=1000)\nfusectl on /sys/fs/fuse/connections type fusectl (rw,relatime)\n/dev/mapper/HostVG-Config on /etc/shadow type ext4 (rw,noatime,seclabel,stripe=256,data=ordered) [CONFIG]\n/dev/sr0 on /run/media/root/VMware Tools type iso9660 (ro,nosuid,nodev,relatime,uid=0,gid=0,iocharset=utf8,mode=0400,dmode=0500,uhelper=udisks2) [VMware Tools]\n').strip()
MOUNT_ERR_DATA = ('\ntmpfs on /tmp type tmpfs (rw,seclabel)\nhugetlbfs /dev/hugepages type hugetlbfs (rw,relatime,seclabel)\n/dev/mapper/fedora-root on / type ext4 (rw,relatime,seclabel,data=ordered)\n').strip()
MOUNT_WITHOUT_ROOT = ('\ntmpfs on /tmp type tmpfs (rw,seclabel)\nhugetlbfs on /dev/hugepages type hugetlbfs (rw,relatime,seclabel)\n/dev/sda1 on /boot type ext4 (rw,relatime,seclabel,data=ordered)\n').strip()
PROC_MOUNT = ('\nproc /proc proc rw,relatime 0 0\nsysfs /sys sysfs rw,relatime 0 0\ndevtmpfs /dev devtmpfs rw,relatime,size=8155456k,nr_inodes=2038864,mode=755 0 0\ndevpts /dev/pts devpts rw,relatime,gid=5,mode=620,ptmxmode=000 0 0\ntmpfs /dev/shm tmpfs rw,nosuid,nodev,noexec,relatime 0 0\n/dev/mapper/rootvg-rootlv / ext4 rw,relatime,barrier=1,data=ordered 0 0\n/proc/bus/usb /proc/bus/usb usbfs rw,relatime 0 0\n/dev/sda1 /boot ext4 rw,relatime,barrier=1,data=ordered 0 0\n/dev/mapper/rootvg-homelv /home ext4 rw,relatime,barrier=1,data=ordered 0 0\n/dev/mapper/rootvg-optlv /opt ext4 rw,relatime,barrier=1,data=ordered 0 0\n/dev/mapper/rootvg-tmplv /tmp ext4 rw,relatime,barrier=1,data=ordered 0 0\n/dev/mapper/rootvg-usrlv /usr ext4 rw,relatime,barrier=1,data=ordered 0 0\n/dev/mapper/rootvg-varlv /var ext4 rw,relatime,barrier=1,data=ordered 0 0\n/dev/mapper/rootvg-tmplv /var/tmp ext4 rw,relatime,barrier=1,data=ordered 0 0\nnone /proc/sys/fs/binfmt_misc binfmt_misc rw,relatime 0 0\nsunrpc /var/lib/nfs/rpc_pipefs rpc_pipefs rw,relatime 0 0\n/vol/vol3/wpsanet /sa/net nfs rw,relatime,vers=3,rsize=8192,wsize=8192,namlen=255,soft,proto=tcp,timeo=14,retrans=2,sec=sys,mountaddr=10.xx.xx.xx,mountvers=3,mountport=4046,mountproto=udp,local_lock=none 0 0\n/vol/vol9/home /users nfs rw,relatime,vers=3,rsize=8192,wsize=8192,namlen=255,soft,proto=tcp,timeo=14,retrans=2,sec=sys,mountaddr=10.xx.xx.xx,mountvers=3,mountport=4046,mountproto=udp,local_lock=none,addr=10.xx.xx.xx 0 0\n/etc/auto.misc /misc autofs rw,relatime,fd=7,pgrp=1936,timeout=300,minproto=5,maxproto=5,indirect 0 0\n').strip()
PROCMOUNT_ERR_DATA = ('\nrootfs / rootfs rw 0 0\nsysfs /sys sysfs rw,relatime\n').strip()
PROC_EXCEPTION1 = ('\n').strip()
PROC_EXCEPTION2 = ('\nproc /proc proc rw,relatime 0 0\nsysfs /sys sysfs rw,relatime 0 0\ndevtmpfs /dev devtmpfs rw,relatime,size=8155456k,nr_inodes=2038864,mode=755 0 0\n').strip()
MOUNT_DOC = ('\n/dev/mapper/rootvg-rootlv on / type ext4 (rw,relatime,barrier=1,data=ordered)\nproc on /proc type proc (rw,nosuid,nodev,noexec,relatime)\n/dev/mapper/HostVG-Config on /etc/shadow type ext4 (rw,noatime,seclabel,stripe=256,data=ordered)\ndev/sr0 on /run/media/root/VMware Tools type iso9660 (ro,nosuid,nodev,relatime,uid=0,gid=0,iocharset=utf8,mode=0400,dmode=0500,uhelper=udisks2) [VMware Tools]\n').strip()
PROC_MOUNT_DOC = ('\n/dev/mapper/rootvg-rootlv / ext4 rw,relatime,barrier=1,data=ordered 0 0\nproc /proc proc rw,nosuid,nodev,noexec,relatime 0 0\n/dev/mapper/HostVG-Config /etc/shadow ext4 rw,noatime,seclabel,stripe=256,data=ordered 0 0\ndev/sr0 /run/media/root/VMware Tools iso9660 ro,nosuid,nodev,relatime,uid=0,gid=0,iocharset=utf8,mode=0400,dmode=0500,uhelper=udisks2 0 0\n').strip()
MOUNT_DATA_WITH_SPECIAL_MNT_POINT = ('\nhugetlbfs on /dev/hugepages type hugetlbfs (rw,relatime,seclabel)\n/dev/sda1 on /boot type ext4 (rw,relatime,seclabel,data=ordered)\n/dev/mapper/fedora-root on / type ext4 (rw,relatime,seclabel,data=ordered)\n/dev/mapper/HostVG-Config on /etc/shadow type ext4 (rw,noatime,seclabel,stripe=256,data=ordered) [CONFIG]\n/dev/sr0 on /run/media/root/VMware Tools type iso9660 (ro,nosuid,nodev,relatime,uid=0,gid=0,iocharset=utf8,mode=0400,dmode=0500,uhelper=udisks2) [VMware Tools]\n/dev/sr1 on /run/media/Disk on C type NFS type iso9660 (ro,uid=0,gid=0,iocharset=utf8,uhelper=udisks2) [C type Disk]\n').strip()

def test_mount():
    results = Mount(context_wrap(MOUNT_DATA))
    assert results is not None
    assert len(results) == 13
    sr0 = results.search(filesystem='/dev/sr0')[0]
    sda1 = results.search(filesystem='/dev/sda1')[0]
    assert sr0 is not None
    assert sr0['mount_point'] == '/run/media/root/VMware Tools'
    assert sr0.get('mount_point') == '/run/media/root/VMware Tools'
    assert sr0.get('does not exist', 'failure') == 'failure'
    assert sr0['mount_type'] == 'iso9660'
    assert 'ro' in sr0['mount_options']
    assert sr0.mount_options.ro
    assert 'relatime' in sr0['mount_options']
    assert sr0['mount_options']['uhelper'] == 'udisks2'
    assert sr0['mount_label'] == '[VMware Tools]'
    assert sda1 is not None
    assert sda1['mount_point'] == '/boot'
    assert sda1['mount_type'] == 'ext4'
    assert 'rw' in sda1['mount_options']
    assert 'seclabel' in sda1['mount_options']
    assert sda1['mount_options']['data'] == 'ordered'
    assert sda1.mount_options.data == 'ordered'
    assert 'mount_label' not in sda1
    for mnt in results:
        assert hasattr(mnt, 'filesystem')
        assert hasattr(mnt, 'mount_point')
        assert hasattr(mnt, 'mount_type')
        assert hasattr(mnt, 'mount_options')

    assert results[12] == sr0
    assert results['/etc/shadow'] == results[11]
    with pytest.raises(TypeError) as (exc):
        assert results[set([1, 2, 3])] is None
    assert 'Mounts can only be indexed by mount string or line number' in str(exc)
    assert results.mounts['/run/media/root/VMware Tools'] == sr0
    assert results.get_dir('/run/media/root/VMware Tools') == sr0
    assert results.get_dir('/boot/grub2/grub.cfg') == sda1
    assert results.get_dir('/etc') == results['/']
    assert results.get_dir('relative/paths/fail') is None
    assert results.search(filesystem='/dev/sr0') == [sr0]
    assert results.search(mount_type='tmpfs') == [ results.rows[n] for n in (0, 7,
                                                                             8) ]
    assert results.search(mount_options__contains='seclabel') == [ results.rows[n] for n in (0,
                                                                                             1,
                                                                                             3,
                                                                                             4,
                                                                                             5,
                                                                                             7,
                                                                                             8,
                                                                                             11) ]
    return


def test_mount_with_special_mnt_point():
    results = Mount(context_wrap(MOUNT_DATA_WITH_SPECIAL_MNT_POINT))
    assert len(results) == 6
    sr0 = results.search(filesystem='/dev/sr0')[0]
    sr1 = results.search(filesystem='/dev/sr1')[0]
    assert sr0['mount_point'] == '/run/media/root/VMware Tools'
    assert sr1['mount_point'] == '/run/media/Disk on C type NFS'
    assert sr0.get('mount_label') == '[VMware Tools]'
    assert sr1.get('mount_label') == '[C type Disk]'
    assert results['/run/media/Disk on C type NFS'].get('mount_label') == '[C type Disk]'


def test_mount_exception1():
    with pytest.raises(ParseException) as (pe):
        Mount(context_wrap(MOUNT_ERR_DATA))
    assert 'Unable to parse' in str(pe.value)


def test_mount_exception2():
    with pytest.raises(ParseException) as (exc):
        Mount(context_wrap(MOUNT_WITHOUT_ROOT))
    assert "Input for mount must contain '/' mount point." in str(exc)


def test_proc_mount():
    results = ProcMounts(context_wrap(PROC_MOUNT))
    assert results is not None
    assert len(results) == 19
    sda1 = results.search(filesystem='/dev/sda1')[0]
    assert sda1 is not None
    assert sda1['mount_point'] == '/boot'
    assert sda1['mount_type'] == 'ext4'
    assert 'rw' in sda1['mount_options']
    assert 'relatime' in sda1['mount_options']
    assert sda1['mount_options']['data'] == 'ordered'
    assert sda1.mount_options.data == 'ordered'
    assert sda1['mount_label'] == ['0', '0']
    for mnt in results:
        assert hasattr(mnt, 'filesystem')
        assert hasattr(mnt, 'mount_point')
        assert hasattr(mnt, 'mount_type')
        assert hasattr(mnt, 'mount_options')

    assert results[7] == sda1
    assert results['/misc'] == results[(-1)]
    with pytest.raises(TypeError) as (exc):
        assert results[set([1, 2, 3])] is None
    assert 'Mounts can only be indexed by mount string or line number' in str(exc)
    assert results.mounts['/boot'] == sda1
    assert results.get_dir('/var/lib/nfs/rpc_pipefs') == results.search(filesystem='sunrpc')[0]
    assert results.get_dir('/etc') == results['/']
    assert results.search(filesystem='/dev/sda1') == [sda1]
    assert results.search(mount_type='nfs') == [ results.rows[n] for n in (16, 17) ]
    assert results.search(mount_options__contains='mode') == [ results.rows[n] for n in (2,
                                                                                         3) ]
    return


def test_proc_mount_exception1():
    with pytest.raises(SkipException) as (e):
        ProcMounts(context_wrap(PROC_EXCEPTION1))
    assert 'Empty content' in str(e)


def test_proc_mount_exception2():
    with pytest.raises(ParseException) as (e):
        ProcMounts(context_wrap(PROC_EXCEPTION2))
    assert "Input for mount must contain '/' mount point." in str(e)


def test_proc_mount_exception3():
    with pytest.raises(ParseException) as (pe):
        ProcMounts(context_wrap(PROCMOUNT_ERR_DATA))
    assert 'Unable to parse' in str(pe.value)


def test_doc_examples():
    env = {'mnt_info': Mount(context_wrap(MOUNT_DOC)), 
       'proc_mnt_info': ProcMounts(context_wrap(PROC_MOUNT_DOC)), 
       'mounts': Mount(context_wrap(MOUNT_DOC))}
    failed, total = doctest.testmod(mount, globs=env)
    assert failed == 0