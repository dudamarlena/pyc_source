# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_smartpdc_settings.py
# Compiled at: 2019-05-16 13:41:33
import doctest
from insights.parsers import smartpdc_settings
from insights.parsers.smartpdc_settings import SmartpdcSettings
from insights.tests import context_wrap
SMARTPDC_SETTINGS = '\n# Path to dynflow database, leave blank for in-memory non-persistent database\n:database:\n:console_auth: true\n\n# URL of the foreman, used for reporting back\n:foreman_url: https://test.example.com\n\n# SSL settings for client authentication against foreman.\n:foreman_ssl_ca: /etc/foreman-proxy/foreman_ssl_ca.pem\n:foreman_ssl_cert: /etc/foreman-proxy/foreman_ssl_cert.pem\n:foreman_ssl_key: /etc/foreman-proxy/foreman_ssl_key.pem\n\n# Listen on address\n:listen: 0.0.0.0\n\n# Listen on port\n:port: 8008\n\n:use_https: true\n:ssl_ca_file: /etc/foreman-proxy/ssl_ca.pem\n'

def test_smartpdc_settings():
    smartpdc_settings = SmartpdcSettings(context_wrap(SMARTPDC_SETTINGS))
    assert smartpdc_settings.data[':listen'] == '0.0.0.0'
    assert ('/etc/foreman-proxy/foreman_ssl_ca.pem' in smartpdc_settings.data[':foreman_ssl_ca']) is True


def test_ls_smartpdc_settings_doc_examples():
    env = {'smartpdc_settings': SmartpdcSettings(context_wrap(SMARTPDC_SETTINGS))}
    failed, total = doctest.testmod(smartpdc_settings, globs=env)
    assert failed == 0