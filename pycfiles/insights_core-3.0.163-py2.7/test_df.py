# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_df.py
# Compiled at: 2020-04-16 14:56:28
import pytest, doctest
from insights.parsers import df, ParseException
from insights.tests import context_wrap
DF_LI = ('\nFilesystem        Inodes  IUsed     IFree IUse% Mounted on\n/dev/mapper/vg_lxcrhel6sat56-lv_root\n\n                 6275072 124955   6150117    2% /\n\ndevtmpfs         1497120    532   1496588    1% /dev\ntmpfs            1499684    331   1499353    1% /dev/shm\ntmpfs            1499684    728   1498956    1% /run\ntmpfs            1499684     16   1499668    1% /sys/fs/cgroup\ntmpfs            1499684     54   1499630    1% /tmp\n/dev/sda2      106954752 298662 106656090    1% /home\n/dev/sda1         128016    429    127587    1% /boot\n/dev/sdb1        1499684      6   1499678    1% /V M T o o l s\n/dev/sdb2        1499684     15   1499669    1% /VM Tools\n').strip()

def test_df_li():
    df_list = df.DiskFree_LI(context_wrap(DF_LI))
    assert len(df_list) == 10
    assert len(df_list.mounts) == 10
    assert len(df_list.filesystems) == 7
    assert '/home' in df_list.mounts
    r = df.Record(filesystem='/dev/sda2', total='106954752', used='298662', available='106656090', capacity='1%', mounted_on='/home')
    assert df_list.get_mount('/home') == r
    assert '/dev/sda2' in df_list.filesystems
    assert len(df_list.get_filesystem('/dev/sda2')) == 1
    assert df_list.get_filesystem('/dev/sda2')[0] == r
    assert len(df_list.get_filesystem('tmpfs')) == 4
    assert df_list.get_mount('/dev').filesystem == 'devtmpfs'
    assert df_list.get_mount('/run').total == '1499684'
    assert df_list.get_mount('/tmp').used == '54'
    assert df_list.get_mount('/boot').available == '127587'
    assert df_list.get_filesystem('/dev/sda2')[0].capacity == '1%'
    assert df_list.get_filesystem('/dev/sda2')[0].available == '106656090'
    assert df_list.get_filesystem('devtmpfs')[0].mounted_on == '/dev'
    assert df_list.get_mount('/V M T o o l s').available == '1499678'
    assert df_list.get_filesystem('/dev/mapper/vg_lxcrhel6sat56-lv_root')[0].mounted_on == '/'
    sorted_mount_names = sorted([
     '/', '/dev', '/dev/shm', '/run', '/sys/fs/cgroup', '/tmp', '/home',
     '/boot', '/V M T o o l s', '/VM Tools'])
    assert sorted([ d.mounted_on for d in df_list ]) == sorted_mount_names
    assert sorted(df_list.mount_names) == sorted_mount_names
    assert sorted(df_list.filesystem_names) == sorted([
     '/dev/mapper/vg_lxcrhel6sat56-lv_root', 'devtmpfs', 'tmpfs',
     '/dev/sda2', '/dev/sda1', '/dev/sdb2', '/dev/sdb1'])
    assert df_list.get_dir('/') == df_list.get_mount('/')
    assert df_list.get_dir('/dev') == df_list.get_mount('/dev')
    assert df_list.get_dir('/boot/grub2') == df_list.get_mount('/boot')
    assert df_list.get_dir('/boot/grub2/') == df_list.get_mount('/boot')
    assert df_list.get_dir('/boot/grub2/grub.cfg') == df_list.get_mount('/boot')
    assert df_list.get_dir('var/lib') is None
    assert df_list.get_dir('"') is None
    return


DF_ALP = ("\n/bin/df: '/vobs/GEMS': No such file or directory\n/bin/df: '/vobs/NT/TFax': No such file or directory\nFilesystem                           1024-blocks      Used Available Capacity Mounted on\n/dev/mapper/vg_lxcrhel6sat56-lv_root    98571884   4244032  89313940       5% /\nsysfs                                          0         0         0        - /sys\nproc                                           0         0         0        - /proc\ndevtmpfs                                 5988480         0   5988480       0% /dev\nsecurityfs                                     0         0         0        - /sys/kernel/security\ntmpfs                                    5998736    491660   5507076       9% /dev/shm\ndevpts                                         0         0         0        - /dev/pts\ntmpfs                                    5998736      1380   5997356       1% /run\n\ntmpfs                                    5998736         0   5998736       0% /sys/fs/cgroup\n").strip()

def test_df_alP():
    df_list = df.DiskFree_ALP(context_wrap(DF_ALP))
    assert len(df_list) == 9
    assert len(df_list.mounts) == 9
    assert len(df_list.filesystems) == 7
    assert '/' in df_list.mounts
    r = df.Record(filesystem='/dev/mapper/vg_lxcrhel6sat56-lv_root', total='98571884', used='4244032', available='89313940', capacity='5%', mounted_on='/')
    assert df_list.get_mount('/') == r
    assert '/dev/mapper/vg_lxcrhel6sat56-lv_root' in df_list.filesystems
    assert len(df_list.get_filesystem('/dev/mapper/vg_lxcrhel6sat56-lv_root')) == 1
    assert df_list.get_filesystem('/dev/mapper/vg_lxcrhel6sat56-lv_root')[0] == r
    assert len(df_list.get_filesystem('tmpfs')) == 3
    assert df_list.get_mount('/sys').filesystem == 'sysfs'
    assert df_list.get_mount('/proc').total == '0'
    assert df_list.get_mount('/dev').used == '0'
    assert df_list.get_mount('/run').available == '5997356'
    assert df_list.get_mount('/sys/fs/cgroup').capacity == '0%'
    assert df_list.get_mount('/').filesystem == '/dev/mapper/vg_lxcrhel6sat56-lv_root'
    assert df_list.get_mount('/').capacity == '5%'
    assert df_list.get_dir('/') == df_list.get_mount('/')
    assert df_list.get_dir('/dev') == df_list.get_mount('/dev')
    assert df_list.get_dir('/dev/v4l') == df_list.get_mount('/dev')
    assert df_list.get_dir('/dev/v4l/') == df_list.get_mount('/dev')
    assert df_list.get_dir('/dev/v4l/adapter0/control0.cfg') == df_list.get_mount('/dev')
    assert df_list.get_dir('dev/sys') is None
    assert df_list.get_dir('"') is None
    return


DF_AL = ('\nFilesystem                             1K-blocks      Used Available     Use% Mounted on\n/dev/mapper/vg_lxcrhel6sat56-lv_root    98571884   4244032  89313940       5% /\nsysfs                                          0         0         0        - /sys\nproc                                           0         0         0        - /proc\ndevtmpfs                                 5988480         0   5988480       0% /dev\nsecurityfs                                     0         0         0        - /sys/kernel/security\n\ntmpfs                                    5998736    491660   5507076       9% /dev/shm\ndevpts                                         0         0         0        - /dev/pts\ntmpfs                                    5998736      1380   5997356       1% /run\ntmpfs                                    5998736         0   5998736       0% /sys/fs/cgroup\n').strip()

def test_df_al():
    df_list = df.DiskFree_AL(context_wrap(DF_AL))
    assert len(df_list) == 9
    assert len(df_list.mounts) == 9
    assert len(df_list.filesystems) == 7
    assert '/' in df_list.mounts
    r = df.Record(filesystem='/dev/mapper/vg_lxcrhel6sat56-lv_root', total='98571884', used='4244032', available='89313940', capacity='5%', mounted_on='/')
    assert df_list.get_mount('/') == r
    assert '/dev/mapper/vg_lxcrhel6sat56-lv_root' in df_list.filesystems
    assert len(df_list.get_filesystem('/dev/mapper/vg_lxcrhel6sat56-lv_root')) == 1
    assert df_list.get_filesystem('/dev/mapper/vg_lxcrhel6sat56-lv_root')[0] == r
    assert len(df_list.get_filesystem('tmpfs')) == 3
    assert df_list.get_mount('/sys').filesystem == 'sysfs'
    assert df_list.get_mount('/proc').total == '0'
    assert df_list.get_mount('/dev').used == '0'
    assert df_list.get_mount('/run').available == '5997356'
    assert df_list.get_mount('/sys/fs/cgroup').capacity == '0%'
    assert df_list.get_mount('/').filesystem == '/dev/mapper/vg_lxcrhel6sat56-lv_root'
    assert df_list.get_mount('/').capacity == '5%'
    assert df_list.get_dir('/') == df_list.get_mount('/')
    assert df_list.get_dir('/dev') == df_list.get_mount('/dev')
    assert df_list.get_dir('/dev/v4l') == df_list.get_mount('/dev')
    assert df_list.get_dir('/dev/v4l/') == df_list.get_mount('/dev')
    assert df_list.get_dir('/dev/v4l/adapter0/control0.cfg') == df_list.get_mount('/dev')
    assert df_list.get_dir('dev/sys') is None
    assert df_list.get_dir('"') is None
    return


DF_AL_BAD = '\nFilesystem                             1K-blocks      Used Available     Use% Mounted on\n/dev/mapper/vg_lxcrhel6sat56-lv_root    98571884   4244032  89313940       5% /\nsysfs                                          0\n'
DF_AL_BAD_BS = '\nFilesystem                             1a-blocks      Used Available     Use% Mounted on\n/dev/mapper/vg_lxcrhel6sat56-lv_root    98571884   4244032  89313940       5% /\n'

def test_df_al_bad():
    with pytest.raises(ParseException) as (exc):
        df_list = df.DiskFree_AL(context_wrap(DF_AL_BAD))
        assert len(df_list) == 2
    assert 'Could not parse line' in str(exc)
    with pytest.raises(ParseException) as (exc):
        df_list = df.DiskFree_AL(context_wrap(DF_AL_BAD_BS))
    assert 'Unknown block size' in str(exc)


DF_AL_BS_2MB = '\nFilesystem     2MB-blocks  Used Available Use% Mounted on\n/dev/vda3           62031 49197      9680  84% /\n'

def test_df_al_2MB():
    df_list = df.DiskFree_LI(context_wrap(DF_AL_BS_2MB))
    root = df_list.get_mount('/')
    assert root.filesystem == '/dev/vda3'
    assert root.total == '62031'
    assert df_list.raw_block_size == '2MB'
    assert df_list.block_size == 2000000
    assert int(root.total) * df_list.block_size == 124062000000


DF_LI_DOC = ('\nFilesystem       Inodes IUsed    IFree IUse% Mounted on\ndevtmpfs         242224   359   241865    1% /dev\ntmpfs            246028     1   246027    1% /dev/shm\ntmpfs            246028   491   245537    1% /run\ntmpfs            246028    17   246011    1% /sys/fs/cgroup\n/dev/sda2       8911872 58130  8853742    1% /\n/dev/sdb1      26213888 19662 26194226    1% /opt/data\n/dev/sda1        524288   306   523982    1% /boot\ntmpfs            246028     5   246023    1% /run/user/0\n').strip()
DF_ALP_DOC = ('\nFilesystem     1024-blocks    Used Available Capacity Mounted on\nsysfs                    0       0         0        - /sys\nproc                     0       0         0        - /proc\ndevtmpfs            968896       0    968896       0% /dev\nsecurityfs               0       0         0        - /sys/kernel/security\ntmpfs               984112       0    984112       0% /dev/shm\ndevpts                   0       0         0        - /dev/pts\ntmpfs               984112    8660    975452       1% /run\ntmpfs               984112       0    984112       0% /sys/fs/cgroup\ncgroup                   0       0         0        - /sys/fs/cgroup/systemd\ncgroup                   0       0         0        - /sys/fs/cgroup/pids\ncgroup                   0       0         0        - /sys/fs/cgroup/rdma\nconfigfs                 0       0         0        - /sys/kernel/config\n/dev/sda2         17813504 2127172  15686332      12% /\nselinuxfs                0       0         0        - /sys/fs/selinux\nsystemd-1                -       -         -        - /proc/sys/fs/binfmt_misc\ndebugfs                  0       0         0        - /sys/kernel/debug\nmqueue                   0       0         0        - /dev/mqueue\nhugetlbfs                0       0         0        - /dev/hugepages\n/dev/sdb1         52402180 1088148  51314032       3% /V M T o o l s\n/dev/sda1          1038336  185676    852660      18% /boot\n').strip()
DF_AL_DOC = ('\nFilesystem     1K-blocks    Used Available Use% Mounted on\nsysfs                  0       0         0    - /sys\nproc                   0       0         0    - /proc\ndevtmpfs          968896       0    968896   0% /dev\nsecurityfs             0       0         0    - /sys/kernel/security\ntmpfs             984112       0    984112   0% /dev/shm\ndevpts                 0       0         0    - /dev/pts\ntmpfs             984112    8660    975452   1% /run\ntmpfs             984112       0    984112   0% /sys/fs/cgroup\ncgroup                 0       0         0    - /sys/fs/cgroup/systemd\ncgroup                 0       0         0    - /sys/fs/cgroup/pids\ncgroup                 0       0         0    - /sys/fs/cgroup/rdma\nconfigfs               0       0         0    - /sys/kernel/config\n/dev/sda2       17813504 2127172  15686332  12% /\nselinuxfs              0       0         0    - /sys/fs/selinux\nsystemd-1              -       -         -    - /proc/sys/fs/binfmt_misc\ndebugfs                0       0         0    - /sys/kernel/debug\nmqueue                 0       0         0    - /dev/mqueue\nhugetlbfs              0       0         0    - /dev/hugepages\n/dev/sdb1       52402180 1088148  51314032   3% /V M T o o l s\n/dev/sda1        1038336  185676    852660  18% /boot\n').strip()

def test_doc_examples():
    env = {'df_li': df.DiskFree_LI(context_wrap(DF_LI_DOC)), 
       'df_al': df.DiskFree_AL(context_wrap(DF_AL_DOC)), 
       'df_alP': df.DiskFree_ALP(context_wrap(DF_ALP_DOC))}
    failed, total = doctest.testmod(df, globs=env)
    assert failed == 0