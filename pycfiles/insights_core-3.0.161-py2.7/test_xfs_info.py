# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_xfs_info.py
# Compiled at: 2019-05-16 13:41:33
import pytest
from insights.parsers import xfs_info, ParseException
from insights.tests import context_wrap

def test_example_xfs_info():
    xfs_obj = xfs_info.XFSInfo(context_wrap('\nmeta-data=/dev/sda      isize=256    agcount=32, agsize=16777184 blks\n         =              sectsz=512   attr=2\ndata     =              bsize=4096   blocks=536869888, imaxpct=5\n         =              sunit=32     swidth=128 blks\nnaming   =version 2     bsize=4096\nlog      =internal      bsize=4096   blocks=32768, version=2\n         =              sectsz=512   sunit=32 blks, lazy-count=1\nrealtime =none          extsz=524288 blocks=0, rtextents=0\n    ', path='sos_commands/xfs/xfs_info_.'))
    xfs = xfs_obj.xfs_info
    assert 'meta-data' in xfs
    assert 'data' in xfs
    assert 'naming' in xfs
    assert 'log' in xfs
    assert 'realtime' in xfs
    assert xfs['meta-data']['specifier'] == '/dev/sda'
    assert xfs['naming']['specifier'] == 'version'
    assert xfs['naming']['specifier_value'] == '2'
    assert xfs['log']['specifier'] == 'internal'
    assert xfs['realtime']['specifier'] == 'none'
    assert xfs['meta-data']['isize'] == 256
    assert xfs['meta-data']['agcount'] == 32
    assert xfs['meta-data']['agsize'] == '16777184 blks'
    assert xfs['meta-data']['sectsz'] == 512
    assert xfs['meta-data']['attr'] == 2
    assert xfs['data']['bsize'] == 4096
    assert xfs['data']['blocks'] == 536869888
    assert xfs['data']['imaxpct'] == 5
    assert xfs['data']['sunit'] == 32
    assert xfs['data']['swidth'] == '128 blks'
    assert xfs['naming']['bsize'] == 4096
    assert xfs['log']['bsize'] == 4096
    assert xfs['log']['blocks'] == 32768
    assert xfs['log']['version'] == 2
    assert xfs['log']['sectsz'] == 512
    assert xfs['log']['sunit'] == '32 blks'
    assert xfs['log']['lazy-count'] == 1
    assert xfs['realtime']['extsz'] == 524288
    assert xfs['realtime']['blocks'] == 0
    assert xfs['realtime']['rtextents'] == 0
    assert xfs_obj.device == '/dev/sda'
    assert xfs_obj.data_size == 2199019061248
    assert xfs_obj.log_size == 134217728
    assert xfs_obj.mount == '/'


def test_root_xfs_info():
    xfs_obj = xfs_info.XFSInfo(context_wrap('\nmeta-data=/dev/mapper/vgSys-lvRoot isize=256    agcount=4, agsize=320000 blks\n         =                       sectsz=512   attr=2, projid32bit=1\n         =                       crc=0        finobt=0\ndata     =                       bsize=4096   blocks=1280000, imaxpct=25\n         =                       sunit=0      swidth=0 blks\nnaming   =version 2              bsize=4096   ascii-ci=0 ftype=0\nlog      =internal               bsize=4096   blocks=2560, version=2\n         =                       sectsz=512   sunit=0 blks, lazy-count=1\nrealtime =none                   extsz=4096   blocks=0, rtextents=0\n    ', path='sos_commands/xfs/xfs_info_.'))
    xfs = xfs_obj.xfs_info
    assert 'meta-data' in xfs
    assert 'data' in xfs
    assert 'naming' in xfs
    assert 'log' in xfs
    assert 'realtime' in xfs
    assert xfs['meta-data']['specifier'] == '/dev/mapper/vgSys-lvRoot'
    assert xfs['naming']['specifier'] == 'version'
    assert xfs['naming']['specifier_value'] == '2'
    assert xfs['log']['specifier'] == 'internal'
    assert xfs['realtime']['specifier'] == 'none'
    assert xfs['meta-data']['isize'] == 256
    assert xfs['meta-data']['agcount'] == 4
    assert xfs['meta-data']['agsize'] == '320000 blks'
    assert xfs['meta-data']['sectsz'] == 512
    assert xfs['meta-data']['attr'] == 2
    assert xfs['meta-data']['projid32bit'] == 1
    assert xfs['meta-data']['crc'] == 0
    assert xfs['meta-data']['finobt'] == 0
    assert xfs['data']['bsize'] == 4096
    assert xfs['data']['blocks'] == 1280000
    assert xfs['data']['imaxpct'] == 25
    assert xfs['data']['sunit'] == 0
    assert xfs['data']['swidth'] == '0 blks'
    assert xfs['naming']['bsize'] == 4096
    assert xfs['naming']['ascii-ci'] == 0
    assert xfs['naming']['ftype'] == 0
    assert xfs['log']['bsize'] == 4096
    assert xfs['log']['blocks'] == 2560
    assert xfs['log']['version'] == 2
    assert xfs['log']['sectsz'] == 512
    assert xfs['log']['sunit'] == '0 blks'
    assert xfs['log']['lazy-count'] == 1
    assert xfs['realtime']['extsz'] == 4096
    assert xfs['realtime']['blocks'] == 0
    assert xfs['realtime']['rtextents'] == 0
    assert xfs_obj.device == '/dev/mapper/vgSys-lvRoot'
    assert xfs_obj.data_size == 5242880000
    assert xfs_obj.log_size == 10485760
    assert xfs_obj.mount == '/'
    assert str(xfs_obj) == 'xfs_info of /dev/mapper/vgSys-lvRoot'


def test_ext_log_xfs_info():
    xfs_obj = xfs_info.XFSInfo(context_wrap('\nmeta-data=data.xfs.image         isize=256    agcount=4, agsize=65536 blks\n         =                       sectsz=512   attr=2, projid32bit=1\n         =                       crc=0        finobt=0\ndata     =                       bsize=4096   blocks=262144, imaxpct=25\n         =                       sunit=0      swidth=0 blks\nnaming   =version 2              bsize=4096   ascii-ci=0 ftype=0\nlog      =log.xfs.image          bsize=4096   blocks=25600, version=2\n         =                       sectsz=512   sunit=0 blks, lazy-count=1\nrealtime =none                   extsz=4096   blocks=0, rtextents=0\n    '))
    xfs = xfs_obj.xfs_info
    assert xfs['meta-data']['specifier'] == 'data.xfs.image'
    assert xfs['log']['specifier'] == 'log.xfs.image'
    assert xfs_obj.data_size == 1073741824
    assert xfs_obj.log_size == 104857600


def test_bad_xfs_info():
    for input_data, exception in [
     ('xfs_info: bad command or file name', "No 'meta-data' section found"),
     ('meta-data=         isize=256    agcount=4, agsize=65536 blks', 'Device specifier not found in meta-data'),
     ('meta-data=data.xfs.image         isize=256    agcount=4, agsize=65536 blks', "No 'data' section found"),
     ('\nmeta-data=data.xfs.image         isize=256    agcount=4, agsize=65536 blks\ndata     =                       sunit=0      swidth=0 blks\n         ',
 "'blocks' not defined in data section"),
     ('\nmeta-data=data.xfs.image         isize=256    agcount=4, agsize=65536 blks\ndata     =                       sunit=0      blocks=262144\n         ',
 "'bsize' not defined in data section"),
     ('\nmeta-data=data.xfs.image         isize=256    agcount=4, agsize=65536 blks\ndata     =                       bsize=4096   blocks=262144, imaxpct=25\n         ',
 "No 'log' section found"),
     ('\nmeta-data=data.xfs.image         isize=256    agcount=4, agsize=65536 blks\ndata     =                       bsize=4096   blocks=262144, imaxpct=25\nlog      =log.xfs.image          bsize=4096   sunit=0 blks, lazy-count=1\n         ',
 "'blocks' not defined in log section"),
     ('\nmeta-data=data.xfs.image         isize=256    agcount=4, agsize=65536 blks\ndata     =                       bsize=4096   blocks=262144, imaxpct=25\nlog      =log.xfs.image          sectsz=512   blocks=25600, version=2\n         ',
 "'bsize' not defined in log section")]:
        with pytest.raises(ParseException) as (e_info):
            xfs_info.XFSInfo(context_wrap(input_data))
        assert exception in str(e_info.value)