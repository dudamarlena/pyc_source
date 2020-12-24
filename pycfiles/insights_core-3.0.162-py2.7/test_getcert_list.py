# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_getcert_list.py
# Compiled at: 2019-05-16 13:41:33
from insights.tests import context_wrap
from insights.parsers.getcert_list import CertList
from insights.parsers import ParseException
import pytest
CERT_LIST_1 = "\nNumber of certificates and requests being tracked: 8.\nRequest ID '20150522133327':\n        status: MONITORING\n        stuck: no\n        key pair storage: type=NSSDB,location='/etc/dirsrv/slapd-EXAMPLE-COM',nickname='Server-Cert',token='NSS Certificate DB',pinfile='/etc/dirsrv/slapd-EXAMPLE-COM/pwdfile.txt'\n        certificate: type=NSSDB,location='/etc/dirsrv/slapd-EXAMPLE-COM',nickname='Server-Cert',token='NSS Certificate DB'\n        CA: IPA\n        issuer: CN=Certificate Authority,O=EXAMPLE.COM\n        subject: CN=ldap.example.com,O=EXAMPLE.COM\n        expires: 2017-05-22 13:33:27 UTC\n        key usage: digitalSignature,nonRepudiation,keyEncipherment,dataEncipherment\n        eku: id-kp-serverAuth,id-kp-clientAuth\n        pre-save command:\n        post-save command: /usr/lib64/ipa/certmonger/restart_dirsrv EXAMPLE-COM\n        track: yes\n        auto-renew: yes\nRequest ID '20150522133549':\n        status: MONITORING\n        stuck: no\n        key pair storage: type=NSSDB,location='/etc/httpd/alias',nickname='Server-Cert',token='NSS Certificate DB',pinfile='/etc/httpd/alias/pwdfile.txt'\n        certificate: type=NSSDB,location='/etc/httpd/alias',nickname='Server-Cert',token='NSS Certificate DB'\n        CA: IPA\n        issuer: CN=Certificate Authority,O=EXAMPLE.COM\n        subject: CN=ldap.example.com,O=EXAMPLE.COM\n        expires: 2017-05-22 13:35:49 UTC\n        key usage: digitalSignature,nonRepudiation,keyEncipherment,dataEncipherment\n        eku: id-kp-serverAuth,id-kp-clientAuth\n        pre-save command:\n        post-save command: /usr/lib64/ipa/certmonger/restart_httpd\n        track: yes\n        auto-renew: yes\n"

def test_getcert_1():
    certs = CertList(context_wrap(CERT_LIST_1, path='sos_commands/ipa/ipa-getcert_list'))
    assert certs.num_tracked == 8
    assert sorted(certs.requests) == sorted(['20150522133327', '20150522133549'])
    assert len(certs) == 2
    assert '20150522133327' in certs
    assert certs['20150522133327']['status'] == 'MONITORING'
    assert certs['20150522133327']['stuck'] == 'no'
    assert certs['20150522133327']['key pair storage'] == "type=NSSDB,location='/etc/dirsrv/slapd-EXAMPLE-COM',nickname='Server-Cert',token='NSS Certificate DB',pinfile='/etc/dirsrv/slapd-EXAMPLE-COM/pwdfile.txt'"
    assert certs['20150522133327']['certificate'] == "type=NSSDB,location='/etc/dirsrv/slapd-EXAMPLE-COM',nickname='Server-Cert',token='NSS Certificate DB'"
    assert certs['20150522133327']['CA'] == 'IPA'
    assert certs['20150522133327']['issuer'] == 'CN=Certificate Authority,O=EXAMPLE.COM'
    assert certs['20150522133327']['subject'] == 'CN=ldap.example.com,O=EXAMPLE.COM'
    assert certs['20150522133327']['expires'] == '2017-05-22 13:33:27 UTC'
    assert certs['20150522133327']['key usage'] == 'digitalSignature,nonRepudiation,keyEncipherment,dataEncipherment'
    assert certs['20150522133327']['eku'] == 'id-kp-serverAuth,id-kp-clientAuth'
    assert certs['20150522133327']['pre-save command'] == ''
    assert certs['20150522133327']['post-save command'] == '/usr/lib64/ipa/certmonger/restart_dirsrv EXAMPLE-COM'
    assert certs['20150522133327']['track'] == 'yes'
    assert certs['20150522133327']['auto-renew'] == 'yes'
    assert certs.search(stuck='no') == [certs['20150522133327'], certs['20150522133549']]


CERT_BAD_1 = '\nNumber of certificates and requests being tracked: d.\n'
CERT_BAD_2 = "\nNumber of certificates and requests being tracked: 8.\nRequest ID '20150522133327':\n        status: MONITORING\n        stuck: no\nRequest ID '20150522133327':\n        status: MONITORING\n        stuck: no\n"

def test_getcert_exceptions():
    with pytest.raises(ParseException) as (exc):
        assert CertList(context_wrap(CERT_BAD_1)) is None
    assert 'Incorrectly formatted number of certificates and requests' in str(exc)
    with pytest.raises(ParseException) as (exc):
        assert CertList(context_wrap(CERT_BAD_2)) is None
    assert "Found duplicate request ID '20150522133327'" in str(exc)
    return


CERT_BAD_3 = "\nNumber of certificates and requests being tracked: 2.\nRequest ID '20150522133327':\n        status: MONITORING\n        invalid object\n"

def test_getcert_coverage():
    certs = CertList(context_wrap(CERT_BAD_3))
    assert certs
    assert certs.num_tracked == 2
    assert '20150522133327' in certs
    assert certs['20150522133327'] == {'status': 'MONITORING'}