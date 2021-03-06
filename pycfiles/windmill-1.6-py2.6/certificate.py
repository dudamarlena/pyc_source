# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/windmill/server/certificate.py
# Compiled at: 2011-01-13 01:48:00
import os, datetime
from pkg_resources import resource_string
from tempfile import mkstemp
from OpenSSL import crypto

class SSLCertificateForHost(object):

    def __init__(self, cert_creator, host):
        self.cert_creator = cert_creator
        self.host = host.split(':')[0]
        self.certfile = None
        self._generate()
        return

    def _generate(self):
        self.key = self.cert_creator.master_key
        self.cert = self.cert_creator.generate_cert_for_host(self.host)
        filetype = self.cert_creator.default_filetype
        key_data = crypto.dump_privatekey(filetype, self.key)
        cert_data = crypto.dump_certificate(filetype, self.cert)
        (fd, self.certfile) = mkstemp(suffix='.pem', prefix='windmill-cert-')
        pem = os.fdopen(fd, 'w')
        pem.write(key_data)
        pem.write('\n')
        pem.write(cert_data)
        pem.close()


class CertificateCreator(object):
    default_filetype = crypto.FILETYPE_PEM
    default_digest = 'md5'
    default_key_bits = 1024
    default_key_type = crypto.TYPE_RSA
    master_cert_file = 'sslcerts/master.crt'
    master_cert_req_file = 'sslcerts/master.csr'
    master_key_file = 'sslcerts/master.key'
    master_key_password = 'password'
    serial_number = 1
    certificates = {}

    def __init__(self):
        cert_buf = resource_string(__name__, self.master_cert_file)
        cert_req_buf = resource_string(__name__, self.master_cert_req_file)
        key_buf = resource_string(__name__, self.master_key_file)
        ft = self.default_filetype
        key = crypto.load_privatekey(ft, key_buf, self.master_key_password)
        self.master_key = key
        crt = crypto.load_certificate(ft, cert_buf)
        self.master_cert = crt
        csr = crypto.load_certificate_request(ft, cert_req_buf)
        self.master_cert_req = csr

    def __getitem__(self, host):
        host = host.split(':')[0]
        if host not in self.certificates:
            cert_for_host = SSLCertificateForHost(self, host)
            self.certificates[host] = cert_for_host
        return self.certificates[host]

    def generate_cert_for_host(self, host):
        cert = crypto.X509()
        cert.set_serial_number(self.serial_number)
        self.serial_number += 1
        cert.set_issuer(self.master_cert.get_subject())
        subject = crypto.X509Name(self.master_cert_req.get_subject())
        subject.commonName = host
        cert.set_subject(subject)
        cert.set_pubkey(self.master_cert.get_pubkey())
        today = datetime.datetime.today()
        before = today - datetime.timedelta(days=365)
        after = today + datetime.timedelta(days=365)
        if hasattr(cert, 'set_notBefore'):
            cert.set_notBefore(before.strftime('%Y%m%d%H%M%SZ'))
            cert.set_notAfter(after.strftime('%Y%m%d%H%M%SZ'))
        else:
            cert.gmtime_adj_notBefore(0)
            cert.gmtime_adj_notAfter(315360000)
        cert.sign(self.master_key, self.default_digest)
        return cert