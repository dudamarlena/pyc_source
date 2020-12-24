# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\common\myecdsa256.py
# Compiled at: 2020-04-23 03:22:32
# Size of source mod 2**32: 3482 bytes
import os, base64, hashlib
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_private_key, Encoding, PrivateFormat
from cryptography.x509 import load_pem_x509_certificate, NameOID
from hfc.util.crypto.crypto import Ecies, ecies, CURVE_P_256_Size, SHA2
from cryptography import x509
from cryptography.hazmat.primitives import serialization

def ecdsa_sign(message, key_data):
    """
        :param message: 待签名字符串
        :param pri_key_file_name: 用户私钥路径
        :return: 返回base64编码格式的签名值
        """
    skey = load_pem_private_key(key_data, password=None, backend=(default_backend()))
    signature = Ecies(CURVE_P_256_Size, SHA2).sign(private_key=skey, message=message)
    return signature


def ecdsa_verify(message, signature, key_data):
    """
        :param message: 待签名字符串
        :param signature: 返回报文中的 mac值
        :param pub_key_file: 网关公钥路径
        :return: 返回 True or False
        """
    cert = load_pem_x509_certificate(key_data, default_backend())
    public_key = cert.public_key()
    mac = signature
    verify_results = Ecies().verify(public_key=public_key, message=(message.encode('utf-8')), signature=(base64.b64decode(mac)))
    return verify_results


def certificate_request(name, save_path):
    ecies256 = ecies()
    private_key = ecies256.generate_private_key()
    csr = ecies256.generate_csr(private_key, x509.Name([
     x509.NameAttribute(NameOID.COMMON_NAME, name)]))
    csr_pem = csr.public_bytes(Encoding.PEM)
    sk_pem = private_key.private_bytes(Encoding.PEM, PrivateFormat.PKCS8, serialization.NoEncryption())
    with open(save_path, mode='wb') as (f):
        f.write(sk_pem)
    return (
     csr_pem, save_path)


def hash256_sign(o_str):
    sha256 = hashlib.sha256()
    sha256.update(o_str.encode('utf-8'))
    return sha256.hexdigest()


if __name__ == '__main__':
    o_str = 'USER0001202004151958010871292app00012020041610201529184510364a7ce7c1f7c3fb7afb3ea2b9c678ed3dfd5e7c61ae72c4541822646fd24a19'
    print(hash256_sign(o_str))