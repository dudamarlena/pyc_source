# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_certificates_enddate.py
# Compiled at: 2019-05-16 13:41:33
from datetime import datetime
from insights.parsers.certificates_enddate import CertificatesEnddate
from insights.tests import context_wrap
CRT1 = ("\n/usr/bin/find: '/etc/origin/node': No such file or directory\n/usr/bin/find: '/etc/origin/master': No such file or directory\nnotAfter=May 25 16:39:40 2019 GMT\nFileName= /etc/origin/node/cert.pem\nunable to load certificate\n139881193203616:error:0906D066:PEM routines:PEM_read_bio:bad end line:pem_lib.c:802:\nunable to load certificate\n140695459370912:error:0906D06C:PEM routines:PEM_read_bio:no start line:pem_lib.c:703:Expecting: TRUSTED CERTIFICATE\nnotAfter=May 25 16:39:40 2019 GMT\nFileName= /etc/pki/ca-trust/extracted/pem/email-ca-bundle.pem\nnotAfter=Dec  9 10:55:38 2017 GMT\nFileName= /etc/pki/consumer/cert.pem\nnotAfter=Jan  1 04:59:59 2022 GMT\nFileName= /etc/pki/entitlement/3343502840335059594.pem\nnotAfter=Aug 31 02:19:59 2017 GMT\nFileName= /etc/pki/consumer/cert.pem\nnotAfter=Jan  1 04:59:59 2022 GMT\nFileName= /etc/pki/entitlement/2387590574974617178.pem\n").strip()
CRT2 = ''
CRT3 = ('\nFileName= /etc/origin/node/cert.pem\nnotAfter=May 25 16:39:40 2019 GMT\nFileName= /etc/pki/ca-trust/extracted/pem/email-ca-bundle.pem\nnotAfter=Dec  9 10:55:38 2017 GMT\nFileName= /etc/pki/consumer/cert.pem\n').strip()
CRT4 = ('\nnotAfter=May 25 16:39:40 2019 GMT\nFileName= /etc/pki/ca-trust/extracted/pem/email-ca-bundle.pem\nunable to load certificate\n140463633168248:error:0906D06C:PEM routines:PEM_read_bio:no start line:pem_lib.c:701:Expecting: TRUSTED CERTIFICATE\nnotAfter=Dec  9 10:55:38 2017 GMT\nFileName= /etc/pki/consumer/cert.pem\nnotAfter=Jan  1 04:59:59 2022 GMT\n').strip()
CRT5 = ('\nnotAfter=May 25 16:39:40 2019 GMT\nFileName= /etc/pki/ca-trust/extracted/pem/email-ca-bundle.pem\nnotAfter=Dec  9 10:55:38 2017 GMT\nunable to load certificate\n140463633168248:error:0906D06C:PEM routines:PEM_read_bio:no start line:pem_lib.c:701:Expecting: TRUSTED CERTIFICATE\nFileName= /etc/pki/consumer/cert.pem\nnotAfter=Jan  1 04:59:59 2022 GMT\n').strip()
CRT6 = ('\nnotAfter=May 25 16:39:40 2019\nFileName= /etc/pki/ca-trust/extracted/pem/email-ca-bundle.pem\nnotAfter=Dec  9 10:55:38 20 GMT\nFileName= /etc/pki/consumer/cert.pem\n').strip()
PATH1 = '/etc/origin/node/cert.pem'

def test_certificates_enddate():
    Cert1 = CertificatesEnddate(context_wrap(CRT1))
    assert PATH1 in Cert1.certificates_path
    expiration_date = Cert1.expiration_date(PATH1)
    assert expiration_date.str == 'May 25 16:39:40 2019'
    assert expiration_date.datetime == datetime(2019, 5, 25, 16, 39, 40)
    Cert2 = CertificatesEnddate(context_wrap(CRT2))
    assert Cert2.certificates_path == []
    Cert3 = CertificatesEnddate(context_wrap(CRT3))
    assert set(Cert3.certificates_path) == set([
     '/etc/pki/consumer/cert.pem',
     '/etc/pki/ca-trust/extracted/pem/email-ca-bundle.pem'])
    Cert4 = CertificatesEnddate(context_wrap(CRT4))
    assert set(Cert4.certificates_path) == set([
     '/etc/pki/consumer/cert.pem',
     '/etc/pki/ca-trust/extracted/pem/email-ca-bundle.pem'])
    Cert5 = CertificatesEnddate(context_wrap(CRT5))
    assert set(Cert5.certificates_path) == set([
     '/etc/pki/ca-trust/extracted/pem/email-ca-bundle.pem'])


def test_certificates_enddate_unparsable_datatime():
    Cert6 = CertificatesEnddate(context_wrap(CRT6))
    assert set(Cert6.certificates_path) == set([
     '/etc/pki/consumer/cert.pem',
     '/etc/pki/ca-trust/extracted/pem/email-ca-bundle.pem'])
    assert Cert6.expiration_date('/etc/pki/consumer/cert.pem').datetime is None
    assert Cert6.expiration_date('/etc/pki/ca-trust/extracted/pem/email-ca-bundle.pem').str == 'May 25 16:39:40'
    assert Cert6.expiration_date('/etc/pki/ca-trust/extracted/pem/email-ca-bundle.pem').datetime is None
    assert Cert6.expiration_date('/etc/pki/email-ca-bundle.pem') is None
    return