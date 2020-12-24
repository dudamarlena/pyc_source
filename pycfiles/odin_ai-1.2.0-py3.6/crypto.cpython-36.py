# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/odin/utils/crypto.py
# Compiled at: 2019-02-01 09:39:26
# Size of source mod 2**32: 12166 bytes
from __future__ import print_function, division, absolute_import
import os, base64, struct, pickle, hashlib, zipfile
from io import BytesIO
from six import string_types
import numpy as np, scipy as sp

def to_password(password, salt=None):
    """ This function return the byte data of hashed password """
    if isinstance(password, string_types):
        password = password.encode('utf-8')
    password += str(salt).encode('utf-8')
    return hashlib.sha256(password).digest()


def _data_to_iobuffer(file_or_data):
    own_file = True
    if isinstance(file_or_data, string_types):
        if os.path.exists(file_or_data):
            filesize = os.path.getsize(file_or_data)
            infile = open(file_or_data, 'rb')
        else:
            filesize = len(file_or_data)
            infile = BytesIO(file_or_data.encode())
    else:
        if isinstance(file_or_data, bytes):
            filesize = len(file_or_data)
            infile = BytesIO(file_or_data)
        else:
            if hasattr(file_or_data, 'read'):
                filesize = os.fstat(file_or_data.fileno()).st_size
                infile = file_or_data
                own_file = False
            else:
                raise ValueError('No support for MD5 of input type: %s' % str(file_or_data))
    return (
     infile, filesize, own_file)


def md5_checksum(file_or_path, chunksize=524288):
    """ Calculating MD5 checksum

  Parameters
  ---------
  file_or_path : object
    One of the following
      - File object
      - string path to a folder
      - string path to a file
      - Bytes array
      - Numpy array
      - List or iterator of numpy array
  chunksize : int (in bytes)
    size of each chunk for updating MD5 value
  """
    chunksize = int(chunksize)
    hash_md5 = hashlib.md5()
    own_file = False
    if isinstance(file_or_path, np.ndarray) or isinstance(file_or_path, (tuple, list)) and all(isinstance(i, np.ndarray) for i in file_or_path):
        if not isinstance(file_or_path, (tuple, list)):
            file_or_path = (
             file_or_path,)
        f = BytesIO()
        for arr in file_or_path:
            np.save(file=f, arr=arr, allow_pickle=False)

        f.seek(0)
        own_file = True
    else:
        if isinstance(file_or_path, string_types):
            if os.path.isfile(file_or_path):
                f = open(file_or_path, 'rb')
                own_file = True
            else:
                if os.path.isdir(file_or_path):
                    for fpath in sorted(os.listdir(file_or_path)):
                        fpath = os.path.join(file_or_path, fpath)
                        with open(fpath, 'rb') as (f):
                            for chunk in iter(lambda : f.read(chunksize), b''):
                                hash_md5.update(chunk)

                    return hash_md5.hexdigest()
                else:
                    hash_md5.update(file_or_path.encode('utf-8'))
                    return hash_md5.hexdigest()
        else:
            if isinstance(file_or_path, bytes):
                hash_md5.update(file_or_path)
                return hash_md5.hexdigest()
    if hasattr(file_or_path, 'read'):
        f = file_or_path
    else:
        if hasattr(file_or_path, 'shape'):
            if isinstance(file_or_path, sp.sparse.coo_matrix):
                file_or_path = file_or_path.todense()
            itemsize = np.dtype(file_or_path.dtype).itemsize
            batch_size = int(max(chunksize // (itemsize * np.prod(file_or_path.shape[1:])), 8))
            indices = range(0, file_or_path.shape[0] + batch_size, batch_size)
            for start, end in zip(indices, indices[1:]):
                x = file_or_path[start:end].tobytes()
                hash_md5.update(x)

            return hash_md5.hexdigest()
        raise ValueError('MD5 checksum has NO support for input: %s' % str(file_or_path))
    for chunk in iter(lambda : f.read(chunksize), b''):
        hash_md5.update(chunk)

    if own_file:
        f.close()
    return hash_md5.hexdigest()


def encrypt_aes(file_or_data, password=None, outfile=None, iv=None, salt=None, mode=None, base64encode=False, chunksize=524288):
    """ Flexible implementaiton of AES encryption

  Parameters
  ----------
  file_or_data : {BufferObject, string, bytes}
    input data will be converted to bytes sequence for encryption
  password : {str, None}
    if None, a prompt will ask for inputing password
  outfile : {None, path, file}
    if None, return raw encrypted data
  iv : initial vector
    16 bytes
  salt : {None, string, bytes}
    salt for password Hashing
  mode : Cipher.AES.MODE_*
    default `None` is converted to `Crypto.Cipher.AES.MODE_CBC`
  chunksize : int
    encryption chunk, multiple of 16.
  """
    try:
        from Crypto.Cipher import AES
    except ImportError as e:
        raise ImportError("Require 'pycrypto' to run this function")

    if mode is None:
        mode = AES.MODE_CBC
    else:
        if password is None:
            password = input('Your password: ')
        assert len(password) > 0, 'Password length must be greater than 0'
    password = to_password(password, salt=salt)
    if iv is None:
        iv = os.urandom(16)
    encryptor = AES.new(password, mode, IV=iv)
    infile, filesize, own_file = _data_to_iobuffer(file_or_data)
    close_file = False
    if isinstance(outfile, string_types):
        if os.path.exists(os.path.dirname(outfile)):
            outfile = open(str(outfile), 'wb')
            close_file = True
    if hasattr(outfile, 'write'):
        if hasattr(outfile, 'flush'):
            close_file = True
        else:
            outfile = BytesIO()
    else:
        outfile.write(struct.pack('<Q', filesize))
        outfile.write(iv)
        while True:
            chunk = infile.read(chunksize)
            if bool(base64encode):
                chunk = base64.encodebytes(chunk)
            if len(chunk) == 0:
                break
            else:
                if len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - len(chunk) % 16)
            outfile.write(encryptor.encrypt(chunk))

        if own_file:
            infile.close()
        outfile.flush()
        if close_file:
            outfile.close()
        else:
            outfile.seek(0)
            data = outfile.read()
            outfile.close()
            return data


def decrypt_aes(file_or_data, password=None, outfile=None, salt=None, mode=None, base64encode=False, chunksize=524288):
    """ Flexible implementaiton of AES decryption

  Parameters
  ----------
  file_or_data : {BufferObject, string, bytes}
    input data will be converted to bytes sequence for encryption
  password : {str, None}
    if None, a prompt will ask for inputing password
  outfile : {None, path, file}
    if None, return raw encrypted data
  salt : {None, string, bytes}
    salt for password Hashing
  mode : Cipher.AES.MODE_*
  chunksize : int
    encryption chunk, multiple of 16.
  """
    try:
        from Crypto.Cipher import AES
    except ImportError as e:
        raise ImportError("Require 'pycrypto' to run this function")

    if mode is None:
        mode = AES.MODE_CBC
    else:
        if password is None:
            password = input('Your password: ')
        assert len(password) > 0, 'Password length must be greater than 0'
    password = to_password(password, salt)
    infile, filesize, own_file = _data_to_iobuffer(file_or_data)
    origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
    iv = infile.read(16)
    decryptor = AES.new(password, mode=(AES.MODE_CBC), IV=iv)
    close_file = False
    if isinstance(outfile, string_types):
        if os.path.exists(os.path.dirname(outfile)):
            outfile = open(str(outfile), 'wb')
            close_file = True
    if hasattr(outfile, 'write'):
        if hasattr(outfile, 'flush'):
            close_file = True
        else:
            outfile = BytesIO()
    else:
        while True:
            chunk = infile.read(chunksize)
            if len(chunk) == 0:
                break
            chunk = decryptor.decrypt(chunk)
            if bool(base64encode):
                chunk = base64.decodebytes(chunk)
            outfile.write(chunk)

        outfile.truncate(origsize)
        if own_file:
            infile.close()
        outfile.flush()
        if close_file:
            outfile.close()
        else:
            outfile.seek(0)
            data = outfile.read()
            outfile.close()
            return data


def zip_aes(in_path, out_path, password=None, compression=True, verbose=False):
    """
  Parameters
  ----------
  in_path : string
    path to a folder
  out_path : string
    path to output zip file
  """
    if password is None:
        password = input('Your password:')
    else:
        password = str(password)
        assert len(password) > 0, '`password`=%s length must be greater than 0' % password
        from odin.utils import get_all_files
        if not os.path.isdir(in_path):
            raise ValueError('`in_path` to %s is not a folder' % str(in_path))
        all_files = get_all_files(in_path)
        raise isinstance(out_path, string_types) or ValueError('`out_path` must be string')
    f = zipfile.ZipFile(out_path, 'w', compression=(zipfile.ZIP_DEFLATED if bool(compression) else zipfile.ZIP_STORED),
      allowZip64=True)
    md5_map = {}
    for path in all_files:
        name = os.path.basename(path)
        md5_map[name] = md5_checksum(path)
        f.writestr(name, encrypt_aes(path, password + name))
        if verbose:
            print('Compressed: "%s"' % name, '(MD5:%s)' % md5_map[name])

    f.writestr('_MD5_CHECKSUM_', pickle.dumps(md5_map))
    f.close()


def unzip_aes(in_path, out_path=None, password=None, compression=True, verbose=False):
    """
  Parameters
  ----------
  in_path : string
    path to input zip file
  out_path : {string, None}
    if None, return iteration of tuple (name, decompressed data),
    otherwise, saving the decompressed data to the given folder

  """
    if password is None:
        password = input('Your password:')
    else:
        password = str(password)
        assert len(password) > 0, '`password`=%s length must be greater than 0' % password
        if not os.path.isfile(in_path):
            raise ValueError('`in_path` to %s is not a file' % str(in_path))
        if out_path is not None:
            if os.path.isfile(out_path):
                raise ValueError('`out_path` must be a folder')
            elif not os.path.exists(out_path):
                os.mkdir(out_path)
    with zipfile.ZipFile(in_path, 'r', compression=(zipfile.ZIP_DEFLATED if bool(compression) else zipfile.ZIP_STORED),
      allowZip64=True) as (fzip):
        md5_map = pickle.loads(fzip.read(name='_MD5_CHECKSUM_'))
        for name in fzip.namelist():
            if '_MD5_CHECKSUM_' == name:
                pass
            else:
                data = fzip.read(name=name)
                data = decrypt_aes(data, password=(password + name))
                md5 = md5_checksum(data)
                assert md5 == md5_map[name], "MD5 mismatch for data name: '%s', probably caused by wrong password!" % name
                if verbose:
                    print('Decompressed: "%s"' % name, '(MD5:%s)' % md5)
            if out_path is not None:
                path = out_path
                for d in name.split('/')[:-1]:
                    path += '/' + d
                    if os.path.exists(path):
                        os.mkdir(path)

                with open((os.path.join(path, name.split('/')[(-1)])), mode='wb') as (f):
                    f.write(data)
            else:
                yield (
                 name, data)