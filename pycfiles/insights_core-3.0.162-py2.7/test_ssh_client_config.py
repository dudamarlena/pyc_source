# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_ssh_client_config.py
# Compiled at: 2019-05-16 13:41:33
import doctest, pytest
from insights.parsers import ssh_client_config as scc, SkipException
from insights.tests import context_wrap
SSH_CONFIG_INPUT = '\n#   ProxyCommand ssh -q -W %h:%p gateway.example.com\n#   RekeyLimit 1G 1h\n#\n# Uncomment this if you want to use .local domain\n# Host *.local\n#   CheckHostIP no\nProxyCommand ssh -q -W %h:%p gateway.example.com\n\nHost *\n    GSSAPIAuthentication yes\n# If this option is set to yes then remote X11 clients will have full access\n# to the original X11 display. As virtually no X11 client supports the untrusted\n# mode correctly we set this to yes.\n    ForwardX11Trusted yes\n# Send locale-related environment variables\n    SendEnv LANG LC_CTYPE LC_NUMERIC LC_TIME LC_COLLATE LC_MONETARY LC_MESSAGES\n    SendEnv LC_PAPER LC_NAME LC_ADDRESS LC_TELEPHONE LC_MEASUREMENT\n    SendEnv LC_IDENTIFICATION LC_ALL LANGUAGE\n    SendEnv XMODIFIERS\n\nHost proxytest\n    HostName 192.168.122.2\n'
SSH_CONFIG_INPUT_EMPTY = '\n#   ProxyCommand ssh -q -W %h:%p gateway.example.com\n#   RekeyLimit 1G 1h\n#\n# Uncomment this if you want to use .local domain\n# Host *.local\n#   CheckHostIP no\n# If this option is set to yes then remote X11 clients will have full access\n# to the original X11 display. As virtually no X11 client supports the untrusted\n# mode correctly we set this to yes.\n# Send locale-related environment variables\n'

def test_ssh_client_config():
    etcsshconfig = scc.EtcSshConfig(context_wrap(SSH_CONFIG_INPUT))
    assert len(etcsshconfig.global_lines) == 1
    assert ('Host_*' in etcsshconfig.host_lines) is True
    assert etcsshconfig.host_lines['Host_*'][0].keyword == 'GSSAPIAuthentication'
    assert etcsshconfig.host_lines['Host_proxytest'][0].value == '192.168.122.2'
    foremansshconfig = scc.ForemanSshConfig(context_wrap(SSH_CONFIG_INPUT))
    assert len(foremansshconfig.global_lines) == 1
    assert ('Host_*' in foremansshconfig.host_lines) is True
    assert foremansshconfig.host_lines['Host_*'][0].keyword == 'GSSAPIAuthentication'
    assert foremansshconfig.host_lines['Host_proxytest'][0].value == '192.168.122.2'


def test_ssh_config_AB():
    with pytest.raises(SkipException):
        scc.ForemanProxySshConfig(context_wrap(SSH_CONFIG_INPUT_EMPTY))


def test_ssh_client_config_docs():
    env = {'etcsshconfig': scc.EtcSshConfig(context_wrap(SSH_CONFIG_INPUT)), 
       'foremansshconfig': scc.ForemanSshConfig(context_wrap(SSH_CONFIG_INPUT)), 
       'foreman_proxy_ssh_config': scc.ForemanProxySshConfig(context_wrap(SSH_CONFIG_INPUT))}
    failed, total = doctest.testmod(scc, globs=env)
    assert failed == 0