# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/PyGnuTLS/tests/test_pkcs7.py
# Compiled at: 2020-04-24 10:52:31
# Size of source mod 2**32: 3197 bytes
import unittest, os, pytest
from PyGnuTLS.crypto import X509Certificate, X509PrivateKey, Pkcs7, X509TrustList
from PyGnuTLS.library.constants import GNUTLS_PKCS7_INCLUDE_CERT, GNUTLS_PKCS7_INCLUDE_TIME, GNUTLS_SIGN_RSA_SHA256, GNUTLS_VERIFY_DISABLE_TIME_CHECKS, GNUTLS_VERIFY_DISABLE_TRUSTED_TIME_CHECKS
from PyGnuTLS.library.errors import GNUTLSError
certs_path = os.path.join('PyGnuTLS', 'tests', 'pkcs7')

class TestPkcs7(unittest.TestCase):

    def test_pkcs7_verify--- This code section failed: ---

 L.  23         0  LOAD_GLOBAL              open
                2  LOAD_GLOBAL              os
                4  LOAD_ATTR                path
                6  LOAD_METHOD              join
                8  LOAD_GLOBAL              certs_path
               10  LOAD_STR                 'LVFS-CA.pem'
               12  CALL_METHOD_2         2  ''
               14  LOAD_STR                 'rb'
               16  CALL_FUNCTION_2       2  ''
               18  SETUP_WITH          108  'to 108'
               20  STORE_FAST               'f'

 L.  24        22  LOAD_GLOBAL              X509Certificate
               24  LOAD_FAST                'f'
               26  LOAD_METHOD              read
               28  CALL_METHOD_0         0  ''
               30  CALL_FUNCTION_1       1  ''
               32  STORE_FAST               'cert'

 L.  25        34  LOAD_FAST                'self'
               36  LOAD_METHOD              assertEqual
               38  LOAD_FAST                'cert'
               40  LOAD_ATTR                issuer
               42  LOAD_STR                 'CN=LVFS CA,O=Linux Vendor Firmware Project'
               44  CALL_METHOD_2         2  ''
               46  POP_TOP          

 L.  26        48  LOAD_FAST                'self'
               50  LOAD_METHOD              assertEqual
               52  LOAD_FAST                'cert'
               54  LOAD_ATTR                serial_number
               56  LOAD_STR                 '1'
               58  CALL_METHOD_2         2  ''
               60  POP_TOP          

 L.  27        62  LOAD_FAST                'self'
               64  LOAD_METHOD              assertEqual
               66  LOAD_FAST                'cert'
               68  LOAD_ATTR                activation_time
               70  LOAD_CONST               1501545600
               72  CALL_METHOD_2         2  ''
               74  POP_TOP          

 L.  28        76  LOAD_FAST                'self'
               78  LOAD_METHOD              assertEqual
               80  LOAD_FAST                'cert'
               82  LOAD_ATTR                expiration_time
               84  LOAD_CONST               2448230400
               86  CALL_METHOD_2         2  ''
               88  POP_TOP          

 L.  29        90  LOAD_FAST                'self'
               92  LOAD_METHOD              assertEqual
               94  LOAD_FAST                'cert'
               96  LOAD_ATTR                version
               98  LOAD_CONST               3
              100  CALL_METHOD_2         2  ''
              102  POP_TOP          
              104  POP_BLOCK        
              106  BEGIN_FINALLY    
            108_0  COME_FROM_WITH       18  '18'
              108  WITH_CLEANUP_START
              110  WITH_CLEANUP_FINISH
              112  END_FINALLY      

 L.  31       114  LOAD_GLOBAL              open
              116  LOAD_GLOBAL              os
              118  LOAD_ATTR                path
              120  LOAD_METHOD              join
              122  LOAD_GLOBAL              certs_path
              124  LOAD_STR                 'firmware.bin'
              126  CALL_METHOD_2         2  ''
              128  LOAD_STR                 'rb'
              130  CALL_FUNCTION_2       2  ''
              132  SETUP_WITH          148  'to 148'
              134  STORE_FAST               'f'

 L.  32       136  LOAD_FAST                'f'
              138  LOAD_METHOD              read
              140  CALL_METHOD_0         0  ''
              142  STORE_FAST               'data'
              144  POP_BLOCK        
              146  BEGIN_FINALLY    
            148_0  COME_FROM_WITH      132  '132'
              148  WITH_CLEANUP_START
              150  WITH_CLEANUP_FINISH
              152  END_FINALLY      

 L.  35       154  LOAD_GLOBAL              open
              156  LOAD_GLOBAL              os
              158  LOAD_ATTR                path
              160  LOAD_METHOD              join
              162  LOAD_GLOBAL              certs_path
              164  LOAD_STR                 'firmware.bin.p7b'
              166  CALL_METHOD_2         2  ''
              168  LOAD_STR                 'rb'
              170  CALL_FUNCTION_2       2  ''
              172  SETUP_WITH          188  'to 188'
              174  STORE_FAST               'f'

 L.  36       176  LOAD_FAST                'f'
              178  LOAD_METHOD              read
              180  CALL_METHOD_0         0  ''
              182  STORE_FAST               'data_sig'
              184  POP_BLOCK        
              186  BEGIN_FINALLY    
            188_0  COME_FROM_WITH      172  '172'
              188  WITH_CLEANUP_START
              190  WITH_CLEANUP_FINISH
              192  END_FINALLY      

 L.  37       194  LOAD_GLOBAL              X509TrustList
              196  CALL_FUNCTION_0       0  ''
              198  STORE_FAST               'tl'

 L.  38       200  LOAD_FAST                'tl'
              202  LOAD_METHOD              add_ca
              204  LOAD_FAST                'cert'
              206  CALL_METHOD_1         1  ''
              208  POP_TOP          

 L.  39       210  LOAD_GLOBAL              Pkcs7
              212  CALL_FUNCTION_0       0  ''
              214  STORE_FAST               'pkcs7'

 L.  40       216  LOAD_FAST                'pkcs7'
              218  LOAD_METHOD              import_signature
              220  LOAD_FAST                'data_sig'
              222  CALL_METHOD_1         1  ''
              224  POP_TOP          

 L.  41       226  LOAD_FAST                'pkcs7'
              228  LOAD_ATTR                verify

 L.  42       230  LOAD_FAST                'tl'

 L.  43       232  LOAD_FAST                'data'

 L.  44       234  LOAD_GLOBAL              GNUTLS_VERIFY_DISABLE_TIME_CHECKS

 L.  45       236  LOAD_GLOBAL              GNUTLS_VERIFY_DISABLE_TRUSTED_TIME_CHECKS

 L.  44       238  BINARY_OR        

 L.  41       240  LOAD_CONST               ('flags',)
              242  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              244  POP_TOP          

 L.  49       246  LOAD_GLOBAL              pytest
              248  LOAD_METHOD              raises
              250  LOAD_GLOBAL              GNUTLSError
              252  CALL_METHOD_1         1  ''
              254  SETUP_WITH          282  'to 282'
              256  POP_TOP          

 L.  50       258  LOAD_FAST                'pkcs7'
              260  LOAD_ATTR                verify

 L.  51       262  LOAD_FAST                'tl'

 L.  52       264  LOAD_CONST               b'FOO'

 L.  53       266  LOAD_GLOBAL              GNUTLS_VERIFY_DISABLE_TIME_CHECKS

 L.  54       268  LOAD_GLOBAL              GNUTLS_VERIFY_DISABLE_TRUSTED_TIME_CHECKS

 L.  53       270  BINARY_OR        

 L.  50       272  LOAD_CONST               ('flags',)
              274  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              276  POP_TOP          
              278  POP_BLOCK        
              280  BEGIN_FINALLY    
            282_0  COME_FROM_WITH      254  '254'
              282  WITH_CLEANUP_START
              284  WITH_CLEANUP_FINISH
              286  END_FINALLY      

Parse error at or near `BEGIN_FINALLY' instruction at offset 106

    def test_pkcs7_self_sign--- This code section failed: ---

 L.  60         0  LOAD_GLOBAL              open
                2  LOAD_GLOBAL              os
                4  LOAD_ATTR                path
                6  LOAD_METHOD              join
                8  LOAD_GLOBAL              certs_path
               10  LOAD_STR                 'test.pem'
               12  CALL_METHOD_2         2  ''
               14  LOAD_STR                 'rb'
               16  CALL_FUNCTION_2       2  ''
               18  SETUP_WITH           38  'to 38'
               20  STORE_FAST               'f'

 L.  61        22  LOAD_GLOBAL              X509Certificate
               24  LOAD_FAST                'f'
               26  LOAD_METHOD              read
               28  CALL_METHOD_0         0  ''
               30  CALL_FUNCTION_1       1  ''
               32  STORE_FAST               'cert'
               34  POP_BLOCK        
               36  BEGIN_FINALLY    
             38_0  COME_FROM_WITH       18  '18'
               38  WITH_CLEANUP_START
               40  WITH_CLEANUP_FINISH
               42  END_FINALLY      

 L.  62        44  LOAD_GLOBAL              open
               46  LOAD_GLOBAL              os
               48  LOAD_ATTR                path
               50  LOAD_METHOD              join
               52  LOAD_GLOBAL              certs_path
               54  LOAD_STR                 'test.key'
               56  CALL_METHOD_2         2  ''
               58  LOAD_STR                 'rb'
               60  CALL_FUNCTION_2       2  ''
               62  SETUP_WITH           82  'to 82'
               64  STORE_FAST               'f'

 L.  63        66  LOAD_GLOBAL              X509PrivateKey
               68  LOAD_FAST                'f'
               70  LOAD_METHOD              read
               72  CALL_METHOD_0         0  ''
               74  CALL_FUNCTION_1       1  ''
               76  STORE_FAST               'privkey'
               78  POP_BLOCK        
               80  BEGIN_FINALLY    
             82_0  COME_FROM_WITH       62  '62'
               82  WITH_CLEANUP_START
               84  WITH_CLEANUP_FINISH
               86  END_FINALLY      

 L.  65        88  LOAD_CONST               b'Hello World!'
               90  STORE_FAST               'data'

 L.  66        92  LOAD_GLOBAL              Pkcs7
               94  CALL_FUNCTION_0       0  ''
               96  STORE_FAST               'pkcs7'

 L.  67        98  LOAD_FAST                'pkcs7'
              100  LOAD_ATTR                sign

 L.  68       102  LOAD_FAST                'cert'

 L.  69       104  LOAD_FAST                'privkey'

 L.  70       106  LOAD_FAST                'data'

 L.  71       108  LOAD_GLOBAL              GNUTLS_PKCS7_INCLUDE_TIME
              110  LOAD_GLOBAL              GNUTLS_PKCS7_INCLUDE_CERT
              112  BINARY_OR        

 L.  67       114  LOAD_CONST               ('flags',)
              116  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              118  POP_TOP          

 L.  73       120  LOAD_FAST                'pkcs7'
              122  LOAD_METHOD              export
              124  CALL_METHOD_0         0  ''
              126  STORE_FAST               'data_sig'

 L.  74       128  LOAD_GLOBAL              Pkcs7
              130  CALL_FUNCTION_0       0  ''
              132  STORE_FAST               'pkcs7'

 L.  75       134  LOAD_FAST                'pkcs7'
              136  LOAD_METHOD              import_signature
              138  LOAD_FAST                'data_sig'
              140  CALL_METHOD_1         1  ''
              142  POP_TOP          

 L.  76       144  LOAD_FAST                'pkcs7'
              146  LOAD_METHOD              verify_direct
              148  LOAD_FAST                'cert'
              150  LOAD_FAST                'data'
              152  CALL_METHOD_2         2  ''
              154  POP_TOP          

Parse error at or near `BEGIN_FINALLY' instruction at offset 36

    def test_pkcs7_signature--- This code section failed: ---

 L.  80         0  LOAD_GLOBAL              open
                2  LOAD_GLOBAL              os
                4  LOAD_ATTR                path
                6  LOAD_METHOD              join
                8  LOAD_GLOBAL              certs_path
               10  LOAD_STR                 'firmware.bin.p7b'
               12  CALL_METHOD_2         2  ''
               14  LOAD_STR                 'rb'
               16  CALL_FUNCTION_2       2  ''
               18  SETUP_WITH           34  'to 34'
               20  STORE_FAST               'f'

 L.  81        22  LOAD_FAST                'f'
               24  LOAD_METHOD              read
               26  CALL_METHOD_0         0  ''
               28  STORE_FAST               'data_sig'
               30  POP_BLOCK        
               32  BEGIN_FINALLY    
             34_0  COME_FROM_WITH       18  '18'
               34  WITH_CLEANUP_START
               36  WITH_CLEANUP_FINISH
               38  END_FINALLY      

 L.  82        40  LOAD_GLOBAL              Pkcs7
               42  CALL_FUNCTION_0       0  ''
               44  STORE_FAST               'pkcs7'

 L.  83        46  LOAD_FAST                'pkcs7'
               48  LOAD_METHOD              import_signature
               50  LOAD_FAST                'data_sig'
               52  CALL_METHOD_1         1  ''
               54  POP_TOP          

 L.  84        56  LOAD_FAST                'pkcs7'
               58  LOAD_METHOD              get_signature_info
               60  CALL_METHOD_0         0  ''
               62  STORE_FAST               'infos'

 L.  85        64  LOAD_FAST                'self'
               66  LOAD_METHOD              assertEqual
               68  LOAD_GLOBAL              len
               70  LOAD_FAST                'infos'
               72  CALL_FUNCTION_1       1  ''
               74  LOAD_CONST               1
               76  CALL_METHOD_2         2  ''
               78  POP_TOP          

 L.  86        80  LOAD_FAST                'infos'
               82  LOAD_CONST               0
               84  BINARY_SUBSCR    
               86  STORE_FAST               'info'

 L.  87        88  LOAD_FAST                'self'
               90  LOAD_METHOD              assertEqual
               92  LOAD_FAST                'info'
               94  LOAD_ATTR                algo
               96  LOAD_GLOBAL              GNUTLS_SIGN_RSA_SHA256
               98  CALL_METHOD_2         2  ''
              100  POP_TOP          

 L.  88       102  LOAD_FAST                'self'
              104  LOAD_METHOD              assertEqual
              106  LOAD_FAST                'info'
              108  LOAD_ATTR                signing_time
              110  LOAD_CONST               1503498945
              112  CALL_METHOD_2         2  ''
              114  POP_TOP          

 L.  89       116  LOAD_FAST                'self'
              118  LOAD_METHOD              assertEqual

 L.  90       120  LOAD_GLOBAL              str
              122  LOAD_FAST                'info'
              124  LOAD_ATTR                issuer_dn
              126  CALL_FUNCTION_1       1  ''

 L.  90       128  LOAD_STR                 'O=Linux Vendor Firmware Project,CN=LVFS CA'

 L.  89       130  CALL_METHOD_2         2  ''
              132  POP_TOP          

 L.  92       134  LOAD_FAST                'self'
              136  LOAD_METHOD              assertEqual

 L.  93       138  LOAD_FAST                'info'
              140  LOAD_ATTR                signer_serial

 L.  93       142  LOAD_STR                 '599d8e581c817895df746555'

 L.  92       144  CALL_METHOD_2         2  ''
              146  POP_TOP          

Parse error at or near `BEGIN_FINALLY' instruction at offset 32


if __name__ == '__main__':
    unittest.main()