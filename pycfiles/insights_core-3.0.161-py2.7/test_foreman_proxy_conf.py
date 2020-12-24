# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_foreman_proxy_conf.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.foreman_proxy_conf import ForemanProxyConf
from insights.tests import context_wrap
conf_content = ("\n---\n### File managed with puppet ###\n## Module:           'foreman_proxy'\n\n:settings_directory: /etc/foreman-proxy/settings.d\n\n# SSL Setup\n\n# if enabled, all communication would be verfied via SSL\n# NOTE that both certificates need to be signed by the same CA in order for this to work\n# see http://theforeman.org/projects/smart-proxy/wiki/SSL for more information\n:ssl_ca_file: /etc/foreman-proxy/ssl_ca.pem\n:ssl_certificate: /etc/foreman-proxy/ssl_cert.pem\n:ssl_private_key: /etc/foreman-proxy/ssl_key.pem\n\n# the hosts which the proxy accepts connections from\n# commenting the following lines would mean every verified SSL connection allowed\n:trusted_hosts:\n - xxx-eopv.xxx.com\n - xxx-eopv.xxx.com\n\n# Endpoint for reverse communication\n:foreman_url: https://xxx-eopv.xxx.com\n").strip()

def test_settings_yml():
    result = ForemanProxyConf(context_wrap(conf_content))
    assert result.data[':settings_directory'] == '/etc/foreman-proxy/settings.d'
    assert result.data[':ssl_ca_file'] == '/etc/foreman-proxy/ssl_ca.pem'
    assert result.data[':ssl_private_key'] == '/etc/foreman-proxy/ssl_key.pem'
    assert result.data[':foreman_url'] == 'https://xxx-eopv.xxx.com'
    assert result.data[':trusted_hosts'] == ['xxx-eopv.xxx.com', 'xxx-eopv.xxx.com']
    assert 'xxx-eopv.xxx.com' in result.data[':trusted_hosts']