# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/plugins/opensshlpk.py
# Compiled at: 2020-05-04 07:13:47
# Size of source mod 2**32: 5568 bytes
"""
web2ldap plugin classes for OpenSSH-LPK
(see https://code.google.com/p/openssh-lpk/)
"""
import re, hashlib, binascii, paramiko
from web2ldap.log import logger
from web2ldap.app.schema.syntaxes import DirectoryString, syntax_registry
PARAMIKO_KEYCLASS = {'ssh-rsa':paramiko.RSAKey, 
 'ssh-dss':paramiko.DSSKey}

class SshPublicKey(DirectoryString):
    oid = 'SshPublicKey-oid'
    oid: str
    desc = 'SSH public key of a user'
    desc: str
    input_pattern = '(^|.* )(ssh-rsa|ssh-dss|ecdsa-sha2-nistp256|ecdsa-sha2-nistp384|ecdsa-sha2-nistp521|ssh-ed25519) (?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?(| .+)$'
    input_pattern: str
    reObj = re.compile(input_pattern)
    hash_algorithms = ('md5', 'sha1', 'sha256', 'sha512')
    fileExt = 'pub'
    min_key_size = {'ssh-rsa':2048, 
     'ssh-dss':2048}

    def sanitize(self, attrValue: bytes) -> bytes:
        if attrValue:
            return DirectoryString.sanitize(self, attrValue).strip().replace(b'\r', b'').replace(b'\n', b'')
        return attrValue

    def _extract_pk_params--- This code section failed: ---

 L.  52         0  LOAD_FAST                'attrValue'
                2  LOAD_METHOD              decode
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                _app
                8  LOAD_ATTR                ls
               10  LOAD_ATTR                charset
               12  CALL_METHOD_1         1  ''
               14  STORE_FAST               'attr_value'

 L.  53        16  SETUP_FINALLY        40  'to 40'

 L.  54        18  LOAD_FAST                'attr_value'
               20  LOAD_METHOD              split
               22  LOAD_STR                 ' '
               24  LOAD_CONST               2
               26  CALL_METHOD_2         2  ''
               28  UNPACK_SEQUENCE_3     3 
               30  STORE_FAST               'pk_type'
               32  STORE_FAST               'pk_base64'
               34  STORE_FAST               'pk_comment'
               36  POP_BLOCK        
               38  JUMP_FORWARD         80  'to 80'
             40_0  COME_FROM_FINALLY    16  '16'

 L.  55        40  DUP_TOP          
               42  LOAD_GLOBAL              ValueError
               44  COMPARE_OP               exception-match
               46  POP_JUMP_IF_FALSE    78  'to 78'
               48  POP_TOP          
               50  POP_TOP          
               52  POP_TOP          

 L.  56        54  LOAD_CONST               None
               56  STORE_FAST               'pk_comment'

 L.  57        58  LOAD_FAST                'attr_value'
               60  LOAD_METHOD              split
               62  LOAD_STR                 ' '
               64  LOAD_CONST               1
               66  CALL_METHOD_2         2  ''
               68  UNPACK_SEQUENCE_2     2 
               70  STORE_FAST               'pk_type'
               72  STORE_FAST               'pk_base64'
               74  POP_EXCEPT       
               76  JUMP_FORWARD         80  'to 80'
             78_0  COME_FROM            46  '46'
               78  END_FINALLY      
             80_0  COME_FROM            76  '76'
             80_1  COME_FROM            38  '38'

 L.  58        80  SETUP_FINALLY       116  'to 116'

 L.  59        82  LOAD_GLOBAL              binascii
               84  LOAD_METHOD              a2b_base64
               86  LOAD_FAST                'pk_base64'
               88  CALL_METHOD_1         1  ''
               90  STORE_DEREF              'pk_bin'

 L.  60        92  LOAD_CLOSURE             'pk_bin'
               94  BUILD_TUPLE_1         1 
               96  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               98  LOAD_STR                 'SshPublicKey._extract_pk_params.<locals>.<dictcomp>'
              100  MAKE_FUNCTION_8          'closure'

 L.  62       102  LOAD_FAST                'self'
              104  LOAD_ATTR                hash_algorithms

 L.  60       106  GET_ITER         
              108  CALL_FUNCTION_1       1  ''
              110  STORE_FAST               'pk_fingerprints'
              112  POP_BLOCK        
              114  JUMP_FORWARD        170  'to 170'
            116_0  COME_FROM_FINALLY    80  '80'

 L.  64       116  DUP_TOP          
              118  LOAD_GLOBAL              Exception
              120  COMPARE_OP               exception-match
              122  POP_JUMP_IF_FALSE   168  'to 168'
              124  POP_TOP          
              126  STORE_FAST               'err'
              128  POP_TOP          
              130  SETUP_FINALLY       156  'to 156'

 L.  65       132  LOAD_GLOBAL              logger
              134  LOAD_METHOD              warning
              136  LOAD_STR                 'Error decoding SSH public key: %s'
              138  LOAD_FAST                'err'
              140  CALL_METHOD_2         2  ''
              142  POP_TOP          

 L.  66       144  LOAD_CONST               (None, None)
              146  UNPACK_SEQUENCE_2     2 
              148  STORE_DEREF              'pk_bin'
              150  STORE_FAST               'pk_fingerprints'
              152  POP_BLOCK        
              154  BEGIN_FINALLY    
            156_0  COME_FROM_FINALLY   130  '130'
              156  LOAD_CONST               None
              158  STORE_FAST               'err'
              160  DELETE_FAST              'err'
              162  END_FINALLY      
              164  POP_EXCEPT       
              166  JUMP_FORWARD        170  'to 170'
            168_0  COME_FROM           122  '122'
              168  END_FINALLY      
            170_0  COME_FROM           166  '166'
            170_1  COME_FROM           114  '114'

 L.  67       170  LOAD_FAST                'pk_type'
              172  LOAD_FAST                'pk_comment'
              174  LOAD_DEREF               'pk_bin'
              176  LOAD_FAST                'pk_fingerprints'
              178  BUILD_TUPLE_4         4 
              180  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_DICTCOMP' instruction at offset 96

    @staticmethod
    def _strip_padding(b64_val):
        i = len(b64_val)
        while b64_val[(i - 1)] == '=':
            i = i - 1

        return b64_val[:i]

    @staticmethod
    def _get_key_size(pk_type, pk_bin):
        try:
            p = PARAMIKO_KEYCLASS[pk_type](data=pk_bin)
        except (KeyError, paramiko.SSHException):
            pk_size = None
        else:
            pk_size = p.get_bits()
        return pk_size

    def _validate(self, attrValue: bytes) -> bool:
        valid = DirectoryString._validate(self, attrValue)
        if not valid:
            return False
        try:
            pk_type, _, pk_bin, _ = self._extract_pk_params(attrValue)
        except ValueError:
            return False
        else:
            if pk_type not in self.min_key_size:
                return True
            pk_size = self._get_key_size(pk_type, pk_bin)
            return pk_size is None or pk_size >= self.min_key_size[pk_type]

    def _display_lines(self, valueindex, commandbutton, pk_type, pk_comment, pk_bin, pk_fingerprints):
        result = []
        result.append('<dt>SSH Key:</dt><dd><input readonly size="70" value="{}"></dd>'.format(DirectoryString.display(self, valueindex, commandbutton)))
        if pk_comment:
            result.append('<dt>Key comment:</dt><dd>{}</dd>'.format(self._app.form.utf2display(pk_comment)))
        else:
            if pk_fingerprints:
                result.append('<dt>Fingerprints:</dt><dd><dl>')
                for hash_algo, pk_fingerprint in sorted(pk_fingerprints.items()):
                    result.append('<dt>{0}:</dt><dd>{1}</dd>'.format(hash_algo.upper(), ':'.join([hex(b)[2:] for b in pk_fingerprint])))
                else:
                    for hash_algo in ('sha1', 'sha256', 'sha512'):
                        result.append('<dt>ssh-keygen -l -E {0}</dt><dd>{1}</dd>'.format(hash_algo, self._app.form.utf2display(self._strip_padding(binascii.b2a_base64(pk_fingerprints[hash_algo]).strip()).decode('ascii'))))
                    else:
                        result.append('</dl></dd>')

            if pk_bin:
                pk_size = self._get_key_size(pk_type, pk_bin)
                if pk_size is None:
                    result.append('<dt>Key size:</dt><dd>unknown</dd>')
                else:
                    result.append('<dt>Key size:</dt><dd>%d</dd>' % pk_size)
        return result

    def display(self, valueindex=0, commandbutton=False) -> str:
        pk_type, pk_comment, pk_bin, pk_fingerprints = self._extract_pk_params(self._av)
        result = ['<dl>']
        result.extend(self._display_lines(valueindex, commandbutton, pk_type, pk_comment, pk_bin, pk_fingerprints))
        result.append('</dl>')
        return '\n'.join(result)


syntax_registry.reg_at(SshPublicKey.oid, [
 '1.3.6.1.4.1.24552.500.1.1.1.13'])
syntax_registry.reg_syntaxes(__name__)