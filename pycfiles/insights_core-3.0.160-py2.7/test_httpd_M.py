# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_httpd_M.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers import httpd_M
from insights.parsers.httpd_M import HttpdM
from insights.tests import context_wrap
from insights.parsers import ParseException
import pytest, doctest
HTTPD_M_RHEL6 = ("\nhttpd.event: apr_sockaddr_info_get() failed for liuxc-rhel6-apache\nhttpd.event: Could not reliably determine the server's fully qualified domain name, using 127.0.0.1 for ServerName\nLoaded Modules:\n core_module (static)\n mpm_event_module (static)\n http_module (static)\n so_module (static)\n auth_basic_module (shared)\n auth_digest_module (shared)\n authn_file_module (shared)\n authn_alias_module (shared)\n authn_anon_module (shared)\n authn_dbm_module (shared)\n authn_default_module (shared)\n authz_host_module (shared)\n authz_user_module (shared)\n authz_owner_module (shared)\n authz_groupfile_module (shared)\n authz_dbm_module (shared)\n authz_default_module (shared)\n ldap_module (shared)\n authnz_ldap_module (shared)\n include_module (shared)\n log_config_module (shared)\nSyntax OK\n").strip()
HTTPD_M_RHEL7 = ("\nAH00558: httpd: Could not reliably determine the server's fully qualified domain name, using fe80::a9:89fd:1fc4:f8d. Set the 'ServerName' directive globally to suppress this message\nLoaded Modules:\n so_module (static)\n http_module (static)\n access_compat_module (shared)\n actions_module (shared)\n alias_module (shared)\n allowmethods_module (shared)\n auth_basic_module (shared)\n auth_digest_module (shared)\n authn_anon_module (shared)\n authn_core_module (shared)\n authn_dbd_module (shared)\n authn_dbm_module (shared)\n authn_file_module (shared)\n").strip()
HTTPD_M_DOC = ('\nLoaded Modules:\n core_module (static)\n http_module (static)\n access_compat_module (shared)\n actions_module (shared)\n alias_module (shared)\nSyntax OK\n').strip()

def test_httpd_M():
    result = HttpdM(context_wrap(HTTPD_M_RHEL6, path='/usr/test/httpd_-M'))
    assert result.httpd_command == '/usr/test/httpd'
    assert sorted(result.loaded_modules) == sorted(result.shared_modules + result.static_modules)
    assert 'core_module' in result
    assert result['core_module'] == 'static'
    result = HttpdM(context_wrap(HTTPD_M_RHEL7, path='/usr/tst/httpd_-M'))
    assert result.httpd_command == '/usr/tst/httpd'
    assert sorted(result.loaded_modules) == sorted(result.shared_modules + result.static_modules)
    assert 'core_module' not in result


def test_httpd_M_exp():
    with pytest.raises(ParseException) as (sc):
        HttpdM(context_wrap(''))
    assert 'Input content is empty.' in str(sc)
    with pytest.raises(ParseException) as (sc):
        HttpdM(context_wrap('HTTPD_M_24'))
    assert 'Input content is not empty but there is no useful parsed data.' in str(sc)


def test_httpd_M_doc():
    env = {'HttpdM': HttpdM, 
       'hm': HttpdM(context_wrap(HTTPD_M_DOC, path='/usr/sbin/httpd_-M'))}
    failed, total = doctest.testmod(httpd_M, globs=env)
    assert failed == 0