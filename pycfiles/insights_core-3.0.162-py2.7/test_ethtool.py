# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_ethtool.py
# Compiled at: 2019-11-14 13:57:46
import pytest, re
from insights.tests import context_wrap
from insights.parsers import ethtool, ParseException
from insights.util import keys_in
import doctest
TEST_ETHTOOL_A_DOCS = '\nPause parameters for eth0:\nAutonegotiate:  on\nRX:             on\nTX:             on\nRX negotiated:  off\nTX negotiated:  off\n'
SUCCESS_ETHTOOL_A = ('\nPause parameters for enp0s25:\nAutonegotiate : on\nRX:             off\nTX:             off\nRX negotiated:  off\nTX negotiated:  off\n').strip()
SUCCESS_ETHTOOL_A_PATH = ('\nsos_commands/networking/ethtool_-a_enp0s25\n').strip()
FAIL_ETHTOOL_A = ('\nCannot get device pause settings: Operation not supported\nPause parameters for __wlp3s0:\n').strip()
FAIL_ETHTOOL_A_PATH = ('\nsos_commands/networking/ethtool_-a___wlp3s0\n').strip()
FAIL_ETHTOOL_A_1 = ('\nethtool: bad command line argument(s)\nFor more information run ethtool -h\n').strip()
FAIL_ETHTOOL_A_PATH_1 = ('\nsos_commands/networking/ethtool_-a_bond0.1384@bond0\n').strip()
FAIL_ETHTOOL_A_2 = ('\nethtool version 6\nUsage:\nethtool DEVNAME Display standard information about device\n    ethtool -s|--change DEVNAME\n').strip()
FAIL_ETHTOOL_A_PATH_2 = ('\nsos_commands/networking/ethtool_-a_g_bond2\n').strip()
SUCCESS_ETHTOOL_A_BLANK_LINE = ('\nPause parameters for enp0s25:\n\nAutonegotiate : on\nRX:             off\nTX:             off\nRX negotiated:  off\nTX negotiated:  off\n').strip()

def test_ethtool_a():
    context = context_wrap(SUCCESS_ETHTOOL_A, path=SUCCESS_ETHTOOL_A_PATH)
    result = ethtool.Pause(context)
    assert result.ifname == 'enp0s25'
    assert result.autonegotiate
    assert not result.rx
    assert not result.tx
    assert not result.rx_negotiated
    assert not result.tx_negotiated


def test_ethtool_a_1():
    context = context_wrap(FAIL_ETHTOOL_A, path=FAIL_ETHTOOL_A_PATH)
    result = ethtool.Pause(context)
    assert result.ifname == '__wlp3s0'
    assert not result.autonegotiate


def test_ethtool_a_2():
    context = context_wrap(FAIL_ETHTOOL_A_1, path=FAIL_ETHTOOL_A_PATH_1)
    result = ethtool.Pause(context)
    assert result.ifname == 'bond0.1384@bond0'


def test_ethtool_a_3():
    context = context_wrap(FAIL_ETHTOOL_A_2, path=FAIL_ETHTOOL_A_PATH_2)
    result = ethtool.Pause(context)
    assert result.ifname == 'g_bond2'


def test_ethtool_a_blank_line():
    context = context_wrap(SUCCESS_ETHTOOL_A_BLANK_LINE, path=SUCCESS_ETHTOOL_A_PATH)
    result = ethtool.Pause(context)
    assert result.ifname == 'enp0s25'


TEST_ETHTOOL_C_DOCS = '\nCoalesce parameters for eth0:\nAdaptive RX: off  TX: off\nstats-block-usecs: 0\nsample-interval: 0\npkt-rate-low: 0\npkt-rate-high: 0\n\nrx-usecs: 20\nrx-frames: 5\nrx-usecs-irq: 0\nrx-frames-irq: 5\n\ntx-usecs: 72\ntx-frames: 53\ntx-usecs-irq: 0\ntx-frames-irq: 5\n\nrx-usecs-low: 0\nrx-frame-low: 0\ntx-usecs-low: 0\ntx-frame-low: 0\n\nrx-usecs-high: 0\nrx-frame-high: 0\ntx-usecs-high: 0\ntx-frame-high: 0\n'
TEST_ETHTOOL_C = ('\nCoalesce parameters for eth2:\nAdaptive RX: off  TX: off\npkt-rate-high: 10\n\ntx-usecs-irq: 0\ntx-frame-low: 25\n\ntx-usecs-high: 0\ntx-frame-high: 0\n\n').strip()
TEST_ETHTOOL_C_PATH = 'sos_commands/networking/ethtool_-c_eth2'
TEST_ETHTOOL_C_CANNOT_GET = ('\nCannot get device coalesce settings: Operation not supported\nCoalesce parameters for usb0:\n').strip()
TEST_ETHTOOL_C_BAD_ARGS = '\nethtool: bad command line argument(s)\nFor more information run ethtool -h\n'
TEST_ETHTOOL_C_SHORT = ('\nCoalesce parameters for eth2:\n').strip()

def test_get_ethtool_c():
    context = context_wrap(TEST_ETHTOOL_C)
    context.path = TEST_ETHTOOL_C_PATH
    result = ethtool.CoalescingInfo(context)
    assert keys_in(['adaptive-rx', 'adaptive-tx', 'pkt-rate-high',
     'tx-usecs-irq', 'tx-frame-low', 'tx-usecs-high', 'tx-frame-high'], result.data)
    assert result.ifname == 'eth2'
    assert not result.adaptive_rx
    assert not result.adaptive_tx
    assert result.pkt_rate_high == 10
    assert result.tx_usecs_irq == 0
    assert result.tx_frame_low == 25
    assert result.tx_usecs_high == 0
    assert result.tx_frame_high == 0


def test_get_ethtool_c_cannot_get():
    context = context_wrap(TEST_ETHTOOL_C_CANNOT_GET)
    context.path = 'sos_commands/networking/ethtool_-c_usb0'
    result = ethtool.CoalescingInfo(context)
    assert result.ifname == 'usb0'


def test_get_ethtool_c_bad_args():
    context = context_wrap(TEST_ETHTOOL_C_BAD_ARGS, path='sos_commands/networking/ethtool_-c_eth0')
    result = ethtool.CoalescingInfo(context)
    assert result.ifname == 'eth0'


def test_get_ethtool_c_short():
    context = context_wrap(TEST_ETHTOOL_C_SHORT, path=TEST_ETHTOOL_C_PATH)
    with pytest.raises(ParseException) as (exc):
        ethtool.CoalescingInfo(context)
    assert 'Command output missing value data' in str(exc)


TEST_ETHTOOL_G_DOCS = '\nRing parameters for eth0:\nPre-set maximums:\nRX:             2047\nRX Mini:        0\nRX Jumbo:       0\nTX:             511\nCurrent hardware settings:\nRX:             200\nRX Mini:        0\nRX Jumbo:       0\nTX:             511\n'
TEST_ETHTOOL_G = ('\nRing parameters for eth2:\nPre-set maximums:\nRX:     2047\nRX Mini:    0\nRX Jumbo:   0\nTX:     511\n\nCurrent hardware settings:\nRX:     200\nRX Mini:    0\nRX Jumbo:   0\nTX:     511\n\n\n').strip()
TEST_ETHTOOL_G_PATH = ('\nsos_commands/networking/ethtool_-g_eth2\n').strip()
TEST_ETHTOOL_G_1 = '\nCannot get device ring settings: No such device\nRing parameters for bond0.102@bond0:\n\n'
TEST_ETHTOOL_G_PATH_1 = '\nsos-command/neworking/ethtool_-g_bond2.102@bond2\n'
TEST_ETHTOOL_G_2 = '\nethtool: bad command line argument(s)\nFor more information run ethtool -h\n'
TEST_ETHTOOL_G_PATH_2 = '\nsos_commands/networkking/ethtool_-g_eth2\n'

def test_ethtool_g():
    context = context_wrap(TEST_ETHTOOL_G)
    context.path = TEST_ETHTOOL_G_PATH
    result = ethtool.Ring(context)
    assert keys_in(['max', 'current'], result.data)
    assert result.ifname == 'eth2'
    assert result.data['max'].rx == 2047
    assert result.data['max'].rx_mini == 0
    assert result.data['max'].rx_jumbo == 0
    assert result.data['max'].tx == 511
    assert result.max.rx == 2047
    assert result.max.rx_mini == 0
    assert result.max.rx_jumbo == 0
    assert result.max.tx == 511
    assert result.current.rx == 200
    assert result.current.rx_mini == 0
    assert result.current.rx_jumbo == 0
    assert result.current.tx == 511


def test_ethtool_g_1():
    context = context_wrap(TEST_ETHTOOL_G_1)
    context.path = TEST_ETHTOOL_G_PATH_1
    result = ethtool.Ring(context)
    assert result.ifname == 'bond0.102@bond0'


def test_ethtool_g_2():
    context = context_wrap(TEST_ETHTOOL_G_2, path=TEST_ETHTOOL_G_PATH_2)
    result = ethtool.Ring(context)
    assert result.ifname == 'eth2'


TEST_ETHTOOL_I_DOCS = '\ndriver: bonding\nversion: 3.6.0\nfirmware-version: 2\nbus-info:\nsupports-statistics: no\nsupports-test: no\nsupports-eeprom-access: no\nsupports-register-dump: no\nsupports-priv-flags: no\n'
TEST_ETHTOOL_I_GOOD = '\ndriver: virtio_net\nversion: 1.0.0\nfirmware-version:\nbus-info: 0000:00:03.0\nsupports-statistics: no\nsupports-test: no\nsupports-eeprom-access: no\nsupports-register-dump: no\nsupports-priv-flags: no\n'
TEST_ETHTOOL_I_MISSING_KEYS = '\ndriver: virtio_net\nfirmware-version:\nbus-info: 0000:00:03.0\nsupports-statistics: no\nsupports-test: no\nsupports-eeprom-access: no\nsupports-register-dump: no\nsupports-priv-flags: no\nsomething without a colon here is ignored\n'

def test_good():
    context = context_wrap(TEST_ETHTOOL_I_GOOD)
    parsed = ethtool.Driver(context)
    assert parsed.version == '1.0.0'
    assert parsed.driver == 'virtio_net'
    assert parsed.firmware_version is None
    assert parsed.bus_info == '0000:00:03.0'
    assert not parsed.supports_statistics
    assert not parsed.supports_test
    assert not parsed.supports_eeprom_access
    assert not parsed.supports_register_dump
    assert not parsed.supports_priv_flags
    return


def test_missing_version():
    context = context_wrap(TEST_ETHTOOL_I_MISSING_KEYS)
    parsed = ethtool.Driver(context)
    assert parsed.version is None
    return


def test_missing_value():
    context = context_wrap(TEST_ETHTOOL_I_GOOD)
    parsed = ethtool.Driver(context)
    assert parsed.firmware_version is None
    return


def test_iface():
    context = context_wrap(TEST_ETHTOOL_I_GOOD, path='sbin/ethtool_-i_eth0')
    parsed = ethtool.Driver(context)
    assert parsed.ifname == 'eth0'


def test_no_iface():
    context = context_wrap(TEST_ETHTOOL_I_GOOD, path='foo/bar/baz/oopsie')
    parsed = ethtool.Driver(context)
    assert parsed.ifname is None
    return


ETHTOOL_K_STANDARD = '\nFeatures for bond0:\nrx-checksumming: off [fixed]\ntx-checksumming: on\n    tx-checksum-ipv4: off [fixed]\n    tx-checksum-unneeded: on [fixed]\n    tx-checksum-ip-generic: off [fixed]\n    tx-checksum-ipv6: off [fixed]\n    tx-checksum-fcoe-crc: off [fixed]\n    tx-checksum-sctp: off [fixed]\nscatter-gather: on\n    tx-scatter-gather: on [fixed]\n    tx-scatter-gather-fraglist: off [fixed]\ntcp-segmentation-offload: on\n    tx-tcp-segmentation: on [fixed]\n    tx-tcp-ecn-segmentation: on [fixed]\n    tx-tcp6-segmentation: on [fixed]\nudp-fragmentation-offload: off [fixed]\ngeneric-segmentation-offload: off [requested on]\ngeneric-receive-offload: on\nlarge-receive-offload: on\nrx-vlan-offload: on\ntx-vlan-offload: on\nntuple-filters: off\nreceive-hashing: off\nhighdma: on [fixed]\nrx-vlan-filter: on [fixed]\nvlan-challenged: off [fixed]\ntx-lockless: on [fixed]\nnetns-local: off [fixed]\ntx-gso-robust: off [fixed]\ntx-fcoe-segmentation: off [fixed]\ntx-gre-segmentation: on [fixed]\ntx-udp_tnl-segmentation: on [fixed]\nfcoe-mtu: off [fixed]\nloopback: off [fixed]\n'
ETHTOOL_K_BAD_ARGS = ('\nethtool: bad command line argument(s)\nFor more information run ethtool -h\n').strip()
ETHTOOL_K_CANNOT_GET = ('\nCannot get stats strings information: Operation not supported\n').strip()
ETHTOOL_K_MISSING_COLON = '\nFeatures for bond0:\nrx-checksumming off [fixed]\ntx-checksumming on\n'

def test_Features_good():
    features = ethtool.Features(context_wrap(ETHTOOL_K_STANDARD, path='sos_commands/networking/ethtool_-k_bond0'))
    assert features.ifname == 'bond0'
    assert features.iface == 'bond0'
    assert not features.is_on('rx-checksumming')
    assert features.is_on('tx-checksumming')
    assert features.is_fixed('rx-checksumming')
    assert not features.is_fixed('tx-checksumming')


def test_Features_bad_args():
    features = ethtool.Features(context_wrap(ETHTOOL_K_BAD_ARGS, path='sbin/ethtool_-k_bond0'))
    assert features.ifname == 'bond0'
    assert features.iface == 'bond0'
    assert features.data == {}


def test_Features_cannot_get():
    features = ethtool.Features(context_wrap(ETHTOOL_K_CANNOT_GET, path='sbin/ethtool_-k_eth1'))
    assert features.ifname == 'eth1'
    assert features.iface == 'eth1'
    assert features.data == {}


def test_Features_missing_colon():
    features = ethtool.Features(context_wrap(ETHTOOL_K_MISSING_COLON, path='sbin/ethtool_-k_bond0'))
    assert features.ifname == 'bond0'
    assert features.data == {}


TEST_ETHTOOL_S_DOCS = '\nNIC statistics:\n     rx_octets: 808488730\n     rx_fragments: 0\n     rx_ucast_packets: 1510830\n     rx_mcast_packets: 678653\n     rx_bcast_packets: 9921\n     rx_fcs_errors: 0\n     rx_align_errors: 0\n     rx_xon_pause_rcvd: 0\n     rx_xoff_pause_rcvd: 0\n     rx_mac_ctrl_rcvd: 0\n     rx_xoff_entered: 0\n     rx_frame_too_long_errors: 0\n     rx_jabbers: 0\n'
SUCCEED_ETHTOOL_S = '\nNIC statistics:\n    rx_packets: 912398\n    tx_packets: 965449\n    rx_bytes: 96506134\n    tx_bytes: 190360255\n    rx_broadcast: 4246\n    tx_broadcast: 4248\n    rx_multicast: 18\n    tx_multicast: 20\n    multicast: 18\n    collisions: 0\n    rx_crc_errors: 0\n    rx_no_buffer_count: 0\n    rx_missed_errors: 0\n    tx_aborted_errors: 0\n    tx_carrier_errors: 0\n    tx_window_errors: 0\n    tx_abort_late_coll: 0\n    tx_deferred_ok: 0\n    tx_single_coll_ok: 0\n    tx_multi_coll_ok: 0\n    tx_timeout_count: 0\n    rx_long_length_errors: 0\n    rx_short_length_errors: 0\n    rx_align_errors: 0\n    tx_tcp_seg_good: 0\n    tx_tcp_seg_failed: 0\n    rx_flow_control_xon: 0\n    rx_flow_control_xoff: 0\n    tx_flow_control_xon: 0\n    tx_flow_control_xoff: 0\n    rx_long_byte_count: 96506134\n    tx_dma_out_of_sync: 0\n    tx_smbus: 0\n    rx_smbus: 0\n    dropped_smbus: 0\n    os2bmc_rx_by_bmc: 0\n    os2bmc_tx_by_bmc: 0\n    os2bmc_tx_by_host: 0\n    os2bmc_rx_by_host: 0\n    tx_hwtstamp_timeouts: 0\n    rx_hwtstamp_cleared: 0\n    rx_errors: 0\n    tx_errors: 0\n    tx_dropped: 0\n    rx_length_errors: 0\n    rx_over_errors: 0\n    rx_frame_errors: 0\n    rx_fifo_errors: 0\n    tx_fifo_errors: 0\n    tx_heartbeat_errors: 0\n    tx_queue_0_packets: 613\n    tx_queue_0_bytes: 240342\n    tx_queue_0_restart: 0\n    tx_queue_1_packets: 935473\n    tx_queue_1_bytes: 181899495\n    tx_queue_1_restart: 0\n    tx_queue_2_packets: 6\n    tx_queue_2_bytes: 412\n    tx_queue_2_restart: 0\n    tx_queue_3_packets: 29357\n    tx_queue_3_bytes: 4358198\n    tx_queue_3_restart: 0\n    rx_queue_0_packets: 912398\n    rx_queue_0_bytes: 92856542\n    rx_queue_0_drops: 0\n    rx_queue_0_csum_err: 0\n    rx_queue_0_alloc_failed: 0\n    rx_queue_1_packets: 0\n    rx_queue_1_bytes: 0\n    rx_queue_1_drops: 0\n    rx_queue_1_csum_err: 0\n    rx_queue_1_alloc_failed: 0\n    rx_queue_2_packets: 0\n    rx_queue_2_bytes: 0\n    rx_queue_2_drops: 0\n    rx_queue_2_csum_err: 0\n    rx_queue_2_alloc_failed: 0\n    rx_queue_3_packets: 0\n    rx_queue_3_bytes: 0\n    rx_queue_3_drops: 0\n    rx_queue_3_csum_err: 0\n    rx_queue_3_alloc_failed: 0\n'
ETHTOOL_S_eth0_1 = 'NIC statistics:\n    rxq0: rx_pkts: 5000000\n    rxq0: rx_drops_no_frags: 5000\n    rxq1: rx_pkts: 5000000\n    rxq1: rx_drops_no_frags: 5000\n'
FAILED_ETHTOOL_S_ONE = 'no stats avilable '
FAILED_ETHTOOL_S_TWO = 'Cannot get stats strings information: Operation not supported'
FAILED_ETHTOOL_S_THREE = 'NIC statistics:\nNothing to see here\n'

def test_ethtool_S():
    ethtool_S_info = ethtool.Statistics(context_wrap(SUCCEED_ETHTOOL_S))
    ret = {}
    for line in SUCCEED_ETHTOOL_S.split('\n')[2:-1]:
        key, value = line.split(':')
        ret[key.strip()] = int(value.strip()) if value else None

    eth_data = dict(ethtool_S_info.data)
    assert eth_data == ret
    assert ethtool_S_info.search('rx_queue_3') == {'rx_queue_3_packets': 0, 
       'rx_queue_3_bytes': 0, 
       'rx_queue_3_drops': 0, 
       'rx_queue_3_csum_err': 0, 
       'rx_queue_3_alloc_failed': 0}
    assert ethtool_S_info.search('RX_QUEUE_3', flags=re.IGNORECASE) == {'rx_queue_3_packets': 0, 
       'rx_queue_3_bytes': 0, 
       'rx_queue_3_drops': 0, 
       'rx_queue_3_csum_err': 0, 
       'rx_queue_3_alloc_failed': 0}
    return


def test_ethtool_S_subinterface():
    ethtool_S_info = ethtool.Statistics(context_wrap(ETHTOOL_S_eth0_1))
    assert sorted(ethtool_S_info.data.keys()) == sorted([
     'rxq0: rx_pkts', 'rxq0: rx_drops_no_frags',
     'rxq1: rx_pkts', 'rxq1: rx_drops_no_frags'])
    assert ethtool_S_info.data['rxq0: rx_pkts'] == 5000000


def test_ethtool_S_f():
    ethtool_S_info_f1 = ethtool.Statistics(context_wrap(FAILED_ETHTOOL_S_ONE))
    assert not ethtool_S_info_f1.ifname
    ethtool_S_info_f2 = ethtool.Statistics(context_wrap(FAILED_ETHTOOL_S_TWO))
    assert not ethtool_S_info_f2.ifname
    ethtool_S_info_f2 = ethtool.Statistics(context_wrap(FAILED_ETHTOOL_S_THREE))
    assert not ethtool_S_info_f2.ifname


TEST_ETHTOOL_TIMESTAMP = '\nTime stamping parameters for eno1:\n\nCapabilities:\n    hardware-transmit     (SOF_TIMESTAMPING_TX_HARDWARE)\n    software-transmit     (SOF_TIMESTAMPING_TX_SOFTWARE)\n    hardware-receive      (SOF_TIMESTAMPING_RX_HARDWARE)\n    software-receive      (SOF_TIMESTAMPING_RX_SOFTWARE)\n    software-system-clock (SOF_TIMESTAMPING_SOFTWARE)\n    hardware-raw-clock    (SOF_TIMESTAMPING_RAW_HARDWARE)\nPTP Hardware Clock: 0\nHardware Transmit Timestamp Modes:\n    off                   (HWTSTAMP_TX_OFF)\n    on                    (HWTSTAMP_TX_ON)\nHardware Receive Filter Modes:\n    none                  (HWTSTAMP_FILTER_NONE)\n    all                   (HWTSTAMP_FILTER_ALL)\n'
TEST_ETHTOOL_TIMESTAMP_AB = '\nTime stamping parameters for eno1:\n\nCapabilities:\n    hardware-transmit     (SOF_TIMESTAMPING_TX_HARDWARE\n    software-transmit     (SOF_TIMESTAMPING_TX_SOFTWARE)\n    hardware-receive      (SOF_TIMESTAMPING_RX_HARDWARE)\n    software-receive      (SOF_TIMESTAMPING_RX_SOFTWARE)\n    software-system-clock (SOF_TIMESTAMPING_SOFTWARE)\n    hardware-raw-clock    (SOF_TIMESTAMPING_RAW_HARDWARE)\nPTP Hardware Clock: 0\nHardware Transmit Timestamp Modes:\n    off                   (HWTSTAMP_TX_OFF)\n    on                    (HWTSTAMP_TX_ON)\nHardware Receive Filter Modes:\n    none                  (HWTSTAMP_FILTER_NONE)\n    all                   (HWTSTAMP_FILTER_ALL)\n'

def test_ethtool_timestamp():
    timestamp = ethtool.TimeStamp(context_wrap(TEST_ETHTOOL_TIMESTAMP, path='sbin/ethtool_-T_eno1'))
    assert timestamp.ifname == 'eno1'
    assert timestamp.data['Capabilities']['hardware-transmit'] == 'SOF_TIMESTAMPING_TX_HARDWARE'
    assert timestamp.data['Capabilities']['hardware-raw-clock'] == 'SOF_TIMESTAMPING_RAW_HARDWARE'
    assert timestamp.data['PTP Hardware Clock'] == '0'
    assert timestamp.data['Hardware Transmit Timestamp Modes']['off'] == 'HWTSTAMP_TX_OFF'
    assert timestamp.data['Hardware Receive Filter Modes']['all'] == 'HWTSTAMP_FILTER_ALL'
    with pytest.raises(ParseException) as (pe):
        ethtool.TimeStamp(context_wrap(TEST_ETHTOOL_TIMESTAMP_AB, path='sbin/ethtool_-T_eno1'))
        assert 'bad line:' in str(pe)


TEST_EXTRACT_FROM_PATH_1 = ('\n    ethtool_-a_eth0\n').strip()
TEST_EXTRACT_FROM_PATH_2 = ('\n    ethtool_-a_bond0.104_bond0\n').strip()
TEST_EXTRACT_FROM_PATH_3 = ('\n    ethtool_-a___tmp199222\n').strip()
TEST_EXTRACT_FROM_PATH_4 = ('\n    ethtool_-a_macvtap_bond0\n').strip()
TEST_EXTRACT_FROM_PATH_5 = ('\n    ethtool_-a_p3p2.2002-fcoe_p3p2\n').strip()
TEST_EXTRACT_FROM_PATH_PARAM = ('\n    ethtool_-a\n').strip()

def test_extract_from_path_1():
    test_data = [
     (
      TEST_EXTRACT_FROM_PATH_1, 'eth0'),
     (
      TEST_EXTRACT_FROM_PATH_2, 'bond0.104@bond0'),
     (
      TEST_EXTRACT_FROM_PATH_3, '__tmp199222'),
     (
      TEST_EXTRACT_FROM_PATH_4, 'macvtap@bond0'),
     (
      TEST_EXTRACT_FROM_PATH_5, 'p3p2.2002-fcoe@p3p2')]
    for input_, value in test_data:
        ifname = ethtool.extract_iface_name_from_path(input_, TEST_EXTRACT_FROM_PATH_PARAM)
        assert ifname == value


TEST_ETHTOOL_DOCS = '\n        Settings for eth0:\n                Supported ports: [ TP MII ]\n                Supported link modes:   10baseT/Half 10baseT/Full\n                                       100baseT/Half 100baseT/Full\n                Supported pause frame use: No\n                Supports auto-negotiation: Yes\n                Advertised link modes:  10baseT/Half 10baseT/Full\n                                        100baseT/Half 100baseT/Full\n                Advertised pause frame use: Symmetric\n                Advertised auto-negotiation: Yes\n                Link partner advertised link modes:  10baseT/Half 10baseT/Full\n                                                     100baseT/Half 100baseT/Full\n                Link partner advertised pause frame use: Symmetric\n                Link partner advertised auto-negotiation: No\n                Speed: 100Mb/s\n                Duplex: Full\n                Port: MII\n                PHYAD: 32\n                Transceiver: internal\n                Auto-negotiation: on\n        Cannot get wake-on-lan settings: Operation not permitted\n                Current message level: 0x00000007 (7)\n                                       drv probe link\n        Cannot get link status: Operation not permitted\n'
ETHTOOL_INFO = ('\nSettings for eth1:\n    Supported ports: [ TP MII ]\n    Supported link modes: 10baseT/Half 10baseT/Full\n                          100baseT/Half 100baseT/Full\n                          1000baseT/Full\n    Supported pause frame use: Symmetric\n    Supports auto-negotiation: Yes\n    Advertised link modes: 10baseT/Half 10baseT/Full\n                           100baseT/Half 100baseT/Full\n                           1000baseT/Full\n    Advertised pause frame use: Symmetric\n    Advertised auto-negotiation: Yes\n    Speed: 1000Mb/s\n    Duplex: Full\n    Port: Twisted Pair\n    PHYAD: 1\n    Transceiver: internal\n    Auto-negotiation: on\n    MDI-X: off (auto)\n    Supports Wake-on: pumbg\n    Wake-on: d\n    Current message level: 0x00000007 (7)\n                           drv probe link\n    Link detected: yes\n').strip()
ETHTOOL_INFO_TEST = ('\nSettings for eth1:\n    Supported pause frame use: Symmetric\n\n    Supports auto-negotiation: Yes\n').strip()

def test_ethtool():
    ethtool_info = ethtool.Ethtool(context_wrap(ETHTOOL_INFO, path='ethtool_eth1'))
    assert ethtool_info.ifname == 'eth1'
    assert ethtool_info.link_detected
    assert ethtool_info.speed == ['1000Mb/s']
    assert ethtool_info.supported_link_modes == [
     '10baseT/Half', '10baseT/Full',
     '100baseT/Half', '100baseT/Full',
     '1000baseT/Full']
    assert ethtool_info.advertised_link_modes == [
     '10baseT/Half', '10baseT/Full',
     '100baseT/Half', '100baseT/Full',
     '1000baseT/Full']
    assert ethtool_info.supported_ports == ['TP', 'MII']


def test_ethtool_corner_cases():
    ethtool_info = ethtool.Ethtool(context_wrap(ETHTOOL_INFO_TEST, path='ethtool_eth1'))
    assert ethtool_info.ifname == 'eth1'


ETHTOOL_INFO_BAD_1 = ('\nSettings for dummy2:\nNo data available\n').strip()
ETHTOOL_INFO_BAD_2 = ('\nNo data available\n').strip()
ETHTOOL_INFO_BAD_3 = '\nSettings for eth1:\n    Supported ports\n    Supported link modes 10baseT/Half 10baseT/Full\n                          100baseT/Half 100baseT/Full\n'

def test_ethtool_fail():
    with pytest.raises(ParseException):
        ethtool.Ethtool(context_wrap(FAIL_ETHTOOL_A_1, path='ethtool_eth1'))
    with pytest.raises(ParseException) as (e):
        ethtool.Ethtool(context_wrap(ETHTOOL_INFO_BAD_1, path='ethtool_eth1'))
    assert 'Fake ethnic as ethtool command argument' in str(e.value)
    with pytest.raises(ParseException) as (e):
        ethtool.Ethtool(context_wrap(ETHTOOL_INFO_BAD_2, path='ethtool_eth1'))
    assert 'ethtool: unrecognised first line ' in str(e.value)
    with pytest.raises(ParseException) as (e):
        ethtool.Ethtool(context_wrap(ETHTOOL_INFO_BAD_3, path='ethtool_eth1'))
    assert 'Ethtool unable to parse content' in str(e.value)


def test_ethtool_i_doc_examples():
    env = {'coalesce': [
                  ethtool.CoalescingInfo(context_wrap(TEST_ETHTOOL_C_DOCS, path='ethtool_-c_eth0'))], 
       'interfaces': [
                    ethtool.Driver(context_wrap(TEST_ETHTOOL_I_DOCS, path='ethtool_-i_bond0'))], 
       'ethers': [
                ethtool.Ethtool(context_wrap(TEST_ETHTOOL_DOCS, path='ethtool_eth0'))], 
       'features': [
                  ethtool.Features(context_wrap(ETHTOOL_K_STANDARD, path='ethtool_-k_bond0'))], 
       'pause': [
               ethtool.Pause(context_wrap(TEST_ETHTOOL_A_DOCS, path='ethtool_-a_eth0'))], 
       'ring': [
              ethtool.Ring(context_wrap(TEST_ETHTOOL_G_DOCS, path='ethtool_-g_eth0'))], 
       'stats': [
               ethtool.Statistics(context_wrap(TEST_ETHTOOL_S_DOCS, path='ethtool_-S_eth0'))], 
       'timestamp': [
                   ethtool.TimeStamp(context_wrap(TEST_ETHTOOL_TIMESTAMP, path='ethtool_-T_eno1'))]}
    failed, total = doctest.testmod(ethtool, globs=env)
    assert failed == 0