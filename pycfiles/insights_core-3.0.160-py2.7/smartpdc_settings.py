# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/smartpdc_settings.py
# Compiled at: 2019-05-16 13:41:33
"""
SmartpdcSettings - file ``/etc/smart_proxy_dynflow_core/settings.yml``
======================================================================

This module provides parsing for smart_proxy_dynflow_core settings file.
``SmartpdcSettings`` is a parser for ``/etc/smart_proxy_dynflow_core/settings.yml`` files.

Typical output is::

    # Path to dynflow database, leave blank for in-memory non-persistent database
    :database:
    :console_auth: true

    # URL of the foreman, used for reporting back
    :foreman_url: https://test.example.com

    # SSL settings for client authentication against foreman.
    :foreman_ssl_ca: /etc/foreman-proxy/foreman_ssl_ca.pem
    :foreman_ssl_cert: /etc/foreman-proxy/foreman_ssl_cert.pem
    :foreman_ssl_key: /etc/foreman-proxy/foreman_ssl_key.pem

    # Listen on address
    :listen: 0.0.0.0

    # Listen on port
    :port: 8008

Examples:
    >>> smartpdc_settings.data[':foreman_url']
    'https://test.example.com'
    >>> "/etc/foreman-proxy/foreman_ssl_ca.pem" in smartpdc_settings.data[':foreman_ssl_ca']
    True
"""
from insights.specs import Specs
from .. import YAMLParser, parser

@parser(Specs.smartpdc_settings)
class SmartpdcSettings(YAMLParser):
    """ Class for parsing the content of ``/etc/smart_proxy_dynflow_core/settings.yml``."""
    pass