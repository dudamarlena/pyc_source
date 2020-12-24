# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hans/workspace/keepassdb/keepassdb/util.py
# Compiled at: 2013-01-01 20:29:42
__authors__ = [
 'Hans Lellelid <hans@xmpl.org>']
__license__ = '\nkeepassdb is free software: you can redistribute it and/or modify it under the terms\nof the GNU General Public License as published by the Free Software Foundation,\neither version 3 of the License, or at your option) any later version.\n\nkeepassdb is distributed in the hope that it will be useful, but WITHOUT ANY\nWARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR\nA PARTICULAR PURPOSE. See the GNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License along with\nkeepassdb.  If not, see <http://www.gnu.org/licenses/>.\n'
import struct
from datetime import datetime
import hashlib
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

def derive_key(seed_key, seed_rand, rounds, password=None, keyfile=None):
    """
    Derives the correct (final) master key from the password and/or keyfile and
    sepcified transform seed & num rounds.
    """
    if password == '':
        password = None
    if keyfile == '':
        keyfile = None
    if password is None and keyfile is None:
        raise ValueError('Password and/or keyfile is required.')
    if password is None:
        masterkey = key_from_keyfile(keyfile)
    elif password and keyfile:
        passwordkey = key_from_password(password)
        filekey = key_from_keyfile(keyfile)
        sha = SHA256.new()
        sha.update(passwordkey + filekey)
        masterkey = sha.digest()
    else:
        masterkey = key_from_password(password)
    final_key = transform_key(masterkey, seed_key=seed_key, seed_rand=seed_rand, rounds=rounds)
    return final_key


def key_from_keyfile(keyfile):
    """
    This method reads in the bytes in the keyfile and returns the
    SHA256 as the key.
    
    :param keyfile: The path to a key file or a file-like object.
    """
    if hasattr(keyfile, 'read'):
        buf = keyfile.read()
    else:
        with open(keyfile, 'rb') as (fp):
            buf = fp.read()
    sha = SHA256.new()
    if len(buf) == 33:
        sha.update(buf)
        return sha.digest()
    else:
        if len(buf) == 65:
            sha.update(struct.unpack('<65s', buf)[0].decode())
            return sha.digest()
        while buf:
            if len(buf) <= 2049:
                sha.update(buf)
                buf = ''
            else:
                sha.update(buf[:2048])
                buf = buf[2048:]

        return sha.digest()


def key_from_password(password):
    """This method just hashes self.password."""
    if isinstance(password, unicode):
        password = password.encode('utf-8')
    if not isinstance(password, bytes):
        raise TypeError('password must be byte string, not %s' % type(password))
    sha = SHA256.new()
    sha.update(password)
    return sha.digest()


def transform_key(startkey, seed_key, seed_rand, rounds):
    """
    This method creates the key to decrypt the database.
    """
    masterkey = startkey
    aes = AES.new(seed_key, AES.MODE_ECB)
    for _i in range(rounds):
        masterkey = aes.encrypt(masterkey)

    masterkey = hashlib.sha256(masterkey).digest()
    return hashlib.sha256(seed_rand + masterkey).digest()


def decrypt_aes_cbc(ciphertext, key, iv):
    """
    This method decrypts contents and strips padding.
    
    :rtype: bytes
    """
    if not isinstance(ciphertext, bytes):
        raise TypeError('content to decrypt must by bytes.')
    aes = AES.new(key, AES.MODE_CBC, iv)
    decrypted_content = aes.decrypt(ciphertext)
    padding = ord(decrypted_content[-1:len(decrypted_content)])
    decrypted_content = decrypted_content[:len(decrypted_content) - padding]
    return decrypted_content


def encrypt_aes_cbc(cleartext, key, iv):
    """
    This method encrypts the content.
    
    :rtype: bytes
    """
    if isinstance(cleartext, unicode):
        cleartext = cleartext.encode('utf8')
    elif isinstance(cleartext, bytearray):
        cleartext = bytes(cleartext)
    if not isinstance(cleartext, bytes):
        raise TypeError('content to encrypt must by bytes.')
    aes = AES.new(key, AES.MODE_CBC, iv)
    padding = AES.block_size - len(cleartext) % AES.block_size
    cleartext += chr(padding).encode('utf-8') * padding
    return aes.encrypt(cleartext)


def now():
    """
    Save some typing by providing a datetime.now() object w/o the microsecond precision.
    """
    return datetime.now().replace(microsecond=0)