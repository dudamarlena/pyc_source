# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Anaconda\Lib\site-packages\crib\crib.py
# Compiled at: 2014-12-02 14:19:18
from Crypto.Cipher import AES
import random, struct, hashlib, os

def keygen(password):
    return hashlib.sha256(password).digest()


def encrypt(key, file_name, chunksize=65536):
    output = file_name + '.crib'
    IV = ('').join(chr(random.randint(0, 255)) for i in range(16))
    encryptor = AES.new(key, AES.MODE_CBC, IV)
    try:
        file_size = os.path.getsize(file_name)
    except OSError as e:
        if e.errno == 2:
            print 'No such file found'
        else:
            print 'Unknown error in file reading'
        return 0

    try:
        with open(file_name, 'rb') as (infile):
            with open(output, 'wb') as (outfile):
                outfile.write(struct.pack('<Q', file_size))
                outfile.write(IV)
                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 16 != 0:
                        chunk += ' ' * (16 - len(chunk) % 16)
                        outfile.write(encryptor.encrypt(chunk))
                        return 1

    except IOError as e:
        if e.errno == 2:
            print 'No such file found'
        else:
            print 'Unknown error in file reading'
        return 0


def decrypt(key, file_name, chunksize=24576):
    output = os.path.splitext(file_name)[0]
    try:
        with open(file_name, 'rb') as (infile):
            origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
            IV = infile.read(16)
            decryptor = AES.new(key, AES.MODE_CBC, IV)
            with open(output, 'wb') as (outfile):
                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break
                    outfile.write(decryptor.decrypt(chunk))
                    outfile.truncate(origsize)
                    return 1

    except IOError as e:
        if e.errno == 2:
            print 'No such file found'
        else:
            print 'Unknow error in file reading'
        return 0