# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_krb5.py
# Compiled at: 2019-11-14 13:57:46
from insights.parsers import krb5
from insights.tests import context_wrap
KRB5CONFIG = ('\n# Configuration snippets may be placed in this directory as well\nincludedir /etc/krb5.conf.d/\ninclude /etc/krb5test.conf\nmodule /etc/krb5test.conf:residual\n\n[logging]\n default = FILE:/var/log/krb5libs.log\n kdc = FILE:/var/log/krb5kdc.log\n admin_server = FILE:/var/log/kadmind.log\n\n[realms]\n dns_lookup_realm = false\n default_ccache_name = KEYRING:persistent:%{uid}\n default_ccache_name2 = KEYRING:%{uid}:persistent\n kdc_default_options = default.example.com\n kdc_default_options = default2.example.com\n EXAMPLE.COM = {\n  kdc = kerberos.example.com\n  admin_server = kerberos.example.com\n  auth_to_local = RULE:[1:$1@$0](.*@.*EXAMPLE.ORG)s/@.*//\n }\n EXAMPLE4.COM = {\n  kdc = kerberos.example4.com\n  admin_server = kerberos.example4.com\n }\n ticket_lifetime = 24h\n[libdefaults]\n dnsdsd = false\n tilnvs = 24h\n default_ccache_name = KEYRING:%{uid}:persistent\n EXAMPLE2.COM = {\n  kdc = kerberos.example2.com\n  admin_server = kerberos.example2.com\n }\n EXAMPLE3.COM = {\n  kdc = kerberos.example3.com\n  admin_server = kerberos.example3.com *\n }\n# renew_lifetime = 7d\n# forwardable = true\n# rdns = false\n').strip()
KRB5CONFIG2 = ('\n# Configuration snippets may be placed in this directory as well\n').strip()
KRB5DCONFIG = ('\n# Configuration snippets may be placed in this directory as well\n\n[logging]\n default = FILE:/var/log/krb5libs.log\n kdc = FILE:/var/log/krb5kdc.log\n\n[realms]\n dns_lookup_realm = false\n ticket_lifetime = 24h\n# default_ccache_name = KEYRING:persistent:%{uid}\n EXAMPLE.COM = {\n  kdc = kerberos.example.com\n  kdc = test2.example.com\n  kdc = test3.example.com\n  admin_server = kerberos.example.com\n }\n\n[logging]\n default = FILE:/var/log/krb5libs.log\n kdc = FILE:/var/log/krb5kdc.log *\n admin_server = FILE:/var/log/kadmind.log\n kdc = FILE:/var/log/krb5kdc.log2\n').strip()
KRB5CONFIG3 = ('\n[logging]\n default = FILE:/var/log/krb5libs.log\n kdc = FILE:/var/log/krb5kdc.log\n admin_server = FILE:/var/log/kadmind.log\n\n[libdefaults]\n dns_lookup_realm = false\n ticket_lifetime = 24h\n renew_lifetime = 7d\n forwardable = true\n rdns = false\n# default_realm = EXAMPLE.COM\n default_ccache_name = KEYRING:persistent:%{uid}\n\n[realms]\n# EXAMPLE.COM = {\n#  kdc = kerberos.example.com\n#  admin_server = kerberos.example.com\n# }\n\n[domain_realm]\n# .example.com = EXAMPLE.COM\n# example.com = EXAMPLE.COM\n').strip()
KRB5_CONF_PATH = 'etc/krb5.conf'
KRB5_DCONF_PATH = 'etc/krb5.conf.d/test.conf'

def test_krb5configuration():
    common_conf_info = krb5.Krb5Configuration(context_wrap(KRB5CONFIG, path=KRB5_CONF_PATH))
    assert common_conf_info['libdefaults']['dnsdsd'] == 'false'
    assert 'renew_lifetime' not in common_conf_info.data.keys()
    assert common_conf_info['realms']['EXAMPLE.COM']['kdc'] == 'kerberos.example.com'
    assert common_conf_info['realms']['default_ccache_name'] == 'KEYRING:persistent:%{uid}'
    assert common_conf_info['libdefaults']['default_ccache_name'] == 'KEYRING:%{uid}:persistent'
    assert common_conf_info['realms']['kdc_default_options'] == ['default.example.com', 'default2.example.com']
    assert 'realms' in common_conf_info.sections()
    assert 'realmstest' not in common_conf_info.sections()
    assert common_conf_info.has_section('realms')
    assert not common_conf_info.has_option('realms', 'nosuchoption')
    assert not common_conf_info.has_option('nosucsection', 'nosuchoption')
    assert not common_conf_info.options('realmsno')
    assert sorted(common_conf_info.options('logging')) == sorted(['default', 'admin_server', 'kdc'])
    assert common_conf_info.include == ['/etc/krb5test.conf']
    assert common_conf_info.includedir == ['/etc/krb5.conf.d/']
    assert common_conf_info.module == ['/etc/krb5test.conf:residual']
    common_conf_info = krb5.Krb5Configuration(context_wrap(KRB5CONFIG3, path=KRB5_CONF_PATH))
    assert len(common_conf_info.sections()) == 4
    assert common_conf_info.has_section('domain_realm') is True
    assert sorted(common_conf_info.options('logging')) == sorted(['default', 'kdc', 'admin_server'])
    assert common_conf_info.has_option('libdefaults', 'dns_lookup_realm') is True
    assert common_conf_info.has_option('domain_realm', 'example.com') is False


def test2_krb5configuration():
    common_conf_info = krb5.Krb5Configuration(context_wrap(KRB5CONFIG2, path=KRB5_CONF_PATH))
    assert common_conf_info.data == {}


def test_krb5Dconfiguration():
    common_conf_info = krb5.Krb5Configuration(context_wrap(KRB5DCONFIG, path=KRB5_DCONF_PATH))
    assert common_conf_info['realms']['ticket_lifetime'] == '24h'
    assert 'default_ccache_name' not in common_conf_info.data.keys()
    assert common_conf_info['realms']['EXAMPLE.COM']['kdc'] == ['kerberos.example.com', 'test2.example.com', 'test3.example.com']
    assert common_conf_info.has_option('logging', 'admin_server')
    assert common_conf_info['logging']['kdc'] == 'FILE:/var/log/krb5kdc.log'