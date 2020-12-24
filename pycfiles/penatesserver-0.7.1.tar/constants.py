# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mgallet/Github/Penates-Server/penatesserver/pki/constants.py
# Compiled at: 2015-10-19 03:33:47
from __future__ import unicode_literals, with_statement, print_function
from django.utils.translation import ugettext as _
__author__ = b'Matthieu gallet'
ENCIPHERMENT = b'Encipherment'
SIGNATURE = b'Signature'
EMAIL = b'Email'
USER = b'User'
CONFIGURATION = b'Configuration'
KERBEROS_DC = b'Kerberos DC'
OCSPSIGNING = b'OCSPSigning'
COMPUTER = b'Computer'
CA = b'CA'
SERVICE = b'Service'
SERVICE_1024 = b'Service1024'
PRINTER = b'Printer'
RESOURCE = b'Resource'
TIME_SERVER = b'Time Server'
CA_TEST = b'CA_TEST'
COMPUTER_TEST = b'Computer_TEST'
TEST_DSA = b'TEST_DSA'
TEST_SHA256 = b'TEST_SHA256'
MD2, MD5, MDC2, SHA1, SHA256, SHA512 = ('md2', 'md5', 'mdc2', 'sha1', 'sha256', 'sha512')
DIGEST_TYPES = ((SHA1, _(b'SHA1')), (MD5, _(b'MD5')), (MDC2, _(b'MDC2')), (SHA256, _(b'SHA256')), (SHA512, _(b'SHA512')))
RSA, DSA = ('rsa', 'dsa')
KEY_TYPES = ((RSA, _(b'RSA')), (DSA, _(b'DSA')))
DES, DES3, CAMELLIA256, CAMELLIA192, AES192, AES256 = ('des', 'des3', 'camellia256',
                                                       'camellia192', 'aes192', 'aes256')
CYPHER_TYPES = ((AES256, _(b'AES 265')), (DES3, _(b'DES 3')), (DES, _(b'DES')), (CAMELLIA192, _(b'Camellia 192')),
 (
  CAMELLIA256, _(b'Camellia 256')), (AES192, _(b'AES 192')))
KEY_LENGTHS = (
 (
  8192, _(b'8192')), (4096, _(b'4096')), (2048, _(b'2048')), (1024, _(b'1024')), (512, _(b'512')),
 (
  256, _(b'256')))
ALT_EMAIL, ALT_DNS, ALT_URI = ('email', 'DNS', 'URI')
ALT_TYPES = ((ALT_EMAIL, _(b'email')), (ALT_URI, _(b'URI')), (ALT_DNS, _(b'DNS')))
CA_FALSE, CA_TRUE = ('CA:FALSE', 'critical, CA:TRUE')
BASIC_CONSTRAINTS = ((CA_FALSE, _(b'CA:FALSE')), (CA_TRUE, _(b'critical, CA:TRUE')))
IDENTIFIER_OPTIONAL, IDENTIFIER_ALWAYS = ('keyid:optional, issuer:optional', 'keyid, issuer:always')
AUTHORITY_KEY_IDENTIFIER = ((IDENTIFIER_ALWAYS, IDENTIFIER_ALWAYS), (IDENTIFIER_OPTIONAL, IDENTIFIER_OPTIONAL))
HASH_IDENTIFIER = b'hash'
SUBJECT_KEY_IDENTIFIER = ((HASH_IDENTIFIER, HASH_IDENTIFIER),)
UNSPECIFIED, KEY_COMPROMISE, CA_COMPROMISE, AFFILIATION_CHANGED, SUPERSEDED, CESSATION_OF_OPERATION, CERTIFICATE_HOLD, REMOVE_FROM_CRL = ('unspecified',
                                                                                                                                          'keyCompromise',
                                                                                                                                          'CACompromise',
                                                                                                                                          'affiliationChanged',
                                                                                                                                          'superseded',
                                                                                                                                          'cessationOfOperation',
                                                                                                                                          'certificateHold',
                                                                                                                                          'removeFromCRL')
CRL_REASONS = (
 (
  UNSPECIFIED, _(b'Unspecified')), (KEY_COMPROMISE, _(b'Compromised key')), (CA_COMPROMISE, _(b'Compromised CA')),
 (
  AFFILIATION_CHANGED, _(b'Changed affiliation')), (SUPERSEDED, _(b'Superseded')),
 (
  CESSATION_OF_OPERATION, _(b'Cessation of operation')),
 (
  CERTIFICATE_HOLD, _(b'Hold certificate')), (REMOVE_FROM_CRL, _(b'Remove from CRL')))
KEY_USAGES = [
 b'keyEncipherment', b'dataEncipherment', b'keyAgreement', b'digitalSignature', b'nonRepudiation',
 b'cRLSign', b'keyCertSign']
NS_CERT_TYPES = [b'client', b'objCA', b'emailCA', b'sslCA', b'server', b'email', b'objsign']
EXTENDED_KEY_USAGES = {b'clientAuth': b'clientAuth', b'emailProtection': b'emailProtection', b'serverAuth': b'serverAuth', b'nsSGC': b'nsSGC', 
   b'1.3.6.1.5.2.3.5': b'KDC Authentication', b'timeStamping': b'timeStamping', b'codeSigning': b'codeSigning', 
   b'OCSPSigning': b'OCSPSigning', b'1.3.6.1.5.2.3.4': b'pkinit KPClientAuth', 
   b'1.3.6.1.4.1.311.20.2.2': b'Microsoft Smart Card Logon', 
   b'1.3.6.1.5.5.7.3.7': b'IP Security User', b'1.3.6.1.5.5.8.2.2': b'IP Security IKE Intermediate', 
   b'1.3.6.1.4.1.311.10.3.12': b'MS document signing', 
   b'1.3.6.1.5.5.7.3.5': b'IP Security End System', b'1.3.6.1.5.5.7.3.6': b'IP Security Tunnel Endpoint'}
ROLES = {TIME_SERVER: {b'authorityKeyIdentifier': IDENTIFIER_ALWAYS, 
                 b'crlDays': 30, b'dsaBits': 4096, b'cypherType': AES256, b'extendedKeyUsage': [
                                     b'clientAuth', b'nsSGC', b'serverAuth', b'timeStamping'], 
                 b'keyUsage': [
                             b'dataEncipherment', b'digitalSignature', b'keyAgreement', b'keyEncipherment', b'nonRepudiation'], 
                 b'digest': SHA256, 
                 b'subjectKeyIdentifier': HASH_IDENTIFIER, b'rsaBits': 4096, b'days': 1000, b'nsCertType': [
                               b'client'], 
                 b'basicConstraints': CA_FALSE, b'keyType': RSA}, 
   RESOURCE: {b'nsCertType': [
                            b'client'], 
              b'authorityKeyIdentifier': IDENTIFIER_ALWAYS, b'crlDays': 30, b'dsaBits': 4096, b'keyUsage': [
                          b'dataEncipherment', b'digitalSignature', b'keyAgreement', b'keyEncipherment'], 
              b'cypherType': AES256, 
              b'extendedKeyUsage': [b'clientAuth'], b'digest': SHA256, b'keyType': RSA, b'subjectKeyIdentifier': HASH_IDENTIFIER, 
              b'rsaBits': 4096, b'days': 1000, b'basicConstraints': CA_FALSE}, 
   PRINTER: {b'nsCertType': [
                           b'client', b'server'], 
             b'authorityKeyIdentifier': IDENTIFIER_ALWAYS, b'crlDays': 30, b'dsaBits': 2048, 
             b'keyUsage': [b'dataEncipherment', b'digitalSignature', b'keyAgreement', b'keyEncipherment'], b'cypherType': AES256, 
             b'extendedKeyUsage': [b'clientAuth', b'serverAuth'], b'digest': SHA256, b'keyType': RSA, b'subjectKeyIdentifier': HASH_IDENTIFIER, 
             b'rsaBits': 2048, b'days': 1000, b'basicConstraints': CA_FALSE}, 
   SERVICE: {b'nsCertType': [
                           b'client', b'server'], 
             b'authorityKeyIdentifier': IDENTIFIER_ALWAYS, b'crlDays': 30, b'dsaBits': 4096, 
             b'keyUsage': [b'dataEncipherment', b'digitalSignature', b'keyAgreement', b'keyEncipherment'], b'cypherType': AES256, 
             b'extendedKeyUsage': [b'clientAuth', b'nsSGC', b'serverAuth'], b'digest': SHA256, b'keyType': RSA, b'subjectKeyIdentifier': HASH_IDENTIFIER, 
             b'rsaBits': 4096, b'days': 1000, b'basicConstraints': CA_FALSE}, 
   SERVICE_1024: {b'nsCertType': [
                                b'client', b'server'], 
                  b'authorityKeyIdentifier': IDENTIFIER_ALWAYS, b'crlDays': 30, b'dsaBits': 1024, 
                  b'keyUsage': [b'dataEncipherment', b'digitalSignature', b'keyAgreement', b'keyEncipherment'], b'cypherType': AES256, 
                  b'extendedKeyUsage': [b'clientAuth', b'nsSGC', b'serverAuth'], b'digest': SHA256, b'keyType': RSA, b'subjectKeyIdentifier': HASH_IDENTIFIER, 
                  b'rsaBits': 1024, b'days': 1000, b'basicConstraints': CA_FALSE}, 
   CA: {b'nsCertType': [
                      b'emailCA', b'objCA', b'sslCA'], 
        b'authorityKeyIdentifier': IDENTIFIER_ALWAYS, b'crlDays': 30, b'dsaBits': 4096, 
        b'keyUsage': [b'cRLSign', b'digitalSignature', b'keyCertSign'], b'cypherType': AES256, b'extendedKeyUsage': [
                            b'serverAuth'], 
        b'digest': SHA256, b'subjectKeyIdentifier': HASH_IDENTIFIER, b'rsaBits': 4096, 
        b'days': 8000, b'basicConstraints': CA_TRUE, b'keyType': RSA}, 
   CA_TEST: {b'nsCertType': [
                           b'emailCA', b'objCA', b'sslCA'], 
             b'authorityKeyIdentifier': IDENTIFIER_ALWAYS, b'crlDays': 30, b'dsaBits': 1024, 
             b'keyUsage': [b'cRLSign', b'digitalSignature', b'keyCertSign'], b'cypherType': AES256, b'extendedKeyUsage': [
                                 b'serverAuth'], 
             b'digest': SHA256, b'subjectKeyIdentifier': HASH_IDENTIFIER, b'rsaBits': 1024, 
             b'days': 8000, b'basicConstraints': CA_TRUE, b'keyType': RSA}, 
   COMPUTER: {b'nsCertType': [
                            b'client'], 
              b'authorityKeyIdentifier': IDENTIFIER_ALWAYS, b'crlDays': 30, b'dsaBits': 4096, b'keyUsage': [
                          b'dataEncipherment', b'digitalSignature', b'keyAgreement', b'keyEncipherment'], 
              b'cypherType': AES256, b'extendedKeyUsage': [
                                  b'clientAuth'], 
              b'digest': SHA256, b'subjectKeyIdentifier': HASH_IDENTIFIER, b'rsaBits': 4096, b'days': 1000, 
              b'basicConstraints': CA_FALSE, b'keyType': RSA}, 
   COMPUTER_TEST: {b'nsCertType': [
                                 b'client'], 
                   b'authorityKeyIdentifier': IDENTIFIER_ALWAYS, b'crlDays': 30, b'dsaBits': 1024, b'keyUsage': [
                               b'dataEncipherment', b'digitalSignature', b'keyAgreement', b'keyEncipherment'], 
                   b'cypherType': DES, b'extendedKeyUsage': [
                                       b'clientAuth'], 
                   b'digest': MD5, b'subjectKeyIdentifier': HASH_IDENTIFIER, b'rsaBits': 1024, b'days': 1000, 
                   b'basicConstraints': CA_FALSE, b'keyType': RSA}, 
   TEST_DSA: {b'nsCertType': [
                            b'client'], 
              b'authorityKeyIdentifier': IDENTIFIER_ALWAYS, b'crlDays': 30, b'dsaBits': 1024, b'keyUsage': [
                          b'dataEncipherment', b'digitalSignature', b'keyAgreement', b'keyEncipherment'], 
              b'cypherType': AES256, b'extendedKeyUsage': [
                                  b'clientAuth'], 
              b'digest': SHA256, b'subjectKeyIdentifier': HASH_IDENTIFIER, b'rsaBits': 1024, b'days': 1000, 
              b'basicConstraints': CA_FALSE, b'keyType': DSA}, 
   TEST_SHA256: {b'nsCertType': [
                               b'client'], 
                 b'authorityKeyIdentifier': IDENTIFIER_ALWAYS, b'crlDays': 30, b'dsaBits': 1024, b'keyUsage': [
                             b'dataEncipherment', b'digitalSignature', b'keyAgreement', b'keyEncipherment'], 
                 b'cypherType': AES256, b'extendedKeyUsage': [
                                     b'clientAuth'], 
                 b'digest': SHA256, b'subjectKeyIdentifier': HASH_IDENTIFIER, b'rsaBits': 1024, b'days': 1000, 
                 b'basicConstraints': CA_FALSE, b'keyType': RSA}, 
   OCSPSIGNING: {b'nsCertType': [
                               b'client', b'server'], 
                 b'authorityKeyIdentifier': IDENTIFIER_ALWAYS, b'crlDays': 30, b'dsaBits': 4096, 
                 b'keyUsage': [b'dataEncipherment', b'digitalSignature', b'keyAgreement', b'keyEncipherment'], b'cypherType': AES256, 
                 b'extendedKeyUsage': [b'OCSPSigning', b'clientAuth', b'nsSGC', b'serverAuth'], b'digest': SHA256, 
                 b'subjectKeyIdentifier': HASH_IDENTIFIER, b'rsaBits': 4096, b'days': 1000, b'basicConstraints': CA_FALSE, 
                 b'keyType': RSA}, 
   KERBEROS_DC: {b'nsCertType': [
                               b'client'], 
                 b'authorityKeyIdentifier': IDENTIFIER_ALWAYS, b'crlDays': 30, b'dsaBits': 4096, b'keyUsage': [
                             b'dataEncipherment', b'digitalSignature', b'keyAgreement', b'keyEncipherment', b'nonRepudiation'], 
                 b'cypherType': AES256, 
                 b'extendedKeyUsage': [b'1.3.6.1.5.2.3.5', b'clientAuth', b'nsSGC', b'serverAuth'], b'digest': SHA256, 
                 b'subjectKeyIdentifier': HASH_IDENTIFIER, b'rsaBits': 4096, b'days': 1000, b'basicConstraints': CA_FALSE, 
                 b'keyType': RSA}, 
   CONFIGURATION: {b'nsCertType': [
                                 b'objsign'], 
                   b'authorityKeyIdentifier': IDENTIFIER_ALWAYS, b'crlDays': 30, b'dsaBits': 4096, b'keyUsage': [
                               b'dataEncipherment', b'digitalSignature', b'keyAgreement', b'keyEncipherment', b'nonRepudiation'], 
                   b'cypherType': AES256, 
                   b'extendedKeyUsage': [b'clientAuth', b'codeSigning', b'nsSGC'], b'digest': SHA256, b'keyType': RSA, 
                   b'subjectKeyIdentifier': HASH_IDENTIFIER, b'rsaBits': 4096, b'days': 1000, b'basicConstraints': CA_FALSE}, 
   USER: {b'nsCertType': [
                        b'client', b'email'], 
          b'authorityKeyIdentifier': IDENTIFIER_ALWAYS, b'crlDays': 30, b'dsaBits': 4096, 
          b'keyUsage': [b'dataEncipherment', b'digitalSignature', b'keyAgreement', b'keyEncipherment'], b'cypherType': AES256, 
          b'basicConstraints': CA_FALSE, b'keyType': RSA, b'extendedKeyUsage': [
                              b'1.3.6.1.4.1.311.10.3.12', b'1.3.6.1.4.1.311.20.2.2', b'1.3.6.1.5.2.3.4',
                              b'1.3.6.1.5.5.7.3.7', b'1.3.6.1.5.5.8.2.2', b'clientAuth', b'emailProtection'], 
          b'digest': SHA256, 
          b'subjectKeyIdentifier': HASH_IDENTIFIER, b'rsaBits': 4096, b'days': 1000}, 
   EMAIL: {b'nsCertType': [
                         b'email'], 
           b'authorityKeyIdentifier': IDENTIFIER_ALWAYS, b'crlDays': 30, b'dsaBits': 4096, 
           b'keyUsage': [b'dataEncipherment'], b'cypherType': AES256, b'extendedKeyUsage': [
                               b'emailProtection'], 
           b'digest': SHA256, b'subjectKeyIdentifier': HASH_IDENTIFIER, b'rsaBits': 4096, 
           b'days': 1000, b'basicConstraints': CA_FALSE, b'keyType': RSA}, 
   SIGNATURE: {b'nsCertType': [], b'authorityKeyIdentifier': IDENTIFIER_ALWAYS, b'crlDays': 30, b'dsaBits': 4096, b'keyUsage': [
                           b'digitalSignature', b'keyAgreement', b'keyEncipherment'], 
               b'cypherType': AES256, b'extendedKeyUsage': [
                                   b'1.3.6.1.4.1.311.10.3.12'], 
               b'digest': SHA256, b'subjectKeyIdentifier': HASH_IDENTIFIER, b'rsaBits': 4096, 
               b'days': 1000, b'basicConstraints': CA_FALSE, b'keyType': RSA}, 
   ENCIPHERMENT: {b'nsCertType': [], b'authorityKeyIdentifier': IDENTIFIER_ALWAYS, b'crlDays': 30, b'dsaBits': 4096, b'keyUsage': [
                              b'dataEncipherment', b'keyEncipherment'], 
                  b'cypherType': AES256, b'extendedKeyUsage': [], b'digest': SHA256, 
                  b'subjectKeyIdentifier': HASH_IDENTIFIER, b'rsaBits': 4096, b'days': 1000, b'basicConstraints': CA_FALSE, 
                  b'keyType': RSA}}