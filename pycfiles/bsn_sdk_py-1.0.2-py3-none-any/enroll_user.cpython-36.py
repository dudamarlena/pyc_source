# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\client\entity\enroll_user.py
# Compiled at: 2020-04-23 03:19:47
# Size of source mod 2**32: 2145 bytes
from bsn_sdk_py.common import myecdsa256
from bsn_sdk_py.client.config import Config
from bsn_sdk_py.client.entity.bsn_base import BsnBase

class EnrollUser(BsnBase):

    def __init__(self, name, secret):
        self.name = name
        self.secret = secret

    def GetCertificateRequest(self):
        name = self.GetCertName()
        csr_pem, private_path = myecdsa256.certificate_request(name, self.config.mspDir + '\\keystore\\\\' + name + '_private.pem')
        self.config.not_trust_tran_private_path = private_path
        self.csr_pem = csr_pem
        return csr_pem

    def req_body(self):
        csr_pem = self.GetCertificateRequest()
        req_body = {'name':self.name, 
         'secret':self.secret, 
         'csrPem':str(csr_pem, encoding='utf-8')}
        return req_body

    def sign(self):
        sign_str = self.config.user_code + self.config.app_code + self.name + self.secret + str((self.csr_pem), encoding='utf-8')
        mac = self.config.encrypt_sign.sign(sign_str).decode()
        return mac

    def verify(self, res_data):
        verify_str = str(res_data['header']['code']) + res_data['header']['msg'] + str(res_data['body']['cert'])
        signature = res_data['mac']
        return self.config.encrypt_sign.verify(verify_str, signature)

    def GetCertName(self):
        return self.name + '@' + self.config.app_code

    def save_cert_to_file(self, csr_pem: bytes):
        name = self.GetCertName()
        public_path = self.config.mspDir + '\\keystore\\\\' + name + '_cert.pem'
        with open(public_path, mode='wb') as (f):
            f.write(csr_pem)
        assert csr_pem.startswith('-----BEGIN CERTIFICATE-----')