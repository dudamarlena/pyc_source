# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_dnsmasq_config.py
# Compiled at: 2019-11-14 13:57:46
from insights.parsers.dnsmasq_config import DnsmasqConf
from insights.tests import context_wrap
DNSMASQ_CONF_MAIN = ('\n# Listen on this specific port instead of the standard DNS port\n# (53). Setting this to zero completely disables DNS function,\n# leaving only DHCP and/or TFTP.\nport=5353\n\nno-resolv\ndomain-needed\nno-negcache\nmax-cache-ttl=1\nenable-dbus\ndns-forward-max=5000\ncache-size=5000\nbind-dynamic\nexcept-interface=lo\nserver=/in-addr.arpa/127.0.0.1\nserver=/cluster.local/127.0.0.1\n# End of config\n').strip()
DNSMASQ_CONF_FILE_1 = ('\nserver=/in-addr.arpa/127.0.0.1\nserver=/cluster.local/127.0.0.1\n').strip()

def test_dnsmasq_conf():
    result = DnsmasqConf(context_wrap(DNSMASQ_CONF_MAIN, path='/etc/dnsmasq.conf'))
    assert 'no-resolv' in result
    assert result.find('port').value == 5353
    assert len(result.find('server')) == 2
    assert result.find('server')[0].value == '/in-addr.arpa/127.0.0.1'
    assert result.find('bind-dynamic')[0].name == 'bind-dynamic'
    assert '# End of config' not in result


def test_dnsmasq_conf_file():
    result = DnsmasqConf(context_wrap(DNSMASQ_CONF_FILE_1, path='/etc/dnsmasq.d/dns-origin.conf'))
    assert len(result['server']) == 2
    assert result['server'][(-1)].value == '/cluster.local/127.0.0.1'