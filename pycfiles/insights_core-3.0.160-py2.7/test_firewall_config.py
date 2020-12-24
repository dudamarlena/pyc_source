# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_firewall_config.py
# Compiled at: 2020-03-25 13:10:41
import doctest, pytest
from insights.parsers import firewall_config
from insights.parsers.firewall_config import FirewallDConf
from insights.tests import context_wrap
from insights.parsers import SkipException
FIREWALLD_CONFIG = ('\n# firewalld config file\n\n# default zone\n# The default zone used if an empty zone string is used.\n# Default: public\nDefaultZone=public\n\n# Minimal mark\n# Marks up to this minimum are free for use for example in the direct\n# interface. If more free marks are needed, increase the minimum\n# Default: 100\nMinimalMark=100\n\n# Clean up on exit\n# If set to no or false the firewall configuration will not get cleaned up\n# on exit or stop of firewalld\n# Default: yes\nCleanupOnExit=yes\n\n\n').strip()
FIREWALLD_CONFIG_2 = ('\n').strip()

def test_docs():
    env = {'firewalld': FirewallDConf(context_wrap(FIREWALLD_CONFIG))}
    failed, total = doctest.testmod(firewall_config, globs=env)
    assert failed == 0


def test_empty_content():
    with pytest.raises(SkipException):
        FirewallDConf(context_wrap(FIREWALLD_CONFIG_2))