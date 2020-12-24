# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_nmcli.py
# Compiled at: 2019-11-14 13:57:46
from insights.tests import context_wrap
from insights.parsers.nmcli import NmcliDevShow, NmcliDevShowSos
from insights.parsers.nmcli import NmcliConnShow
from insights.parsers import nmcli, SkipException
import doctest, pytest
NMCLI_SHOW = '\nGENERAL.DEVICE:                         em3\nGENERAL.TYPE:                           ethernet\nGENERAL.HWADDR:                         B8:2A:72:DE:F8:B9\nGENERAL.MTU:                            1500\nGENERAL.STATE:                          100 (connected)\nGENERAL.CONNECTION:                     em3\nGENERAL.CON-PATH:                       /org/freedesktop/NetworkManager/ActiveConnection/1\nWIRED-PROPERTIES.CARRIER:               on\nIP4.ADDRESS[1]:                         10.16.184.98/22\nIP4.GATEWAY:                             10.16.187.254\nIP4.DNS[1]:                             10.16.36.29\nIP4.DNS[2]:                             10.11.5.19\nIP4.DNS[3]:                             10.5.30.160\nIP4.DOMAIN[1]:                          khw.lab.eng.bos.example.com\nIP6.ADDRESS[1]:                         2620:52:0:10bb:ba2a:72ff:fede:f8b9/64\nIP6.ADDRESS[2]:                         fe80::ba2a:72ff:fede:f8b9/64\nIP6.GATEWAY:                            fe80:52:0:10bb::fc\nIP6.ROUTE[1]:                           dst = 2620:52:0:10bb::/64, nh = ::, mt = 100\n\nGENERAL.DEVICE:                         em1\nGENERAL.TYPE:                           ethernet\nGENERAL.HWADDR:                         B8:2A:72:DE:F8:BB\nGENERAL.MTU:                            1500\nGENERAL.STATE:                          100 connected\nGENERAL.CONNECTION:                     --\nGENERAL.CON-PATH:                       --\nWIRED-PROPERTIES.CARRIER:               off\n\nGENERAL.DEVICE:                         em2\nGENERAL.TYPE:                           ethernet\nGENERAL.HWADDR:                         B8:AA:BB:DE:F8:BC\nGENERAL.MTU:                            1500\nGENERAL.STATE:                          100 (connected)\nGENERAL.CONNECTION:                     --\nGENERAL.CON-PATH:                       --\nWIRED-PROPERTIES.CARRIER:               off\n'
NMCLI_SHOW_SOS = ('\nGENERAL.DEVICE:                         em3\nGENERAL.TYPE:                           ethernet\nGENERAL.HWADDR:                         B8:2A:72:DE:F8:B9\nGENERAL.MTU:                            1500\nGENERAL.STATE:                          100 (connected)\nGENERAL.CONNECTION:                     em3\nGENERAL.CON-PATH:                       /org/freedesktop/NetworkManager/ActiveConnection/1\nWIRED-PROPERTIES.CARRIER:               on\nIP4.ADDRESS[1]:                         10.16.184.98/22\nIP4.GATEWAY:                             10.16.187.254\nIP4.DNS[1]:                             10.16.36.29\nIP4.DNS[2]:                             10.11.5.19\nIP4.DNS[3]:                             10.5.30.160\nIP4.DOMAIN[1]:                          khw.lab.eng.bos.example.com\nIP6.ADDRESS[1]:                         2620:52:0:10bb:ba2a:72ff:fede:f8b9/64\nIP6.ADDRESS[2]:                         fe80::ba2a:72ff:fede:f8b9/64\nIP6.GATEWAY:                            fe80:52:0:10bb::fc\nIP6.ROUTE[1]:                           dst = 2620:52:0:10bb::/64, nh = ::, mt = 100\n').strip()
NMCLI_SHOW_ERROR = "\nError: Option '-l' is unknown, try 'nmcli -help'.\n"
NMCLI_SHOW_ERROR_2 = "\nError: Option '-l' is unknown, try 'nmcli -help'.\nWarning: nmcli (1.0.0) and NetworkManager (1.0.6) versions don't match. Use --nocheck to suppress the warning.\n"
STATIC_CONNECTION_SHOW_1 = ('\nNAME      UUID                                  TYPE      DEVICE\nenp0s3    320d4923-c410-4b22-b7e9-afc5f794eecc  ethernet  enp0s3\nvirbr0    7c7dec66-4a8c-4b49-834a-889194b3b83c  bridge    virbr0\ntest-net-1  f858b1cc-d149-4de0-93bc-b1826256847a  ethernet  --\n').strip()
STATIC_CONNECTION_SHOW_2 = ('\nNAME      UUID                                  TYPE      DEVICE\nenp0s3    320d4923-c410-4b22-b7e9-afc5f794eecc  ethernet  enp0s3\nvirbr0    7c7dec66-4a8c-4b49-834a-889194b3b83c  bridge    virbr0\ntest-net-1  f858b1cc-d149-4de0-93bc-b1826256847a  ethernet  --\ntest-net-2 f858b1cc-d149-4de0-93bc-b1826256847a  ethernet  --\n').strip()
STATIC_CONNECTION_SHOW_3 = ('\nWarning: nmcli (1.0.0) and NetworkManager (1.0.6) versions don\'t match. Use --nocheck to suppress the warning.\nNAME           UUID                                  TYPE            DEVICE\nenp0s8         00cb8299-feb9-55b6-a378-3fdc720e0bc6  802-3-ethernet  --\nenp0s3         bfb4760c-96ce-4a29-9f2e-7427051da943  802-3-ethernet  enp0s3"\n').strip()
NMCLI_DEV_SHOW = ('\nTextFileProvider("\'/tmp/insights-fcct09p0/insights-rhel7-box-20191016082653/insights_commands/nmcli_dev_show\'")\nGENERAL.DEVICE:                         br0\nGENERAL.TYPE:                           bridge\nGENERAL.HWADDR:                         7A:C3:4C:23:65:8A\nGENERAL.MTU:                            1450\nGENERAL.STATE:                          100 (connected)\nGENERAL.CONNECTION:                     br0\nGENERAL.CON-PATH:                       /org/freedesktop/NetworkManager/ActiveConnection/1\nIP4.GATEWAY:\nIP6.ADDRESS[1]:                         fe80::78c3:4cff:fe23:658a/64\nIP6.GATEWAY:\n\nGENERAL.DEVICE:                         enp0s3\nGENERAL.TYPE:                           ethernet\nGENERAL.HWADDR:                         08:00:27:4A:C5:EF\nGENERAL.MTU:                            1500\nGENERAL.STATE:                          100 (connected)\nGENERAL.CONNECTION:                     enp0s3\nGENERAL.CON-PATH:                       /org/freedesktop/NetworkManager/ActiveConnection/0\nWIRED-PROPERTIES.CARRIER:               on\nIP4.ADDRESS[1]:                         10.0.2.15/24\nIP4.GATEWAY:                            10.0.2.2\nIP4.DNS[1]:                             10.0.2.3\nIP4.DOMAIN[1]:                          redhat.com\nIP6.ADDRESS[1]:                         fe80::a00:27ff:fe4a:c5ef/64\nIP6.GATEWAY:\n\nGENERAL.DEVICE:                         vxlan10\nGENERAL.TYPE:                           vxlan\nGENERAL.HWADDR:                         7A:C3:4C:23:65:8A\nGENERAL.MTU:                            1450\nGENERAL.STATE:                          100 (connected)\nGENERAL.CONNECTION:                     vxlan10\nGENERAL.CON-PATH:                       /org/freedesktop/NetworkManager/ActiveConnection/2\nIP4.GATEWAY:\nIP6.GATEWAY:\n\nGENERAL.DEVICE:                         enp0s8\nGENERAL.TYPE:                           ethernet\nGENERAL.HWADDR:                         08:00:27:45:74:6B\nGENERAL.MTU:                            1500\nGENERAL.STATE:                          30 (disconnected)\nGENERAL.CONNECTION:                     --\nGENERAL.CON-PATH:                       --\nWIRED-PROPERTIES.CARRIER:               on\n\nGENERAL.DEVICE:                         enp0s9\nGENERAL.TYPE:                           ethernet\nGENERAL.HWADDR:                         08:00:27:F2:32:1E\nGENERAL.MTU:                            1500\nGENERAL.STATE:                          30 (disconnected)\nGENERAL.CONNECTION:                     --\nGENERAL.CON-PATH:                       --\nWIRED-PROPERTIES.CARRIER:               on\n\nGENERAL.DEVICE:                         lo\nGENERAL.TYPE:                           loopback\nGENERAL.HWADDR:                         00:00:00:00:00:00\nGENERAL.MTU:                            65536\nGENERAL.STATE:                          10 (unmanaged)\nGENERAL.CONNECTION:                     --\nGENERAL.CON-PATH:                       --\nIP4.ADDRESS[1]:                         127.0.0.1/8\nIP4.GATEWAY:\nIP6.ADDRESS[1]:                         ::1/128\nIP6.GATEWAY:\n').strip()

def test_nmcli():
    nmcli_obj = NmcliDevShow(context_wrap(NMCLI_SHOW))
    con_dev = nmcli_obj.connected_devices
    assert sorted(con_dev) == sorted(['em1', 'em3', 'em2'])
    assert nmcli_obj['em3']['IP4_GATEWAY'] == '10.16.187.254'
    assert nmcli_obj['em3']['IP4_DNS1'] == '10.16.36.29'
    assert nmcli_obj['em3']['IP6_ROUTE1'] == 'dst = 2620:52:0:10bb::/64, nh = ::, mt = 100'
    assert nmcli_obj['em1']['STATE'] == 'connected'
    assert nmcli_obj['em1']['CON-PATH'] == '--'
    assert nmcli_obj['em3']['IP6_ADDRESS1'] == '2620:52:0:10bb:ba2a:72ff:fede:f8b9/64'
    assert nmcli_obj['em3']['IP6_ADDRESS2'] == 'fe80::ba2a:72ff:fede:f8b9/64'
    assert nmcli_obj['em3']['CON-PATH'] == '/org/freedesktop/NetworkManager/ActiveConnection/1'
    assert len(nmcli_obj['em3']) == 17
    assert len(nmcli_obj['em1']) == 7
    nmcli_obj = NmcliDevShow(context_wrap(NMCLI_DEV_SHOW))
    assert 'IP6_GATEWAY' not in nmcli_obj['lo']
    assert 'IP6_ADDRESS1' in nmcli_obj['lo']
    assert nmcli_obj['lo']['IP6_ADDRESS1'] == '::1/128'
    assert nmcli_obj.data is not None
    return


def test_nmcli_sos():
    nmcli_obj = NmcliDevShowSos(context_wrap(NMCLI_SHOW_SOS))
    con_dev = nmcli_obj.connected_devices
    assert sorted(con_dev) == sorted(['em3'])
    assert nmcli_obj['em3']['IP4_GATEWAY'] == '10.16.187.254'
    assert nmcli_obj['em3']['IP4_DNS1'] == '10.16.36.29'
    assert nmcli_obj['em3']['IP6_ROUTE1'] == 'dst = 2620:52:0:10bb::/64, nh = ::, mt = 100'
    assert nmcli_obj['em3']['IP6_ADDRESS1'] == '2620:52:0:10bb:ba2a:72ff:fede:f8b9/64'
    assert nmcli_obj['em3']['IP6_ADDRESS2'] == 'fe80::ba2a:72ff:fede:f8b9/64'
    assert nmcli_obj['em3']['CON-PATH'] == '/org/freedesktop/NetworkManager/ActiveConnection/1'
    assert len(nmcli_obj['em3']) == 17


def test_static_connection_test_1():
    static_conn = NmcliConnShow(context_wrap(STATIC_CONNECTION_SHOW_1))
    assert static_conn.data[0] == {'NAME': 'enp0s3', 'UUID': '320d4923-c410-4b22-b7e9-afc5f794eecc', 'TYPE': 'ethernet', 'DEVICE': 'enp0s3'}
    assert static_conn.disconnected_connection == ['test-net-1']


def test_static_connection_test_2():
    static_conn = NmcliConnShow(context_wrap(STATIC_CONNECTION_SHOW_2))
    assert static_conn.disconnected_connection == ['test-net-1', 'test-net-2']


def test_static_connection_test_3():
    static_conn = NmcliConnShow(context_wrap(STATIC_CONNECTION_SHOW_3))
    assert static_conn.disconnected_connection == ['enp0s8']


def test_nmcli_dev_show_ab():
    with pytest.raises(SkipException):
        NmcliDevShow(context_wrap(''))
    with pytest.raises(SkipException):
        NmcliDevShow(context_wrap('GENERAL.TYPE: ethernet'))
    with pytest.raises(SkipException):
        NmcliDevShow(context_wrap('Error'))


def test_nmcli_doc_examples():
    env = {'nmcli_obj': NmcliDevShow(context_wrap(NMCLI_SHOW)), 
       'nmcli_obj_sos': NmcliDevShowSos(context_wrap(NMCLI_SHOW_SOS)), 
       'static_conn': NmcliConnShow(context_wrap(STATIC_CONNECTION_SHOW_1))}
    failed, total = doctest.testmod(nmcli, globs=env)
    assert failed == 0


def test_nmcli_exceptions():
    with pytest.raises(SkipException) as (exc):
        nmcli_obj = NmcliConnShow(context_wrap(NMCLI_SHOW_ERROR))
        nmcli_obj = NmcliConnShow(context_wrap(NMCLI_SHOW_ERROR_2))
        assert nmcli_obj is None
    assert 'Invalid Contents!' in str(exc)
    return