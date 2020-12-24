# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/combiners/tests/test_dnsmasq_conf_all.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.dnsmasq_config import DnsmasqConf
from insights.combiners.dnsmasq_conf_all import DnsmasqConfTree
from insights.tests import context_wrap
DNSMASQ_CONF_MAIN = ('\n# Listen on this specific port instead of the standard DNS port\n# (53). Setting this to zero completely disables DNS function,\n# leaving only DHCP and/or TFTP.\nport=5353\n\nno-resolv\ndomain-needed\nno-negcache\nmax-cache-ttl=1\nenable-dbus\ndns-forward-max=5000\ncache-size=5000\nbind-dynamic\nexcept-interface=lo\nserver=/in-addr.arpa/127.0.0.1\nserver=/cluster.local/127.0.0.1\n# End of config\n').strip()
DNSMASQ_CONF_MAIN_CONF_DIR = ('\n# Listen on this specific port instead of the standard DNS port\n# (53). Setting this to zero completely disables DNS function,\n# leaving only DHCP and/or TFTP.\nport=5353\n\nno-resolv\ndomain-needed\nno-negcache\nmax-cache-ttl=1\nenable-dbus\ndns-forward-max=5000\ncache-size=5000\nbind-dynamic\nexcept-interface=lo\nserver=/in-addr.arpa/127.0.0.1\nserver=/cluster.local/127.0.0.1\nconf-dir=/etc/dnsmasq.d\n# End of config\n').strip()
DNSMASQ_CONF_MAIN_EXCLUDE_CONF_DIR = ('\n# Listen on this specific port instead of the standard DNS port\n# (53). Setting this to zero completely disables DNS function,\n# leaving only DHCP and/or TFTP.\nport=5353\n\nno-resolv\ndomain-needed\nno-negcache\nmax-cache-ttl=1\nenable-dbus\ndns-forward-max=5000\ncache-size=5000\nbind-dynamic\nexcept-interface=lo\nserver=/in-addr.arpa/127.0.0.1\nserver=/cluster.local/127.0.0.1\nconf-dir=/etc/dnsmasq.d,.conf\n# End of config\n').strip()
DNSMASQ_CONF_MAIN_INCLUDE_CONF_DIR = ('\nenable-dbus\ndns-forward-max=5000\ncache-size=5000\nbind-dynamic\nexcept-interface=lo\nserver=/in-addr.arpa/127.0.0.1\nserver=/cluster.local/127.0.0.1\nconf-dir=/etc/dnsmasq.d,*.conf\n# End of config\n').strip()
DNSMASQ_CONF_FILE_1 = ('\nserver=/in-addr.arpa/127.0.0.1\nlog-queries\ntxt-record=example.com,"v=spf1 a -all"\n').strip()
DNSMASQ_CONF_FILE_2 = ('\ndns-forward-max=10000\nno-resolv\ndomain-needed\nno-negcache\nmax-cache-ttl=1\nenable-dbus\n').strip()

def test_no_conf_dir():
    dnsmasq1 = DnsmasqConf(context_wrap(DNSMASQ_CONF_MAIN, path='/etc/dnsmasq.conf'))
    dnsmasq2 = DnsmasqConf(context_wrap(DNSMASQ_CONF_FILE_1, path='/etc/dnsmasq.d/origin-dns.conf'))
    result = DnsmasqConfTree([dnsmasq1, dnsmasq2])
    assert 'domain-needed' in result
    assert 'log-queries' not in result
    assert len(result['server']) == 2


def test_conf_dir():
    dnsmasq1 = DnsmasqConf(context_wrap(DNSMASQ_CONF_MAIN_CONF_DIR, path='/etc/dnsmasq.conf'))
    dnsmasq2 = DnsmasqConf(context_wrap(DNSMASQ_CONF_FILE_1, path='/etc/dnsmasq.d/origin-dns.conf'))
    result = DnsmasqConfTree([dnsmasq1, dnsmasq2])
    assert 'txt-record' in result
    assert len(result['server']) == 3
    dnsmasq1 = DnsmasqConf(context_wrap(DNSMASQ_CONF_MAIN_CONF_DIR, path='/etc/dnsmasq.conf'))
    dnsmasq2 = DnsmasqConf(context_wrap(DNSMASQ_CONF_FILE_2, path='/etc/dnsmasq.d/dns-forward-max.conf'))
    result = DnsmasqConfTree([dnsmasq1, dnsmasq2])
    assert len(result['dns-forward-max']) == 2
    assert result['dns-forward-max'][(-1)].value == 10000


def test_exclude_conf_dir():
    dnsmasq1 = DnsmasqConf(context_wrap(DNSMASQ_CONF_MAIN_EXCLUDE_CONF_DIR, path='/etc/dnsmasq.conf'))
    dnsmasq2 = DnsmasqConf(context_wrap(DNSMASQ_CONF_FILE_1, path='/etc/dnsmasq.d/origin-dns.conf'))
    result = DnsmasqConfTree([dnsmasq1, dnsmasq2])
    assert 'txt-record' not in result
    assert len(result['server']) == 2


def test_include_conf_dir():
    dnsmasq1 = DnsmasqConf(context_wrap(DNSMASQ_CONF_MAIN_INCLUDE_CONF_DIR, path='/etc/dnsmasq.conf'))
    dnsmasq2 = DnsmasqConf(context_wrap(DNSMASQ_CONF_FILE_2, path='/etc/dnsmasq.d/1id-dns.conf'))
    result = DnsmasqConfTree([dnsmasq1, dnsmasq2])
    assert len(result['dns-forward-max']) == 2