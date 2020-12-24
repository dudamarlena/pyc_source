# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_neutron_metadata_agent_conf.py
# Compiled at: 2019-05-16 13:41:33
import doctest
from insights.parsers import neutron_metadata_agent_conf
from insights.parsers.neutron_metadata_agent_conf import NeutronMetadataAgentIni
from insights.tests import context_wrap
METADATA_AGENT_INI = ("\n[DEFAULT]\n# Show debugging output in log (sets DEBUG log level output)\n# debug = True\ndebug = False\n\n# The Neutron user information for accessing the Neutron API.\nauth_url = http://localhost:35357/v2.0\n# Turn off verification of the certificate for ssl\n# auth_insecure = False\nauth_insecure = False\n# Certificate Authority public key (CA cert) file for ssl\n# auth_ca_cert =\nadmin_tenant_name = service\nadmin_user = neutron\nadmin_password = *********\n\n# Network service endpoint type to pull from the keystone catalog\n# endpoint_type = adminURL\n\n# IP address used by Nova metadata server\n# nova_metadata_ip = 127.0.0.1\nnova_metadata_ip = 127.0.0.1\n\n# TCP Port used by Nova metadata server\n# nova_metadata_port = 8775\nnova_metadata_port = 8775\n\n# Which protocol to use for requests to Nova metadata server, http or https\n# nova_metadata_protocol = http\nnova_metadata_protocol = http\n\n# Whether insecure SSL connection should be accepted for Nova metadata server\n# requests\n# nova_metadata_insecure = False\n\n# Client certificate for nova api, needed when nova api requires client\n# certificates\n# nova_client_cert =\n\n# Private key for nova client certificate\n# nova_client_priv_key =\n\n# When proxying metadata requests, Neutron signs the Instance-ID header with a\n# shared secret to prevent spoofing.  You may select any string for a secret,\n# but it must match here and in the configuration used by the Nova Metadata\n# Server. NOTE: Nova uses the same config key, but in [neutron] section.\n# metadata_proxy_shared_secret =\nmetadata_proxy_shared_secret =*********\n\n# Location of Metadata Proxy UNIX domain socket\n# metadata_proxy_socket = $state_path/metadata_proxy\n\n# Metadata Proxy UNIX domain socket mode, 4 values allowed:\n# 'deduce': deduce mode from metadata_proxy_user/group values,\n# 'user': set metadata proxy socket mode to 0o644, to use when\n# metadata_proxy_user is agent effective user or root,\n# 'group': set metadata proxy socket mode to 0o664, to use when\n# metadata_proxy_group is agent effective group,\n# 'all': set metadata proxy socket mode to 0o666, to use otherwise.\n# metadata_proxy_socket_mode = deduce\n\n# Number of separate worker processes for metadata server. Defaults to\n# half the number of CPU cores\n# metadata_workers =\nmetadata_workers =0\n\n# Number of backlog requests to configure the metadata server socket with\n# metadata_backlog = 4096\nmetadata_backlog = 4096\n\n# URL to connect to the cache backend.\n# default_ttl=0 parameter will cause cache entries to never expire.\n# Otherwise default_ttl specifies time in seconds a cache entry is valid for.\n# No cache is used in case no value is passed.\n# cache_url = memory://?default_ttl=5\ncache_url = memory://?default_ttl=5\n\n[AGENT]\n# Log agent heartbeats from this Metadata agent\nlog_agent_heartbeats = False\n").strip()

def test_neutron_metadata_agent_ini():
    nmda_ini = NeutronMetadataAgentIni(context_wrap(METADATA_AGENT_INI))
    assert nmda_ini.has_option('AGENT', 'log_agent_heartbeats')
    assert nmda_ini.get('DEFAULT', 'auth_url') == 'http://localhost:35357/v2.0'
    assert nmda_ini.getint('DEFAULT', 'metadata_backlog') == 4096


def test_doc():
    env = {'metadata_agent_ini': NeutronMetadataAgentIni(context_wrap(METADATA_AGENT_INI, path='/etc/neutron/metadata_agent.ini'))}
    failed, total = doctest.testmod(neutron_metadata_agent_conf, globs=env)
    assert failed == 0