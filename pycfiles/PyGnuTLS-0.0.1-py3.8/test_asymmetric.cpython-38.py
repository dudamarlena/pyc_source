# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/PyGnuTLS/tests/test_asymmetric.py
# Compiled at: 2020-04-24 09:26:03
# Size of source mod 2**32: 4183 bytes
import hashlib, unittest
from PyGnuTLS.crypto import PrivateKey, RSAPrivateKey
from PyGnuTLS.errors import GNUTLSError
from PyGnuTLS.library.constants import GNUTLS_PK_RSA, GNUTLS_DIG_SHA1, GNUTLS_DIG_SHA256, GNUTLS_DIG_SHA512, GNUTLS_SIGN_RSA_SHA1, GNUTLS_SIGN_RSA_SHA256, GNUTLS_SIGN_RSA_SHA512, GNUTLS_PK_DSA, GNUTLS_SIGN_DSA_SHA1, GNUTLS_SIGN_DSA_SHA256, GNUTLS_SIGN_DSA_SHA512, GNUTLS_VERIFY_ALLOW_BROKEN

def is_tpm_not_available_error(err_message):
    errors = [
     'TPM key was not found in persistent storage.',
     'Cannot initialize a session with the TPM.',
     'An unimplemented or disabled feature has been requested.']
    for error in errors:
        if err_message.find(error) >= 0:
            return True
        return False


class TestSigning(unittest.TestCase):

    def test_generate_rsa_and_sign(self):
        teststring = b'foobar'
        for bits in (1024, 2048):
            privkey = PrivateKey.generate(algo=GNUTLS_PK_RSA, bits=bits)
            pubkey = privkey.get_public_key()
            for hash_algo, sign_algo, hashfunc in (
             (
              GNUTLS_DIG_SHA256, GNUTLS_SIGN_RSA_SHA256, hashlib.sha256),
             (
              GNUTLS_DIG_SHA1, GNUTLS_SIGN_RSA_SHA1, hashlib.sha1),
             (
              GNUTLS_DIG_SHA512, GNUTLS_SIGN_RSA_SHA512, hashlib.sha512)):
                signature = privkey.sign_data(hash_algo, 0, teststring)
                self.assertEqual(len(signature), bits / 8)
                pubkey.verify_data2(sign_algo, 0, teststring, signature)
                myhash = hashfunc(teststring).digest()
                pubkey.verify_hash2(sign_algo, 0, myhash, signature)
                signature2 = privkey.sign_hash(hash_algo, 0, myhash)
                self.assertEqual(len(signature2), bits / 8)
                pubkey.verify_hash2(sign_algo, 0, myhash, signature2)

    def test_generate_dsa_and_sign(self):
        teststring = b'foobar'
        for bits in (2048, ):
            privkey = PrivateKey.generate(GNUTLS_PK_DSA, bits)
            pubkey = privkey.get_public_key()
            for hash_algo, sign_algo, hashfunc in (
             (
              GNUTLS_DIG_SHA256, GNUTLS_SIGN_DSA_SHA256, hashlib.sha256),
             (
              GNUTLS_DIG_SHA1, GNUTLS_SIGN_DSA_SHA1, hashlib.sha1),
             (
              GNUTLS_DIG_SHA512, GNUTLS_SIGN_DSA_SHA512, hashlib.sha512)):
                signature = privkey.sign_data(hash_algo, 0, teststring)
                pubkey.verify_data2(sign_algo, GNUTLS_VERIFY_ALLOW_BROKEN, teststring, signature)
                myhash = hashfunc(teststring).digest()
                pubkey.verify_hash2(sign_algo, GNUTLS_VERIFY_ALLOW_BROKEN, myhash, signature)
                signature2 = privkey.sign_hash(hash_algo, 0, myhash)
                pubkey.verify_hash2(sign_algo, GNUTLS_VERIFY_ALLOW_BROKEN, myhash, signature2)

    def test_tpmkey_sign--- This code section failed: ---

 L.  87         0  LOAD_CONST               b'foobar'
                2  STORE_FAST               'teststring'

 L.  89         4  SETUP_FINALLY        20  'to 20'

 L.  90         6  LOAD_GLOBAL              PrivateKey
                8  LOAD_METHOD              import_uri

 L.  91        10  LOAD_STR                 'tpmkey:uuid=e93a2bc9-6777-467c-8704-c7b25ca7c45b;storage=system'

 L.  90        12  CALL_METHOD_1         1  ''
               14  STORE_FAST               'privkey'
               16  POP_BLOCK        
               18  JUMP_FORWARD         88  'to 88'
             20_0  COME_FROM_FINALLY     4  '4'

 L.  93        20  DUP_TOP          
               22  LOAD_GLOBAL              GNUTLSError
               24  COMPARE_OP               exception-match
               26  POP_JUMP_IF_FALSE    86  'to 86'
               28  POP_TOP          
               30  STORE_FAST               'ex'
               32  POP_TOP          
               34  SETUP_FINALLY        74  'to 74'

 L.  94        36  LOAD_GLOBAL              is_tpm_not_available_error
               38  LOAD_GLOBAL              str
               40  LOAD_FAST                'ex'
               42  CALL_FUNCTION_1       1  ''
               44  CALL_FUNCTION_1       1  ''
               46  POP_JUMP_IF_FALSE    66  'to 66'

 L.  95        48  LOAD_GLOBAL              unittest
               50  LOAD_METHOD              skip
               52  LOAD_STR                 'Key not available'
               54  CALL_METHOD_1         1  ''
               56  ROT_FOUR         
               58  POP_BLOCK        
               60  POP_EXCEPT       
               62  CALL_FINALLY         74  'to 74'
               64  RETURN_VALUE     
             66_0  COME_FROM            46  '46'

 L.  96        66  LOAD_FAST                'ex'
               68  RAISE_VARARGS_1       1  'exception instance'
               70  POP_BLOCK        
               72  BEGIN_FINALLY    
             74_0  COME_FROM            62  '62'
             74_1  COME_FROM_FINALLY    34  '34'
               74  LOAD_CONST               None
               76  STORE_FAST               'ex'
               78  DELETE_FAST              'ex'
               80  END_FINALLY      
               82  POP_EXCEPT       
               84  JUMP_FORWARD         88  'to 88'
             86_0  COME_FROM            26  '26'
               86  END_FINALLY      
             88_0  COME_FROM            84  '84'
             88_1  COME_FROM            18  '18'

 L.  97        88  LOAD_FAST                'privkey'
               90  LOAD_METHOD              sign_data
               92  LOAD_GLOBAL              GNUTLS_DIG_SHA1
               94  LOAD_CONST               0
               96  LOAD_FAST                'teststring'
               98  CALL_METHOD_3         3  ''
              100  STORE_FAST               'signature'

 L.  98       102  LOAD_FAST                'self'
              104  LOAD_METHOD              assertEqual
              106  LOAD_GLOBAL              len
              108  LOAD_FAST                'signature'
              110  CALL_FUNCTION_1       1  ''
              112  LOAD_CONST               256
              114  CALL_METHOD_2         2  ''
              116  POP_TOP          

 L.  99       118  LOAD_FAST                'privkey'
              120  LOAD_METHOD              get_public_key
              122  CALL_METHOD_0         0  ''
              124  STORE_FAST               'pubkey'

 L. 100       126  LOAD_FAST                'pubkey'
              128  LOAD_METHOD              verify_data2
              130  LOAD_GLOBAL              GNUTLS_SIGN_RSA_SHA1
              132  LOAD_CONST               0
              134  LOAD_FAST                'teststring'
              136  LOAD_FAST                'signature'
              138  CALL_METHOD_4         4  ''
              140  POP_TOP          

Parse error at or near `POP_BLOCK' instruction at offset 58


class TestEncryption(unittest.TestCase):

    def test_generate_rsa_and_encrypt(self):
        teststring = b'foobar'
        for bits in (1024, 2048):
            privkey = RSAPrivateKey.generate(bits=bits)
            pubkey = privkey.get_public_key()
            enc_data = pubkey.encrypt_data(0, teststring)
            self.assertEqual(len(enc_data), bits / 8)
            plaintext = privkey.decrypt_data(0, enc_data)
            self.assertEqual(plaintext, teststring)


if __name__ == '__main__':
    unittest.main()