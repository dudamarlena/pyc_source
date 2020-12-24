# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_satellite_installer_configurations.py
# Compiled at: 2020-03-25 13:10:41
from insights.parsers import satellite_installer_configurations
from insights.tests import context_wrap
import doctest
CUSTOM_HIERA_CONFIG = '\nmongodb::server::config_data:\n  storage.wiredTiger.engineConfig.cacheSizeGB: 8\napache::mod::prefork::serverlimit: 582\napache::mod::prefork::maxclients: 582\napache::mod::prefork::startservers: 10\n'
CUSTOM_HIERA_CONFIG_2 = "\n---\n# This YAML file lets you set your own custom configuration in Hiera for the\n# installer puppet modules that might not be exposed to users directly through\n# installer arguments.\n#\n# For example, to set 'TraceEnable Off' in Apache, a common requirement for\n# security auditors, add this to this file:\n#\n#   apache::trace_enable: Off\n#\n# Consult the full module documentation on http://forge.puppetlabs.com,\n# or the actual puppet classes themselves, to discover options to configure.\n#\n# Do note, setting some values may have unintended consequences that affect the\n# performance or functionality of the application. Consider the impact of your\n# changes before applying them, and test them in a non-production environment\n# first.\n#\n# Here are some examples of how you tune the Apache options if needed:\n#\n# apache::mod::prefork::startservers: 8\n\n"

def test_custom_hiera():
    result = satellite_installer_configurations.CustomHiera(context_wrap(CUSTOM_HIERA_CONFIG))
    assert result.data['mongodb::server::config_data']['storage.wiredTiger.engineConfig.cacheSizeGB'] == 8
    assert result.data['apache::mod::prefork::startservers'] == 10
    assert result.data['apache::mod::prefork::maxclients'] == 582
    result = satellite_installer_configurations.CustomHiera(context_wrap(CUSTOM_HIERA_CONFIG_2))
    assert result.data is None
    return


def test_doc():
    env = {'custom_hiera': satellite_installer_configurations.CustomHiera(context_wrap(CUSTOM_HIERA_CONFIG))}
    failed, total = doctest.testmod(satellite_installer_configurations, globs=env)
    assert failed == 0