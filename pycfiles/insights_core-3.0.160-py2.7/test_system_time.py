# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_system_time.py
# Compiled at: 2019-05-16 13:41:33
from insights.tests import context_wrap
from insights.parsers import system_time
CHRONY_CONF = '\n# Use public servers from the pool.ntp.org project.\n# Please consider joining the pool (http://www.pool.ntp.org/join.html).\nserver 0.rhel.pool.ntp.org iburst\nserver 1.rhel.pool.ntp.org iburst\nserver 2.rhel.pool.ntp.org iburst\nserver 3.rhel.pool.ntp.org iburst\n\n# Ignore stratum in source selection.\nstratumweight 0\n\n# Record the rate at which the system clock gains/losses time.\ndriftfile /var/lib/chrony/drift\n\n# Enable kernel RTC synchronization.\nrtcsync\n\n# In first three updates step the system clock instead of slew\n# if the adjustment is larger than 10 seconds.\nmakestep 10 3\n\n# Allow NTP client access from local network.\n#allow 192.168/16\n\n# Listen for commands only on localhost.\nbindcmdaddress 127.0.0.1\nbindcmdaddress ::1\n\n# Serve time even if not synchronized to any NTP server.\n#local stratum 10\n\nkeyfile /etc/chrony.keys\n\n# Specify the key used as password for chronyc.\ncommandkey 1\n\n# Generate command key if missing.\ngeneratecommandkey\n\n# Disable logging of client accesses.\nnoclientlog\n\n# Send a message to syslog if a clock adjustment is larger than 0.5 seconds.\nlogchange 0.5\n\nlogdir /var/log/chrony\n#log measurements statistics tracking\n\nleapsecmode slew\nmaxslewrate 1000\nsmoothtime 400 0.001 leaponly\n'
STANDARD_NTP_CONF = '\n# For more information about this file, see the man pages\n# ntp.conf(5), ntp_acc(5), ntp_auth(5), ntp_clock(5), ntp_misc(5), ntp_mon(5).\n\ndriftfile /var/lib/ntp/drift\n\n# Permit time synchronization with our time source, but do not\n# permit the source to query or modify the service on this system.\nrestrict default nomodify notrap nopeer noquery\n\n# Permit all access over the loopback interface.  This could\n# be tightened as well, but to do so would effect some of\n# the administrative functions.\nrestrict 127.0.0.1\nrestrict ::1\n\n# Hosts on local network are less restricted.\n#restrict 192.168.1.0 mask 255.255.255.0 nomodify notrap\n\n# Use public servers from the pool.ntp.org project.\n# Please consider joining the pool (http://www.pool.ntp.org/join.html).\n#server 0.rhel.pool.ntp.org iburst\n#server 1.rhel.pool.ntp.org iburst\n#server 2.rhel.pool.ntp.org iburst\n\n#broadcast 192.168.1.255 autokey        # broadcast server\n#broadcastclient                        # broadcast client\n#broadcast 224.0.1.1 autokey            # multicast server\n#multicastclient 224.0.1.1              # multicast client\n#manycastserver 239.255.254.254         # manycast server\n#manycastclient 239.255.254.254 autokey # manycast client\n\n# Enable public key cryptography.\n#crypto\n\nincludefile /etc/ntp/crypto/pw\n\n# Key file containing the keys and key identifiers used when operating\n# with symmetric key cryptography.\nkeys /etc/ntp/keys\n\n# Specify the key identifiers which are trusted.\n#trustedkey 4 8 42\n\n# Specify the key identifier to use with the ntpdc utility.\n#requestkey 8\n\n# Specify the key identifier to use with the ntpq utility.\n#controlkey 8\n\n# Enable writing of statistics records.\n#statistics clockstats cryptostats loopstats peerstats\n\n# Disable the monitoring facility to prevent amplification attacks using ntpdc\n# monlist command when default restrict does not include the noquery flag. See\n# CVE-2013-5211 for more details.\n# Note: Monitoring will not be disabled with the limited restriction flag.\n#disable monitor\n\n# Set a couple of single keyword options:\nbroadcastclient\niburst\n\n### Added by IPA Installer ###\nserver 127.127.1.0\nfudge 127.127.1.0 stratum 10\n\nserver 10.20.30.40\nserver 192.168.1.111\n\n### Added by IPA Installer ###\npeer ntp1.example.com\npeer ntp2.example.com\npeer ntp3.example.com\n\n'
ZERO_HOSTS_NTP_CONF = '\nbroadcastclient\n'
NTP_TINKER_CONF = '\ndriftfile /var/lib/ntp/ntp.drift\nrestrict default kod nomodify notrap nopeer noquery\nrestrict 127.0.0.1\nserver 192.168.17.62 iburst\ntinker step 0.9\ntinker step step\ntinker step 0.4\n'

def test_chrony_conf():
    ntp_obj = system_time.ChronyConf(context_wrap(CHRONY_CONF))
    result = ntp_obj.data
    assert result['server'] == ['0.rhel.pool.ntp.org iburst',
     '1.rhel.pool.ntp.org iburst',
     '2.rhel.pool.ntp.org iburst',
     '3.rhel.pool.ntp.org iburst']
    assert 'rtcsync' in result
    assert result.get('rtcsync') is None
    assert result['leapsecmode'] == ['slew']
    assert result['smoothtime'] == ['400 0.001 leaponly']
    assert ntp_obj.get_param('device') == [None]
    assert ntp_obj.get_param('device', 'embn0') == [None]
    assert ntp_obj.get_param('device', default='bad') == ['bad']
    assert ntp_obj.get_param('device', param='embn0', default='bad') == ['bad']
    assert ntp_obj.get_param('device', 'embn0', 'bad') == ['bad']
    assert ntp_obj.get_param('noclientlog') == [None]
    assert ntp_obj.get_param('noclientlog', 'true') == [None]
    assert ntp_obj.get_param('noclientlog', default='yes') == [None]
    assert ntp_obj.get_param('noclientlog', param='true', default='yes') == [None]
    assert ntp_obj.get_param('noclientlog', 'true', 'yes') == [None]
    assert ntp_obj.get_param('commandkey') == ['1']
    assert ntp_obj.get_param('commandkey', '0') == ['1']
    assert ntp_obj.get_param('commandkey', default='2') == ['1']
    assert ntp_obj.get_param('commandkey', param='0', default='2') == ['1']
    assert ntp_obj.get_param('commandkey', '0', '2') == ['1']
    assert ntp_obj.get_last('device') is None
    assert ntp_obj.get_last('device', 'embn0') is None
    assert ntp_obj.get_last('device', default='bad') == 'bad'
    assert ntp_obj.get_last('device', param='embn0', default='bad') == 'bad'
    assert ntp_obj.get_last('device', 'embn0', 'bad') == 'bad'
    assert ntp_obj.get_last('noclientlog') is None
    assert ntp_obj.get_last('noclientlog', 'true') is None
    assert ntp_obj.get_last('noclientlog', default='yes') is None
    assert ntp_obj.get_last('noclientlog', param='true', default='yes') is None
    assert ntp_obj.get_last('noclientlog', 'true', 'yes') is None
    assert ntp_obj.get_last('commandkey') == '1'
    assert ntp_obj.get_last('commandkey', '0') == '1'
    assert ntp_obj.get_last('commandkey', default='2') == '1'
    assert ntp_obj.get_last('commandkey', param='0', default='2') == '1'
    assert ntp_obj.get_last('commandkey', '0', '2') == '1'
    return


LOCALTIME = '/etc/localtime: timezone data, version 2, 5 gmt time flags, 5 std time flags, no leap seconds, 69 transition times, 5 abbreviation chars'
LOCALTIME_BAD = '/etc/localtime: file not found'

def test_localtime():
    result = system_time.LocalTime(context_wrap(LOCALTIME)).data
    assert result['name'] == '/etc/localtime'
    assert result['version'] == '2'
    assert result['gmt_time_flag'] == '5'
    assert result['std_time_flag'] == '5'
    assert result['leap_second'] == 'no'
    assert result['transition_time'] == '69'
    assert result['abbreviation_char'] == '5'


def test_bad_localtime():
    result = system_time.LocalTime(context_wrap(LOCALTIME_BAD)).data
    assert result == {'name': '/etc/localtime'}


NTPTIME = ('\nntp_gettime() returns code 0 (OK)\n  time dbbc595d.1adbd720  Thu, Oct 27 2016 18:45:49.104, (.104917550),\n  maximum error 263240 us, estimated error 102 us, TAI offset 0\nntp_adjtime() returns code 0 (OK)\n  modes 0x0 (),\n  offset 0.000 us, frequency 4.201 ppm, interval 1 s,\n  maximum error 263240 us, estimated error 102 us,\n  status 0x2011 (PLL,INS,NANO),\n  time constant 2, precision 0.001 us, tolerance 500 ppm,\n').strip()
NTPTIME_STATUS = ('\nntp_gettime() returns code 5 (ERROR)\n  time ddb6c4ae.e3485000  Wed, Nov 15 2017 13:50:38.887, (.887822),\n  maximum error 16000000 us, estimated error 16000000 us, TAI offset 0\nntp_adjtime() returns code 5 (ERROR)\n  modes 0x0 (),\n  offset 0.000 us, frequency 0.000 ppm, interval 1 s,\n  maximum error 16000000 us, estimated error 16000000 us,\n  status 0x50 (INS,UNSYNC),\n  time constant 2, precision 1.000 us, tolerance 500 ppm,\n').strip()

def test_ntptime():
    result = system_time.NtpTime(context_wrap(NTPTIME)).data
    assert result['ntp_gettime'] == '0'
    assert result['ntp_adjtime'] == '0'
    assert result['status'] == '0x2011'
    assert result['flags'] == ['PLL', 'INS', 'NANO']
    assert result['timecode'] == 'dbbc595d.1adbd720'
    assert result['timestamp'] == 'Thu, Oct 27 2016 18:45:49.104, (.104917550)'
    assert result['maximum error'] == 263240
    assert result['estimated error'] == 102
    assert result['TAI offset'] == 0
    assert result['modes'] == 0
    assert result['offset'] == 0.0
    assert result['frequency'] == 4.201
    assert result['interval'] == 1
    assert result['time constant'] == 2
    assert result['precision'] == 0.001
    assert result['tolerance'] == 500


def test_ntptime_status():
    result = system_time.NtpTime(context_wrap(NTPTIME_STATUS)).data
    assert result['ntp_gettime'] == '5'
    assert result['ntp_adjtime'] == '5'
    assert result['status'] == '0x50'
    assert result['flags'] == ['INS', 'UNSYNC']


def test_standard_ntp_conf():
    ntp_obj = system_time.NTPConf(context_wrap(STANDARD_NTP_CONF))
    assert ntp_obj
    assert hasattr(ntp_obj, 'data')
    data = ntp_obj.data
    assert data == {'driftfile': [
                   '/var/lib/ntp/drift'], 
       'restrict': [
                  'default nomodify notrap nopeer noquery',
                  '127.0.0.1',
                  '::1'], 
       'includefile': [
                     '/etc/ntp/crypto/pw'], 
       'keys': [
              '/etc/ntp/keys'], 
       'broadcastclient': None, 
       'iburst': None, 
       'server': [
                '127.127.1.0',
                '10.20.30.40',
                '192.168.1.111'], 
       'fudge': [
               '127.127.1.0 stratum 10'], 
       'peer': [
              'ntp1.example.com',
              'ntp2.example.com',
              'ntp3.example.com']}
    assert hasattr(ntp_obj, 'servers')
    assert ntp_obj.servers == [
     '10.20.30.40', '127.127.1.0', '192.168.1.111']
    assert hasattr(ntp_obj, 'peers')
    assert ntp_obj.peers == [
     'ntp1.example.com', 'ntp2.example.com', 'ntp3.example.com']
    assert ntp_obj.get_last('tinker', 'panic') is None
    return


def test_zero_hosts_ntp_conf():
    ntp_obj = system_time.NTPConf(context_wrap(ZERO_HOSTS_NTP_CONF))
    assert ntp_obj
    assert hasattr(ntp_obj, 'data')
    assert ntp_obj.data == {'broadcastclient': None}
    assert hasattr(ntp_obj, 'servers')
    assert ntp_obj.servers == []
    assert hasattr(ntp_obj, 'peers')
    assert ntp_obj.peers == []
    return


def test_ntp_get_tinker():
    ntp_obj = system_time.NTPConf(context_wrap(NTP_TINKER_CONF))
    assert ntp_obj
    assert hasattr(ntp_obj, 'data')
    assert 'tinker' in ntp_obj.data
    assert ntp_obj.get_last('tinker', 'panic') is None
    assert ntp_obj.get_last('tinker', 'step') == '0.4'
    assert ntp_obj.get_last('tinker', 'panic') is None
    assert ntp_obj.get_last('tinker', default='1') == 'step 0.4'
    assert ntp_obj.get_last('tinker', param='panic', default='1') == '1'
    assert ntp_obj.get_last('tinker', 'panic', '1') == '1'
    assert ntp_obj.get_last('tinker', 'step') == '0.4'
    assert ntp_obj.get_last('tinker', param='step', default='1') == '0.4'
    assert ntp_obj.get_last('tinker', 'step', '1') == '0.4'
    return