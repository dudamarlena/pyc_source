# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
    __doc__ = '\n\t\tchunksize:\n\t\t\tSets the size of the chunk which the function uses to read and encrypt the file\n\t\t\tLarger chunk sizes can be faster for some files and machines.\n\t\t\tchunksize must be divisible by 16.\n\t'

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
        else:
            if key == '' and iv == '':
                key = self.KEY
                iv = self.IV
            else:
                if key != '':
                    key = self.process_keys(key=key, bit=(self.bit))
                    self.check_keys(key=key, bit=(self.bit))
                    try:
                        iv = self.IV
                    except:
                        iv = os.urandom(AES_.block_size)

                else:
                    if iv != '':
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
            else:
                if bit == 128 and key_length != 1 * AES_.block_size:
                    raise ValueError(f"AES-128 encryption needs the key to be 16 characters long. {key_length} characters long key given.")
            if iv == '' and key == '':
                raise ValueError('Both key and iv can not be empty in check_keys')

    def process_keys(self, bit, key='', iv=''):
        if key != '':
            key = key.encode('ascii')
            if bit == 256:
                key = SHA256.new(key).digest()
            else:
                if bit == 192:
                    key = SHA224.new(key).digest()[:-4]
                else:
                    if bit == 128:
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
        for byte_block in iter(lambda : file_or_iobuffer.read(4 * __KILO_BYTE__), ''):
            md5_hash.update(byte_block)
        else:
            file_or_iobuffer.seek(0)
            return_ = self.aes.encrypt(md5_hash.hexdigest()) if encrypt else md5_hash.hexdigest()
            return return_

    def calculate_sha256_sum(file_or_iobuffer):
        file_or_iobuffer.seek(0)
        sha256_hash = hashlib.md5()
        for byte_block in iter(lambda : file_or_iobuffer.read(4 * __KILO_BYTE__), ''):
            sha256_hash.update(byte_block)
        else:
            file_or_iobuffer.seek(0)
            return sha256_hash.hexdigest()

    def anybyte_to_string(self, byte, stringify_method):
        if stringify_method == 'b64':
            byte = b64encode(byte)
        else:
            if stringify_method == 'hex':
                byte = binascii.hexlify(byte)
        return byte.decode('utf-8')

    def string_to_anybyte(self, string, stringify_method):
        byte = string.encode('utf-8')
        if stringify_method == 'b64':
            string = b64decode(byte)
        else:
            if stringify_method == 'hex':
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
            else:
                if len(chunk) % 16 != 0:
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

    def encrypt_to_readable_text(self, data, stringify_method='b64', chunksize=16):
        data_byte = data.encode('utf-8')
        understand = False
        filesize = len(data_byte)
        if self.log:
            print('Log : BYTE Size', filesize)
        with BytesIO(data_byte) as (infile):
            with BytesIO('') as (outfile):
                self.encrypt_common(infile, outfile, understand, filesize, chunksize)
                encrypted_byte = outfile.getvalue()
        encrypted_byte = self.anybyte_to_string(encrypted_byte, stringify_method) if self.stringify_enable else encrypted_byte
        return encrypted_byte

    def encrypt_file(self, in_filename, out_filename=None, chunksize=64 * __KILO_BYTE__):
        """ Encrypts a file using AES (CBC mode) with the given key."""
        if not out_filename:
            out_filename = in_filename + '.enc'
        understand = False
        filesize = os.path.getsize(in_filename)
        if self.log:
            print('Log : FILE Size', filesize)
        if understand:
            print(type(struct.pack('<Q', filesize)))
        with open(in_filename, 'rb') as (infile):
            with open(out_filename, 'wb') as (outfile):
                self.encrypt_common(infile, outfile, understand, filesize, chunksize)

    def encrypt_string_to_file(self, string, out_filename, chunksize=64 * __KILO_BYTE__, data_encoding='ascii'):
        data_byte = string.encode('utf-8')
        understand = False
        filesize = len(data_byte)
        if self.log:
            print('Log : BYTE Size', filesize)
        with BytesIO(data_byte) as (infile):
            with open(out_filename, 'wb') as (outfile):
                self.encrypt_common(infile, outfile, understand, filesize, chunksize)

    def decrypt_to_readable_text(self, encrypted_string, stringify_method='b64', chunksize=16):
        string_encrypted_byte = self.string_to_anybyte(encrypted_string, stringify_method) if self.stringify_enable else encrypted_string
        understand = False
        encrypted_filesize = len(string_encrypted_byte)
        with BytesIO(string_encrypted_byte) as (infile):
            with BytesIO('') as (outfile):
                self.decrypt_common(infile, outfile, encrypted_filesize, chunksize, understand)
                decrypted_data_byte = outfile.getvalue()
        data = decrypted_data_byte.decode('utf-8')
        return data

    def decrypt_file(self, in_filename, out_filename=None, chunksize=24 * __KILO_BYTE__):
        """ Decrypts a file using AES (CBC mode) with"""
        if not out_filename:
            out_filename = os.path.splitext(in_filename)[0]
        understand = False
        encrypted_filesize = os.path.getsize(in_filename)
        with open(in_filename, 'rb') as (infile):
            with open(out_filename, 'wb') as (outfile):
                self.decrypt_common(infile, outfile, encrypted_filesize, chunksize, understand)

    def decrypt_file_to_string(self, in_filename, chunksize=24 * __KILO_BYTE__, data_encoding='ascii'):
        understand = False
        encrypted_filesize = os.path.getsize(in_filename)
        with open(in_filename, 'rb') as (infile):
            with BytesIO('') as (outfile):
                self.decrypt_common(infile, outfile, encrypted_filesize, chunksize, understand)
                decrypted_data_byte = outfile.getvalue()
        data = decrypted_data_byte.decode(data_encoding)
        return data