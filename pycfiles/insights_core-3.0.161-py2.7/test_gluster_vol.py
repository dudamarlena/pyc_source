# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_gluster_vol.py
# Compiled at: 2019-12-13 11:35:35
import pytest, doctest
from insights.parsers import ParseException, gluster_vol
from insights.tests import context_wrap
from insights.parsers.gluster_vol import GlusterVolInfo, GlusterVolStatus
TRACKING_VALID = '\n\nVolume Name: test_vol\nType: Replicate\ncluster.choose-local: off\nnetwork.remote-dio: enable\nperformance.low-prio-threads: 32\nperformance.io-cache: off\nperformance.read-ahead: off\nperformance.quick-read: off\nnfs.disable: on\nperformance.client-io-threads: off\n'
TRACKING_INVALID = ' '
MULTIPLE_VOLUMES = ('\nVolume Name: test_vol\nType: Replicate\nVolume ID: 2c32ed8d-5a07-4a76-a73a-123859556974\nStatus: Started\nSnapshot Count: 0\nNumber of Bricks: 1 x 3 = 3\nTransport-type: tcp\nBricks:\nBrick1: 172.17.18.42:/home/brick\nBrick2: 172.17.18.43:/home/brick\nBrick3: 172.17.18.44:/home/brick\nOptions Reconfigured:\ncluster.choose-local: off\nuser.cifs: off\nfeatures.shard: on\ncluster.shd-wait-qlength: 10000\ncluster.shd-max-threads: 8\ncluster.locking-scheme: granular\ncluster.data-self-heal-algorithm: full\ncluster.server-quorum-type: server\ncluster.quorum-type: auto\ncluster.eager-lock: enable\nnetwork.remote-dio: enable\nperformance.low-prio-threads: 32\nperformance.io-cache: off\nperformance.read-ahead: off\nperformance.quick-read: off\ntransport.address-family: inet\nnfs.disable: on\nperformance.client-io-threads: off\n\nVolume Name: test_vol_2\nType: Replicate\nVolume ID: dd821df9-ee2e-429c-98a0-81b1b794433d\nStatus: Started\nSnapshot Count: 0\nNumber of Bricks: 1 x 3 = 3\nTransport-type: tcp\nBricks:\nBrick1: 172.17.18.42:/home/brick2\nBrick2: 172.17.18.43:/home/brick2\nBrick3: 172.17.18.44:/home/brick2\nOptions Reconfigured:\ncluster.choose-local: off\nuser.cifs: off\nfeatures.shard: on\ncluster.shd-wait-qlength: 10000\ncluster.shd-max-threads: 8\ncluster.locking-scheme: granular\ncluster.data-self-heal-algorithm: full\ncluster.server-quorum-type: server\ncluster.quorum-type: auto\ncluster.eager-lock: enable\nnetwork.remote-dio: enable\nperformance.low-prio-threads: 32\nperformance.io-cache: off\nperformance.read-ahead: off\nperformance.quick-read: off\ntransport.address-family: inet\nnfs.disable: on\nperformance.client-io-threads: off\n').strip()

def test_gluster_vol_info_invalid():
    with pytest.raises(ParseException) as (e):
        GlusterVolInfo(context_wrap(TRACKING_INVALID))
    assert 'Unable to parse gluster volume options: []' in str(e)


def test_gluster_volume_options():
    parser_result = GlusterVolInfo(context_wrap(TRACKING_VALID))
    assert parser_result is not None
    data = parser_result.data['test_vol']
    assert data['network.remote-dio'] == 'enable'
    assert data['cluster.choose-local'] == 'off'
    assert data['performance.client-io-threads'] == 'off'
    assert data['performance.quick-read'] == 'off'
    assert data['performance.low-prio-threads'] == '32'
    assert data['performance.io-cache'] == 'off'
    assert data['performance.read-ahead'] == 'off'
    assert data['nfs.disable'] == 'on'
    return


def test_gluster_multiple_volume_options():
    parser_result = GlusterVolInfo(context_wrap(MULTIPLE_VOLUMES))
    assert parser_result is not None
    data = parser_result.data['test_vol']
    assert data['network.remote-dio'] == 'enable'
    assert data['cluster.choose-local'] == 'off'
    assert data['performance.client-io-threads'] == 'off'
    assert data['performance.quick-read'] == 'off'
    assert data['performance.low-prio-threads'] == '32'
    assert data['performance.io-cache'] == 'off'
    assert data['performance.read-ahead'] == 'off'
    assert data['nfs.disable'] == 'on'
    data = parser_result.data['test_vol_2']
    assert data['network.remote-dio'] == 'enable'
    assert data['cluster.choose-local'] == 'off'
    assert data['performance.client-io-threads'] == 'off'
    assert data['performance.quick-read'] == 'off'
    assert data['performance.low-prio-threads'] == '32'
    assert data['performance.io-cache'] == 'off'
    assert data['performance.read-ahead'] == 'off'
    assert data['nfs.disable'] == 'on'
    return


VOL_STATUS_BAD = ('\n').strip()
VOL_STATUS_GOOD = ('\nStatus of volume: test_vol\nGluster process                             TCP Port  RDMA Port  Online  Pid\n------------------------------------------------------------------------------\nBrick 172.17.18.42:/home/brick              49152     0          Y       26685\nBrick 172.17.18.43:/home/brick              49152     0          Y       27094\nBrick 172.17.18.44:/home/brick              49152     0          Y       27060\nSelf-heal Daemon on localhost               N/A       N/A        Y       7805\nSelf-heal Daemon on 172.17.18.44            N/A       N/A        Y       33400\nSelf-heal Daemon on 172.17.18.43            N/A       N/A        Y       33680\n\nTask Status of Volume test_vol\n------------------------------------------------------------------------------\nThere are no active volume tasks\n').strip()
VOL_STATUS_MULTIPLE_GOOD = ('\nStatus of volume: test_vol\nGluster process                             TCP Port  RDMA Port  Online  Pid\n------------------------------------------------------------------------------\nBrick 172.17.18.42:/home/brick              49152     0          Y       26685\nBrick 172.17.18.43:/home/brick              49152     0          Y       27094\nBrick 172.17.18.44:/home/brick              49152     0          Y       27060\nSelf-heal Daemon on localhost               N/A       N/A        Y       7805\nSelf-heal Daemon on 172.17.18.44            N/A       N/A        Y       33400\nSelf-heal Daemon on 172.17.18.43            N/A       N/A        Y       33680\n\nTask Status of Volume test_vol\n------------------------------------------------------------------------------\nThere are no active volume tasks\n\n\nStatus of volume: test_vol_2\nGluster process                             TCP Port  RDMA Port  Online  Pid\n------------------------------------------------------------------------------\nBrick 172.17.18.42:/home/brick              49152     0          Y       6685\nBrick 172.17.18.43:/home/brick              49152     0          Y       33094\nBrick 172.17.18.44:/home/brick              49152     0          Y       2060\nSelf-heal Daemon on localhost               N/A       N/A        Y       7805\nSelf-heal Daemon on 172.17.18.44            N/A       N/A        Y       33400\nSelf-heal Daemon on 172.17.18.43            N/A       N/A        Y       33680\n\nTask Status of Volume test_vol\n------------------------------------------------------------------------------\nThere are no active volume tasks\n\n').strip()
MULTIPLE_VOL_STATUS_LONG_HOSTNAME = ('\nLocking failed on srvgluspvlsu72.example.com. Please check log file for details.\nAnother transaction is in progress for volQXCHISTP_data. Please try again after sometime.\n\nStatus of volume: volQXCHISTPI_log\nGluster process                             TCP Port  RDMA Port  Online  Pid\n------------------------------------------------------------------------------\nBrick srvgluspvlsu71.example.com:/gluster/Q\nXCHISTPI/log/brick                          49153     0          Y       11020\nBrick srvgluspvlsu72.example.com:/gluster/Q\nXCHISTPI/log/brick                          49153     0          Y       11182\nBrick srvgluspvlsu73.example.com:/gluster/Q\nXCHISTPI/log/brick                          49153     0          Y       129143\nSelf-heal Daemon on localhost               N/A       N/A        Y       130186\nSelf-heal Daemon on srvgluspvlsu71          N/A       N/A        Y       20009\nSelf-heal Daemon on srvgluspvlsu72.example.\ncom                                         N/A       N/A        Y       12300\n\nTask Status of Volume volQXCHISTPI_log\n------------------------------------------------------------------------------\nThere are no active volume tasks\n\nStatus of volume: volQXSCCINTP_data\nGluster process                             TCP Port  RDMA Port  Online  Pid\n------------------------------------------------------------------------------\nBrick srvgluspvlsu71.example.com:/gluster/Q\nXSCCINTP/data/brick                         49190     0          Y       11374\nBrick srvgluspvlsu72.example.com:/gluster/Q\nXSCCINTP/data/brick                         49190     0          Y       11524\nBrick srvgluspvlsu73.example.com:/gluster/Q\nXSCCINTP/data/bri                           49190     0          Y       129476\nSelf-heal Daemon on localhost               N/A       N/A        Y       130186\nSelf-heal Daemon on srvgluspvlsu71          N/A       N/A        Y       20009\nSelf-heal Daemon on srvgluspvlsu72.example.\ncom                                         N/A       N/A        Y       12300\n\nTask Status of Volume volQXSCCINTP_data\n------------------------------------------------------------------------------\nThere are no active volume tasks\n').strip()

def test_invalid():
    with pytest.raises(ParseException) as (e):
        GlusterVolStatus(context_wrap(VOL_STATUS_BAD))
    assert 'Unable to parse gluster volume status: []' in str(e)


def test_valid():
    parser_result = GlusterVolStatus(context_wrap(VOL_STATUS_GOOD))
    parser_data = parser_result.data
    assert list(parser_data.keys()) == ['test_vol']
    assert parser_data['test_vol'][0] == {'Gluster_process': 'Brick 172.17.18.42:/home/brick', 
       'RDMA_Port': '0', 
       'TCP_Port': '49152', 
       'Pid': '26685', 
       'Online': 'Y'}
    assert parser_data['test_vol'][1]['Online'] == 'Y'
    assert parser_data['test_vol'][1]['TCP_Port'] == '49152'
    assert parser_data['test_vol'][1]['Pid'] == '27094'
    assert parser_data['test_vol'][2] == {'Gluster_process': 'Brick 172.17.18.44:/home/brick', 
       'RDMA_Port': '0', 
       'TCP_Port': '49152', 
       'Pid': '27060', 
       'Online': 'Y'}
    assert parser_data['test_vol'][3] == {'Online': 'Y', 
       'TCP_Port': 'N/A', 
       'RDMA_Port': 'N/A', 
       'Pid': '7805', 
       'Gluster_process': 'Self-heal Daemon on localhost'}
    assert parser_data['test_vol'][4] == {'Online': 'Y', 
       'TCP_Port': 'N/A', 
       'RDMA_Port': 'N/A', 
       'Pid': '33400', 
       'Gluster_process': 'Self-heal Daemon on 172.17.18.44'}
    Self_heal_Daemon3_data = parser_data['test_vol'][5]
    assert Self_heal_Daemon3_data['RDMA_Port'] == 'N/A'


def test_multiple_valid():
    parser_result = GlusterVolStatus(context_wrap(VOL_STATUS_MULTIPLE_GOOD))
    parser_data = parser_result.data
    assert list(parser_data.keys()) == ['test_vol', 'test_vol_2']
    assert parser_data['test_vol_2'][0] == {'Gluster_process': 'Brick 172.17.18.42:/home/brick', 
       'RDMA_Port': '0', 
       'TCP_Port': '49152', 
       'Pid': '6685', 
       'Online': 'Y'}
    assert parser_data['test_vol_2'][1]['Online'] == 'Y'
    assert parser_data['test_vol_2'][1]['TCP_Port'] == '49152'
    assert parser_data['test_vol_2'][1]['Pid'] == '33094'
    assert parser_data['test_vol_2'][2] == {'Gluster_process': 'Brick 172.17.18.44:/home/brick', 
       'RDMA_Port': '0', 
       'TCP_Port': '49152', 
       'Pid': '2060', 
       'Online': 'Y'}
    assert parser_data['test_vol_2'][3] == {'Gluster_process': 'Self-heal Daemon on localhost', 
       'RDMA_Port': 'N/A', 
       'Pid': '7805', 
       'TCP_Port': 'N/A', 
       'Online': 'Y'}


def test_long_hostnames():
    result = GlusterVolStatus(context_wrap(MULTIPLE_VOL_STATUS_LONG_HOSTNAME))
    assert len(result.data) == 2
    assert len(result.data['volQXCHISTPI_log']) == 6
    assert len(result.data['volQXSCCINTP_data']) == 6
    assert result.data['volQXSCCINTP_data'][0]['Gluster_process'] == 'Brick srvgluspvlsu71.example.com:/gluster/QXSCCINTP/data/brick'


def test_doc():
    INFO = TRACKING_VALID
    STATUS = VOL_STATUS_GOOD
    env = {'parser_result_v_info': GlusterVolInfo(context_wrap(INFO)), 
       'parser_result_v_status': GlusterVolStatus(context_wrap(STATUS))}
    failed, total = doctest.testmod(gluster_vol, globs=env)
    assert failed == 0