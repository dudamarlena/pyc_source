# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\AESClient\AES.py
# Compiled at: 2020-04-28 23:31:49
# Size of source mod 2**32: 20492 bytes
import Crypto.Cipher as AES_
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import SHA256, SHA1, MD5, SHA224
from Crypto import Random
from Crypto.Util.RFC1751 import english_to_key
from shaonutil.security import generateCryptographicallySecureRandomString
from base64 import b64encode, b64decode
from uuid import UUID
from io import BytesIO
import hashlib, shaonutil, binascii, os, struct
__RANDOM__ = True
__KILO_BYTE__ = 1024
__byte__ = 8

class AES:
    """AES"""

    def __init__(self, KEY, IV='', bit=256, log=True):
        self.log = log
        self.has_iv_str_block_length = 16
        self.check_sum = True
        self.check_sum_str_length = 32
        self.stringify_enable = True
        self.bit = bit
        self.new(key=KEY, iv=IV)

    def new(self, key='', iv=''):
        if key != '' and iv != '':
            key, iv = self.process_keys(bit=(self.bit), key=key, iv=iv)
            self.check_keys(bit=(self.bit), key=key, iv=iv)
        elif key == '' and iv == '':
            key = self.KEY
            iv = self.IV
        elif key != '':
            key = self.process_keys(key=key, bit=(self.bit))
            self.check_keys(key=key, bit=(self.bit))
            try:
                iv = self.IV
            except:
                iv = os.urandom(AES_.block_size)

        elif iv != '':
            iv = self.process_keys(iv=iv, bit=(self.bit))
            self.check_keys(iv=iv, bit=(self.bit))
            key = self.KEY
        self.aes = AES_.new(key, AES_.MODE_CBC, iv)
        self.KEY = key
        self.IV = iv

    def check_keys(self, bit, key='', iv=''):
        if iv != '':
            if len(iv) != AES_.block_size:
                raise ValueError('Initialization Vector must be 16 characters long')
        else:
            if key != '':
                key_length = len(key)
                if not key_length == 1 * AES_.block_size:
                    if not key_length == 1.5 * AES_.block_size:
                        if not key_length == 2 * AES_.block_size:
                            raise ValueError('Key length needs to be 16/24/32 characters long or 16/24/32 bytes long, depending if we want to use AES-128, AES-192 or AES-256 respectively')
                if bit == 256 and key_length != 2 * AES_.block_size:
                    raise ValueError(f"AES-256 encryption needs the key to be 32 characters long. {key_length} characters long key given.")
            elif bit == 192 and key_length != 1.5 * AES_.block_size:
                raise ValueError(f"AES-192 encryption needs the key to be 24 characters long. {key_length} characters long key given.")
            elif bit == 128 and key_length != 1 * AES_.block_size:
                raise ValueError(f"AES-128 encryption needs the key to be 16 characters long. {key_length} characters long key given.")
            if iv == '' and key == '':
                raise ValueError('Both key and iv can not be empty in check_keys')

    def process_keys(self, bit, key='', iv=''):
        if key != '':
            key = key.encode('ascii')
            if bit == 256:
                key = SHA256.new(key).digest()
            elif bit == 192:
                key = SHA224.new(key).digest()[:-4]
            elif bit == 128:
                key = MD5.new(key).digest()
        elif iv != '':
            if type(iv) == str:
                iv = iv.encode('ascii')
            self.has_iv = False
        else:
            self.has_iv = True
        if key != '':
            if iv != '':
                return (
                 key, iv)
        if key != '':
            return key
        if iv != '':
            return iv
        raise ValueError('No parameter given to process.')

    def get_has_iv_str_length(self, PARSE_PARAM):
        int_sum = sum([int(i) for i in PARSE_PARAM[:self.has_iv_str_block_length]])
        reminder = int_sum % (self.has_iv_str_block_length - 1) + 1
        return reminder

    def parse_has_iv_combined(self, filebuffer_or_bytesio, input_buffersize):
        """Parse has_iv from encrypted buffer"""
        if self.log:
            print('Log : has_iv state has been extracted.')
        has_iv_str_length = self.get_has_iv_str_length(self.KEY)
        EN_ = self.KEY[:self.has_iv_str_block_length]
        hash_algo1 = 'sha1'
        h = hashlib.new(hash_algo1)
        h.update(EN_)
        has_iv_str1 = h.digest()[:has_iv_str_length]
        hash_algo2 = 'ripemd160'
        h = hashlib.new(hash_algo2)
        h.update(EN_)
        has_iv_str2 = h.digest()[:has_iv_str_length]
        encrypted_filesize = input_buffersize
        St_ = encrypted_filesize - has_iv_str_length
        previous_position = filebuffer_or_bytesio.tell()
        filebuffer_or_bytesio.seek(St_)
        has_iv_str = filebuffer_or_bytesio.read(has_iv_str_length)
        filebuffer_or_bytesio.seek(previous_position)
        if self.log:
            print('Log : Get IV_STATE', has_iv_str)
        if has_iv_str == has_iv_str1:
            return True
        if has_iv_str == has_iv_str2:
            return False
        raise ValueError('Data Corrupted')

    def get_has_iv(self, has_iv):
        has_iv_str_length = self.get_has_iv_str_length(self.KEY)
        EN_ = self.KEY[:self.has_iv_str_block_length]
        if has_iv:
            hash_algo = 'sha1'
        else:
            hash_algo = 'ripemd160'
        h = hashlib.new(hash_algo)
        h.update(EN_)
        has_iv_str = h.digest()[:has_iv_str_length]
        if self.log:
            print('Log : has_iv state has been created.')
        return has_iv_str

    def append_has_iv(self, has_iv, filebuffer_or_bytesio, input_buffersize):
        """adding iv at begining and state at end"""
        check_sum_length = self.check_sum_str_length if self.check_sum else 0
        has_iv_str = self.get_has_iv(has_iv)
        outfile = filebuffer_or_bytesio
        file_size_str_length = len(struct.pack('<Q', input_buffersize))
        if self.has_iv:
            outfile.seek(file_size_str_length)
            outfile.write(self.IV)
            IV_length = len(self.IV)
        else:
            IV_length = 0
        file_size = input_buffersize
        padding_size = self.get_padding_size(file_size)
        outfile.seek(file_size_str_length + IV_length + file_size + padding_size + check_sum_length)
        outfile.write(has_iv_str)
        if self.log:
            print('Log : Set IV_STATE', has_iv_str)
        outfile.seek(file_size_str_length + IV_length)
        return outfile

    def get_padding_size(self, original_filesize):
        if original_filesize % AES_.block_size != 0:
            return AES_.block_size - original_filesize % AES_.block_size
        return 0

    def calculate_encrypted_buffersize(self, in_filename):
        """fix me"""
        original_filesize = os.path.getsize(in_filename)
        original_filesize_str_length = len(struct.pack('<Q', original_filesize))
        IV_length = len(self.IV) if self.has_iv else 0
        padded_size = self.get_padding_size(original_filesize)
        has_iv_str_size = len(self.get_has_iv(self.has_iv))
        total_file_size_or_buffer_size = original_filesize_str_length + IV_length + original_filesize + padded_size + has_iv_str_size
        print(f"original_filesize_str_length({original_filesize_str_length}) + IV_length({IV_length}) + original_filesize({original_filesize}) + padded_size({padded_size}) + has_iv_str_size({has_iv_str_size})")
        print('total_outfilesize', total_file_size_or_buffer_size)
        return total_file_size_or_buffer_size

    def calculate_md5_sum(self, file_or_iobuffer, encrypt=False):
        file_or_iobuffer.seek(0)
        md5_hash = hashlib.md5()
        for byte_block in iter(lambda : file_or_iobuffer.read(4 * __KILO_BYTE__), b''):
            md5_hash.update(byte_block)

        file_or_iobuffer.seek(0)
        return_ = self.aes.encrypt(md5_hash.hexdigest()) if encrypt else md5_hash.hexdigest()
        return return_

    def calculate_sha256_sum(file_or_iobuffer):
        file_or_iobuffer.seek(0)
        sha256_hash = hashlib.md5()
        for byte_block in iter(lambda : file_or_iobuffer.read(4 * __KILO_BYTE__), b''):
            sha256_hash.update(byte_block)

        file_or_iobuffer.seek(0)
        return sha256_hash.hexdigest()

    def anybyte_to_string(self, byte, stringify_method):
        if stringify_method == 'b64':
            byte = b64encode(byte)
        elif stringify_method == 'hex':
            byte = binascii.hexlify(byte)
        return byte.decode('utf-8')

    def string_to_anybyte(self, string, stringify_method):
        byte = string.encode('utf-8')
        if stringify_method == 'b64':
            string = b64decode(byte)
        elif stringify_method == 'hex':
            string = binascii.unhexlify(byte)
        return string

    def encrypt_common(self, inbuffer, outbuffer, understand, buffersize, chunksize):
        if understand:
            print('File pointer position', outbuffer.tell())
        outbuffer.write(struct.pack('<Q', buffersize))
        if understand:
            print('File pointer position', outbuffer.tell())
        outbuffer = self.append_has_iv(self.has_iv, outbuffer, buffersize)
        if self.check_sum:
            md5_hash = hashlib.md5()
        while True:
            chunk = inbuffer.read(chunksize)
            if self.check_sum:
                md5_hash.update(chunk)
            elif len(chunk) == 0:
                break
            elif len(chunk) % 16 != 0:
                chunk += b' ' * (16 - len(chunk) % 16)
            encryption_chunk = self.aes.encrypt(chunk)
            outbuffer.write(encryption_chunk)

        if self.check_sum:
            check_sum_str = md5_hash.hexdigest().encode('utf-8')
            md5_hash_encrypted = self.aes.encrypt(check_sum_str)
            outbuffer.write(md5_hash_encrypted)

    def decrypt_common(self, inbuffer, outbuffer, encrypted_filesize, chunksize, understand):
        if self.check_sum:
            md5_hash = hashlib.md5()
        else:
            original_filesize_str_length = struct.calcsize('Q')
            size_byte = inbuffer.read(original_filesize_str_length)
            if understand:
                print(' After Reading filesize_chunk length Pointer Position', inbuffer.tell())
            else:
                original_size = struct.unpack('<Q', size_byte)
                original_size = original_size[0]
                has_iv = self.parse_has_iv_combined(inbuffer, encrypted_filesize)
                if has_iv:
                    extracted_iv = inbuffer.read(AES_.block_size)
                    if understand:
                        print('File pointer at position (<24>= 16 - <8>) after 16 bytes IV chunk . Pointer Position', inbuffer.tell())
                    self.new(iv=extracted_iv)
                    IV_length = len(extracted_iv)
                else:
                    IV_length = 0
                file_read_up_to = original_filesize_str_length + IV_length + original_size + self.get_padding_size(original_size)
                decrypted_size = 0
            while True:
                chunk_reading_size = file_read_up_to - inbuffer.tell() if inbuffer.tell() + chunksize > file_read_up_to else chunksize
                if chunk_reading_size == 0:
                    break
                chunk = inbuffer.read(chunk_reading_size)
                decrypted_text = self.aes.decrypt(chunk)
                decrypted_size += len(decrypted_text)
                if decrypted_size > original_size:
                    decrypted_text = decrypted_text[:-(decrypted_size - original_size)]
                outbuffer.write(decrypted_text)
                if self.check_sum:
                    md5_hash.update(decrypted_text)

            if self.check_sum:
                check_sum_str = inbuffer.read(self.check_sum_str_length)
                extracted_check_sum_str = self.aes.decrypt(check_sum_str)
                calculated_check_sum_str = md5_hash.hexdigest().encode('utf-8')
                if extracted_check_sum_str == calculated_check_sum_str:
                    if self.log:
                        print('Log : Successfully Decrypted')
                else:
                    if self.log:
                        print('Log : Data Corrupted')
                    raise ValueError('Data Corrupted')

    def encrypt_to_readable_text--- This code section failed: ---

 L. 449         0  LOAD_FAST                'data'
                2  LOAD_METHOD              encode
                4  LOAD_STR                 'utf-8'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'data_byte'

 L. 451        10  LOAD_CONST               False
               12  STORE_FAST               'understand'

 L. 453        14  LOAD_GLOBAL              len
               16  LOAD_FAST                'data_byte'
               18  CALL_FUNCTION_1       1  ''
               20  STORE_FAST               'filesize'

 L. 454        22  LOAD_FAST                'self'
               24  LOAD_ATTR                log
               26  POP_JUMP_IF_FALSE    38  'to 38'

 L. 454        28  LOAD_GLOBAL              print
               30  LOAD_STR                 'Log : BYTE Size'
               32  LOAD_FAST                'filesize'
               34  CALL_FUNCTION_2       2  ''
               36  POP_TOP          
             38_0  COME_FROM            26  '26'

 L. 457        38  LOAD_GLOBAL              BytesIO
               40  LOAD_FAST                'data_byte'
               42  CALL_FUNCTION_1       1  ''
               44  SETUP_WITH           98  'to 98'
               46  STORE_FAST               'infile'

 L. 458        48  LOAD_GLOBAL              BytesIO
               50  LOAD_CONST               b''
               52  CALL_FUNCTION_1       1  ''
               54  SETUP_WITH           88  'to 88'
               56  STORE_FAST               'outfile'

 L. 459        58  LOAD_FAST                'self'
               60  LOAD_METHOD              encrypt_common
               62  LOAD_FAST                'infile'
               64  LOAD_FAST                'outfile'
               66  LOAD_FAST                'understand'
               68  LOAD_FAST                'filesize'
               70  LOAD_FAST                'chunksize'
               72  CALL_METHOD_5         5  ''
               74  POP_TOP          

 L. 461        76  LOAD_FAST                'outfile'
               78  LOAD_METHOD              getvalue
               80  CALL_METHOD_0         0  ''
               82  STORE_FAST               'encrypted_byte'
               84  POP_BLOCK        
               86  BEGIN_FINALLY    
             88_0  COME_FROM_WITH       54  '54'
               88  WITH_CLEANUP_START
               90  WITH_CLEANUP_FINISH
               92  END_FINALLY      
               94  POP_BLOCK        
               96  BEGIN_FINALLY    
             98_0  COME_FROM_WITH       44  '44'
               98  WITH_CLEANUP_START
              100  WITH_CLEANUP_FINISH
              102  END_FINALLY      

 L. 463       104  LOAD_FAST                'self'
              106  LOAD_ATTR                stringify_enable
              108  POP_JUMP_IF_FALSE   122  'to 122'
              110  LOAD_FAST                'self'
              112  LOAD_METHOD              anybyte_to_string
              114  LOAD_FAST                'encrypted_byte'
              116  LOAD_FAST                'stringify_method'
              118  CALL_METHOD_2         2  ''
              120  JUMP_FORWARD        124  'to 124'
            122_0  COME_FROM           108  '108'
              122  LOAD_FAST                'encrypted_byte'
            124_0  COME_FROM           120  '120'
              124  STORE_FAST               'encrypted_byte'

 L. 464       126  LOAD_FAST                'encrypted_byte'
              128  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `BEGIN_FINALLY' instruction at offset 86

    def encrypt_file--- This code section failed: ---

 L. 468         0  LOAD_FAST                'out_filename'
                2  POP_JUMP_IF_TRUE     12  'to 12'

 L. 468         4  LOAD_FAST                'in_filename'
                6  LOAD_STR                 '.enc'
                8  BINARY_ADD       
               10  STORE_FAST               'out_filename'
             12_0  COME_FROM             2  '2'

 L. 470        12  LOAD_CONST               False
               14  STORE_FAST               'understand'

 L. 472        16  LOAD_GLOBAL              os
               18  LOAD_ATTR                path
               20  LOAD_METHOD              getsize
               22  LOAD_FAST                'in_filename'
               24  CALL_METHOD_1         1  ''
               26  STORE_FAST               'filesize'

 L. 473        28  LOAD_FAST                'self'
               30  LOAD_ATTR                log
               32  POP_JUMP_IF_FALSE    44  'to 44'

 L. 473        34  LOAD_GLOBAL              print
               36  LOAD_STR                 'Log : FILE Size'
               38  LOAD_FAST                'filesize'
               40  CALL_FUNCTION_2       2  ''
               42  POP_TOP          
             44_0  COME_FROM            32  '32'

 L. 474        44  LOAD_FAST                'understand'
               46  POP_JUMP_IF_FALSE    68  'to 68'

 L. 474        48  LOAD_GLOBAL              print
               50  LOAD_GLOBAL              type
               52  LOAD_GLOBAL              struct
               54  LOAD_METHOD              pack
               56  LOAD_STR                 '<Q'
               58  LOAD_FAST                'filesize'
               60  CALL_METHOD_2         2  ''
               62  CALL_FUNCTION_1       1  ''
               64  CALL_FUNCTION_1       1  ''
               66  POP_TOP          
             68_0  COME_FROM            46  '46'

 L. 477        68  LOAD_GLOBAL              open
               70  LOAD_FAST                'in_filename'
               72  LOAD_STR                 'rb'
               74  CALL_FUNCTION_2       2  ''
               76  SETUP_WITH          124  'to 124'
               78  STORE_FAST               'infile'

 L. 478        80  LOAD_GLOBAL              open
               82  LOAD_FAST                'out_filename'
               84  LOAD_STR                 'wb'
               86  CALL_FUNCTION_2       2  ''
               88  SETUP_WITH          114  'to 114'
               90  STORE_FAST               'outfile'

 L. 479        92  LOAD_FAST                'self'
               94  LOAD_METHOD              encrypt_common
               96  LOAD_FAST                'infile'
               98  LOAD_FAST                'outfile'
              100  LOAD_FAST                'understand'
              102  LOAD_FAST                'filesize'
              104  LOAD_FAST                'chunksize'
              106  CALL_METHOD_5         5  ''
              108  POP_TOP          
              110  POP_BLOCK        
              112  BEGIN_FINALLY    
            114_0  COME_FROM_WITH       88  '88'
              114  WITH_CLEANUP_START
              116  WITH_CLEANUP_FINISH
              118  END_FINALLY      
              120  POP_BLOCK        
              122  BEGIN_FINALLY    
            124_0  COME_FROM_WITH       76  '76'
              124  WITH_CLEANUP_START
              126  WITH_CLEANUP_FINISH
              128  END_FINALLY      

Parse error at or near `BEGIN_FINALLY' instruction at offset 112

    def encrypt_string_to_file--- This code section failed: ---

 L. 484         0  LOAD_FAST                'string'
                2  LOAD_METHOD              encode
                4  LOAD_STR                 'utf-8'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'data_byte'

 L. 486        10  LOAD_CONST               False
               12  STORE_FAST               'understand'

 L. 488        14  LOAD_GLOBAL              len
               16  LOAD_FAST                'data_byte'
               18  CALL_FUNCTION_1       1  ''
               20  STORE_FAST               'filesize'

 L. 489        22  LOAD_FAST                'self'
               24  LOAD_ATTR                log
               26  POP_JUMP_IF_FALSE    38  'to 38'

 L. 489        28  LOAD_GLOBAL              print
               30  LOAD_STR                 'Log : BYTE Size'
               32  LOAD_FAST                'filesize'
               34  CALL_FUNCTION_2       2  ''
               36  POP_TOP          
             38_0  COME_FROM            26  '26'

 L. 492        38  LOAD_GLOBAL              BytesIO
               40  LOAD_FAST                'data_byte'
               42  CALL_FUNCTION_1       1  ''
               44  SETUP_WITH           92  'to 92'
               46  STORE_FAST               'infile'

 L. 493        48  LOAD_GLOBAL              open
               50  LOAD_FAST                'out_filename'
               52  LOAD_STR                 'wb'
               54  CALL_FUNCTION_2       2  ''
               56  SETUP_WITH           82  'to 82'
               58  STORE_FAST               'outfile'

 L. 494        60  LOAD_FAST                'self'
               62  LOAD_METHOD              encrypt_common
               64  LOAD_FAST                'infile'
               66  LOAD_FAST                'outfile'
               68  LOAD_FAST                'understand'
               70  LOAD_FAST                'filesize'
               72  LOAD_FAST                'chunksize'
               74  CALL_METHOD_5         5  ''
               76  POP_TOP          
               78  POP_BLOCK        
               80  BEGIN_FINALLY    
             82_0  COME_FROM_WITH       56  '56'
               82  WITH_CLEANUP_START
               84  WITH_CLEANUP_FINISH
               86  END_FINALLY      
               88  POP_BLOCK        
               90  BEGIN_FINALLY    
             92_0  COME_FROM_WITH       44  '44'
               92  WITH_CLEANUP_START
               94  WITH_CLEANUP_FINISH
               96  END_FINALLY      

Parse error at or near `BEGIN_FINALLY' instruction at offset 80

    def decrypt_to_readable_text--- This code section failed: ---

 L. 498         0  LOAD_FAST                'self'
                2  LOAD_ATTR                stringify_enable
                4  POP_JUMP_IF_FALSE    18  'to 18'
                6  LOAD_FAST                'self'
                8  LOAD_METHOD              string_to_anybyte
               10  LOAD_FAST                'encrypted_string'
               12  LOAD_FAST                'stringify_method'
               14  CALL_METHOD_2         2  ''
               16  JUMP_FORWARD         20  'to 20'
             18_0  COME_FROM             4  '4'
               18  LOAD_FAST                'encrypted_string'
             20_0  COME_FROM            16  '16'
               20  STORE_FAST               'string_encrypted_byte'

 L. 500        22  LOAD_CONST               False
               24  STORE_FAST               'understand'

 L. 501        26  LOAD_GLOBAL              len
               28  LOAD_FAST                'string_encrypted_byte'
               30  CALL_FUNCTION_1       1  ''
               32  STORE_FAST               'encrypted_filesize'

 L. 503        34  LOAD_GLOBAL              BytesIO
               36  LOAD_FAST                'string_encrypted_byte'
               38  CALL_FUNCTION_1       1  ''
               40  SETUP_WITH           94  'to 94'
               42  STORE_FAST               'infile'

 L. 505        44  LOAD_GLOBAL              BytesIO
               46  LOAD_CONST               b''
               48  CALL_FUNCTION_1       1  ''
               50  SETUP_WITH           84  'to 84'
               52  STORE_FAST               'outfile'

 L. 507        54  LOAD_FAST                'self'
               56  LOAD_METHOD              decrypt_common
               58  LOAD_FAST                'infile'
               60  LOAD_FAST                'outfile'
               62  LOAD_FAST                'encrypted_filesize'
               64  LOAD_FAST                'chunksize'
               66  LOAD_FAST                'understand'
               68  CALL_METHOD_5         5  ''
               70  POP_TOP          

 L. 509        72  LOAD_FAST                'outfile'
               74  LOAD_METHOD              getvalue
               76  CALL_METHOD_0         0  ''
               78  STORE_FAST               'decrypted_data_byte'
               80  POP_BLOCK        
               82  BEGIN_FINALLY    
             84_0  COME_FROM_WITH       50  '50'
               84  WITH_CLEANUP_START
               86  WITH_CLEANUP_FINISH
               88  END_FINALLY      
               90  POP_BLOCK        
               92  BEGIN_FINALLY    
             94_0  COME_FROM_WITH       40  '40'
               94  WITH_CLEANUP_START
               96  WITH_CLEANUP_FINISH
               98  END_FINALLY      

 L. 511       100  LOAD_FAST                'decrypted_data_byte'
              102  LOAD_METHOD              decode
              104  LOAD_STR                 'utf-8'
              106  CALL_METHOD_1         1  ''
              108  STORE_FAST               'data'

 L. 512       110  LOAD_FAST                'data'
              112  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `BEGIN_FINALLY' instruction at offset 82

    def decrypt_file--- This code section failed: ---

 L. 516         0  LOAD_FAST                'out_filename'
                2  POP_JUMP_IF_TRUE     20  'to 20'

 L. 516         4  LOAD_GLOBAL              os
                6  LOAD_ATTR                path
                8  LOAD_METHOD              splitext
               10  LOAD_FAST                'in_filename'
               12  CALL_METHOD_1         1  ''
               14  LOAD_CONST               0
               16  BINARY_SUBSCR    
               18  STORE_FAST               'out_filename'
             20_0  COME_FROM             2  '2'

 L. 518        20  LOAD_CONST               False
               22  STORE_FAST               'understand'

 L. 519        24  LOAD_GLOBAL              os
               26  LOAD_ATTR                path
               28  LOAD_METHOD              getsize
               30  LOAD_FAST                'in_filename'
               32  CALL_METHOD_1         1  ''
               34  STORE_FAST               'encrypted_filesize'

 L. 521        36  LOAD_GLOBAL              open
               38  LOAD_FAST                'in_filename'
               40  LOAD_STR                 'rb'
               42  CALL_FUNCTION_2       2  ''
               44  SETUP_WITH           92  'to 92'
               46  STORE_FAST               'infile'

 L. 523        48  LOAD_GLOBAL              open
               50  LOAD_FAST                'out_filename'
               52  LOAD_STR                 'wb'
               54  CALL_FUNCTION_2       2  ''
               56  SETUP_WITH           82  'to 82'
               58  STORE_FAST               'outfile'

 L. 525        60  LOAD_FAST                'self'
               62  LOAD_METHOD              decrypt_common
               64  LOAD_FAST                'infile'
               66  LOAD_FAST                'outfile'
               68  LOAD_FAST                'encrypted_filesize'
               70  LOAD_FAST                'chunksize'
               72  LOAD_FAST                'understand'
               74  CALL_METHOD_5         5  ''
               76  POP_TOP          
               78  POP_BLOCK        
               80  BEGIN_FINALLY    
             82_0  COME_FROM_WITH       56  '56'
               82  WITH_CLEANUP_START
               84  WITH_CLEANUP_FINISH
               86  END_FINALLY      
               88  POP_BLOCK        
               90  BEGIN_FINALLY    
             92_0  COME_FROM_WITH       44  '44'
               92  WITH_CLEANUP_START
               94  WITH_CLEANUP_FINISH
               96  END_FINALLY      

Parse error at or near `BEGIN_FINALLY' instruction at offset 80

    def decrypt_file_to_string--- This code section failed: ---

 L. 528         0  LOAD_CONST               False
                2  STORE_FAST               'understand'

 L. 529         4  LOAD_GLOBAL              os
                6  LOAD_ATTR                path
                8  LOAD_METHOD              getsize
               10  LOAD_FAST                'in_filename'
               12  CALL_METHOD_1         1  ''
               14  STORE_FAST               'encrypted_filesize'

 L. 531        16  LOAD_GLOBAL              open
               18  LOAD_FAST                'in_filename'
               20  LOAD_STR                 'rb'
               22  CALL_FUNCTION_2       2  ''
               24  SETUP_WITH           78  'to 78'
               26  STORE_FAST               'infile'

 L. 533        28  LOAD_GLOBAL              BytesIO
               30  LOAD_CONST               b''
               32  CALL_FUNCTION_1       1  ''
               34  SETUP_WITH           68  'to 68'
               36  STORE_FAST               'outfile'

 L. 535        38  LOAD_FAST                'self'
               40  LOAD_METHOD              decrypt_common
               42  LOAD_FAST                'infile'
               44  LOAD_FAST                'outfile'
               46  LOAD_FAST                'encrypted_filesize'
               48  LOAD_FAST                'chunksize'
               50  LOAD_FAST                'understand'
               52  CALL_METHOD_5         5  ''
               54  POP_TOP          

 L. 537        56  LOAD_FAST                'outfile'
               58  LOAD_METHOD              getvalue
               60  CALL_METHOD_0         0  ''
               62  STORE_FAST               'decrypted_data_byte'
               64  POP_BLOCK        
               66  BEGIN_FINALLY    
             68_0  COME_FROM_WITH       34  '34'
               68  WITH_CLEANUP_START
               70  WITH_CLEANUP_FINISH
               72  END_FINALLY      
               74  POP_BLOCK        
               76  BEGIN_FINALLY    
             78_0  COME_FROM_WITH       24  '24'
               78  WITH_CLEANUP_START
               80  WITH_CLEANUP_FINISH
               82  END_FINALLY      

 L. 539        84  LOAD_FAST                'decrypted_data_byte'
               86  LOAD_METHOD              decode
               88  LOAD_FAST                'data_encoding'
               90  CALL_METHOD_1         1  ''
               92  STORE_FAST               'data'

 L. 540        94  LOAD_FAST                'data'
               96  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `BEGIN_FINALLY' instruction at offset 66


# NOTE: have internal decompilation grammar errors.
# Use -t option to show full context.
# not in loop:
#	break
#      L. 361       122  BREAK_LOOP          190  'to 190'
# not in loop:
#	break
#      L. 408   210_212  BREAK_LOOP          304  'to 304'