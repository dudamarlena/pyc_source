# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/combiners/tests/test_nmcli_dev_show.py
# Compiled at: 2019-11-14 13:57:46
from insights.tests import context_wrap
from insights.combiners.nmcli_dev_show import AllNmcliDevShow
from insights.combiners import nmcli_dev_show
from insights.parsers.nmcli import NmcliDevShow
import doctest
NMCLI_SHOW1 = ('\nGENERAL.DEVICE:                         eth0\nGENERAL.TYPE:                           ethernet\nGENERAL.HWADDR:                         00:1A:4A:16:02:E0\nGENERAL.MTU:                            1500\nGENERAL.STATE:                          100 (connected)\nGENERAL.CONNECTION:                     System eth0\nGENERAL.CON-PATH:                       /org/freedesktop/NetworkManager/ActiveConnection/1\nWIRED-PROPERTIES.CARRIER:               on\nIP4.ADDRESS[1]:                         10.72.37.85/23\nIP4.GATEWAY:                            10.72.37.254\nIP4.ROUTE[1]:                           dst = 0.0.0.0/0, nh = 10.72.37.254, mt = 100\nIP4.ROUTE[2]:                           dst = 10.72.36.0/23, nh = 0.0.0.0, mt = 100\nIP4.DNS[1]:                             10.72.17.5\nIP4.DOMAIN[1]:                          gsslab.pek2.redhat.com\nIP6.ADDRESS[1]:                         2620:52:0:4824:21a:4aff:fe16:2e0/64\nIP6.ADDRESS[2]:                         fe80::21a:4aff:fe16:2e0/64\nIP6.GATEWAY:                            fe80:52:0:4824::1fe\nIP6.ROUTE[1]:                           dst = ff00::/8, nh = ::, mt = 256, table=255\nIP6.ROUTE[2]:                           dst = fe80::/64, nh = ::, mt = 256\nIP6.ROUTE[3]:                           dst = ::/0, nh = fe80:52:0:4824::1fe, mt = 1024\nIP6.ROUTE[4]:                           dst = 2620:52:0:4824::/64, nh = ::, mt = 256\n\nGENERAL.DEVICE:                         lo\nGENERAL.TYPE:                           loopback\nGENERAL.HWADDR:                         00:00:00:00:00:00\nGENERAL.MTU:                            65536\nGENERAL.STATE:                          10 (unmanaged)\nGENERAL.CONNECTION:                     --\nGENERAL.CON-PATH:                       --\nIP4.ADDRESS[1]:                         127.0.0.1/8\nIP4.GATEWAY:                            --\nIP6.ADDRESS[1]:                         ::1/128\nIP6.GATEWAY:                            --\n').strip()
NMCLI_SHOW2 = ('\nGENERAL.DEVICE:                         eth0\nGENERAL.TYPE:                           ethernet\nGENERAL.HWADDR:                         00:1A:4A:16:02:E0\nGENERAL.MTU:                            1500\nGENERAL.STATE:                          100 (connected)\nGENERAL.CONNECTION:                     System eth0\nGENERAL.CON-PATH:                       /org/freedesktop/NetworkManager/ActiveConnection/1\nWIRED-PROPERTIES.CARRIER:               on\nIP4.ADDRESS[1]:                         10.72.37.85/23\nIP4.GATEWAY:                            10.72.37.254\nIP4.ROUTE[1]:                           dst = 0.0.0.0/0, nh = 10.72.37.254, mt = 100\nIP4.ROUTE[2]:                           dst = 10.72.36.0/23, nh = 0.0.0.0, mt = 100\nIP4.DNS[1]:                             10.72.17.5\nIP4.DOMAIN[1]:                          gsslab.pek2.redhat.com\nIP6.ADDRESS[1]:                         2620:52:0:4824:21a:4aff:fe16:2e0/64\nIP6.ADDRESS[2]:                         fe80::21a:4aff:fe16:2e0/64\nIP6.GATEWAY:                            fe80:52:0:4824::1fe\nIP6.ROUTE[1]:                           dst = ff00::/8, nh = ::, mt = 256, table=255\nIP6.ROUTE[2]:                           dst = fe80::/64, nh = ::, mt = 256\nIP6.ROUTE[3]:                           dst = ::/0, nh = fe80:52:0:4824::1fe, mt = 1024\nIP6.ROUTE[4]:                           dst = 2620:52:0:4824::/64, nh = ::, mt = 256\n').strip()
NMCLI_SHOW3 = ('\nGENERAL.DEVICE:                         lo\nGENERAL.TYPE:                           loopback\nGENERAL.HWADDR:                         00:00:00:00:00:00\nGENERAL.MTU:                            65536\nGENERAL.STATE:                          10 (unmanaged)\nGENERAL.CONNECTION:                     --\nGENERAL.CON-PATH:                       --\nIP4.ADDRESS[1]:                         127.0.0.1/8\nIP4.GATEWAY:                            --\nIP6.ADDRESS[1]:                         ::1/128\nIP6.GATEWAY:                            --\n').strip()

def test_allnmcli1():
    nmcli_obj = NmcliDevShow(context_wrap(NMCLI_SHOW1))
    allnmcli_obj = AllNmcliDevShow(nmcli_obj, None)
    con_dev = allnmcli_obj.connected_devices
    assert sorted(con_dev) == sorted(['eth0'])
    assert allnmcli_obj['eth0']['IP4_GATEWAY'] == '10.72.37.254'
    assert allnmcli_obj['eth0']['IP4_DNS1'] == '10.72.17.5'
    assert allnmcli_obj['eth0']['STATE'] == 'connected'
    assert allnmcli_obj['eth0']['CON-PATH'] == '/org/freedesktop/NetworkManager/ActiveConnection/1'
    assert len(allnmcli_obj['lo']) == 10
    return


def test_allnmcli2():
    nmcli_obj1 = NmcliDevShow(context_wrap(NMCLI_SHOW2))
    nmcli_obj2 = NmcliDevShow(context_wrap(NMCLI_SHOW3))
    allnmcli_obj = AllNmcliDevShow(None, [nmcli_obj1, nmcli_obj2])
    con_dev = allnmcli_obj.connected_devices
    assert sorted(con_dev) == sorted(['eth0'])
    assert allnmcli_obj['eth0']['IP4_GATEWAY'] == '10.72.37.254'
    assert allnmcli_obj['eth0']['IP4_DNS1'] == '10.72.17.5'
    assert allnmcli_obj['eth0']['STATE'] == 'connected'
    assert allnmcli_obj['eth0']['CON-PATH'] == '/org/freedesktop/NetworkManager/ActiveConnection/1'
    assert len(allnmcli_obj['lo']) == 10
    return


def test_doc_examples():
    env = {'allnmclidevshow': AllNmcliDevShow(NmcliDevShow(context_wrap(NMCLI_SHOW1)), None)}
    failed, total = doctest.testmod(nmcli_dev_show, globs=env)
    assert failed == 0
    return