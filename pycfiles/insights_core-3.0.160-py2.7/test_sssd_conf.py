# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_sssd_conf.py
# Compiled at: 2019-05-16 13:41:33
from insights.tests import context_wrap
from insights.parsers.sssd_conf import SSSD_Config
sssd_conf_cnt = '\n\n[sssd]\nconfig_file_version = 2\n\n# Number of times services should attempt to reconnect in the\n# event of a crash or restart before they give up\nreconnection_retries = 3\n\n# If a back end is particularly slow you can raise this timeout here\nsbus_timeout = 30\nservices = nss, pam\n\n# SSSD will not start if you do not configure any domains.\n# Add new domain configurations as [domain/<NAME>] sections, and\n# then add the list of domains (in the order you want them to be\n# queried) to the "domains" attribute below and uncomment it.\n# domains = LOCAL,LDAP\ndomains = example.com\ndebug_level = 9\n\n[nss]\n# The following prevents SSSD from searching for the root user/group in\n# all domains (you can add here a comma-separated list of system accounts that\n# are always going to be /etc/passwd users, or that you want to filter out).\nfilter_groups = root\nfilter_users = root\nreconnection_retries = 3\n\n[pam]\nreconnection_retries = 3\n\n[domain/example.com]\nid_provider = ldap\nlookup_family_order = ipv4_only\nldap_uri = ldap://ldap.example.com/\nldap_search_base = dc=example,dc=com\nenumerate = False\nhbase_directory= /home\ncreate_homedir = True\noverride_homedir = /home/%u\nauth_provider = krb5\nkrb5_server = kerberos.example.com\nkrb5_realm = EXAMPLE.COM\n'
sssd_conf_no_domains = '\n[sssd]\ndebug_level = 5\n'
sssd_conf_blank_domains = '\n[sssd]\ndebug_level = 5\ndomains =\n'

def test_sssd_conf():
    result = SSSD_Config(context_wrap(sssd_conf_cnt))
    assert 'sssd' in result
    assert 'domain/example.com' in result
    assert result.getint('pam', 'reconnection_retries') == 3
    assert [
     'example.com'] == result.domains
    domain = result.domain_config('example.com')
    assert type(domain) == dict
    assert domain['id_provider'] == 'ldap'
    absent_domain = result.domain_config('example.org')
    assert type(absent_domain) == dict
    assert absent_domain == {}


def test_sssd_conf_empty_domains():
    conf = SSSD_Config(context_wrap(sssd_conf_no_domains))
    assert conf.domains == []
    conf = SSSD_Config(context_wrap(sssd_conf_blank_domains))
    assert conf.domains == []