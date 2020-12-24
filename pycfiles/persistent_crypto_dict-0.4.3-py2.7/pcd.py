# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pcd.py
# Compiled at: 2013-02-04 15:44:54
from __future__ import with_statement
import hmac, hashlib
from Crypto.Cipher import AES
from contextlib import closing
from base64 import b64encode, b64decode
import sqlite3

class sha512:
    digest_size = 64

    def new(self, inp=''):
        return hashlib.sha512(inp)


CREATE_SQL = 'CREATE TABLE if not exists pcd_urlcache (key TEXT PRIMARY KEY, value TEXT);'

class PersistentCryptoDict:

    def __init__(self, filename='pcd.db', salt='3j3,xiDS'):
        self.salt = salt
        self.db = sqlite3.connect(filename)
        cursor = self.db.cursor()
        cursor.executescript(CREATE_SQL)
        self.db.commit()
        cursor.close()
        self.db.close()
        self.db = sqlite3.connect(filename)

    def __setitem__(self, key, value):
        B, C = self.get_key(key)
        ciphertext = self.encrypt(C, value)
        self.query_db('INSERT OR REPLACE INTO pcd_urlcache (key, value) VALUES (?, ?)', (B, ciphertext))

    def __getitem__(self, key):
        B, C = self.get_key(key)
        value = self.query_db('SELECT value FROM pcd_urlcache WHERE key == ? LIMIT 1', (B,))
        if value:
            return self.decrypt(C, value)

    def query_db(self, query, params=[]):
        with closing(self.db.cursor()) as (cursor):
            cursor.execute(query, params)
            self.db.commit()
            return (cursor.fetchone() or [None])[0]
        return

    def get_key(self, key):
        A = hmac.new(self.salt, key, sha512())
        return (A.hexdigest()[:64],
         A.digest()[32:])

    def encrypt(self, C, value):
        bsize = len(C)
        cipher = AES.new(C, AES.MODE_OFB, '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        value += chr(8) * (-len(value) % bsize)
        return b64encode(('').join([ cipher.encrypt(value[i * bsize:(i + 1) * bsize]) for i in range(len(value) / bsize)
                                   ]))

    def decrypt(self, C, value):
        value = b64decode(value)
        cipher = AES.new(C, AES.MODE_OFB, '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        bsize = len(C)
        return ('').join([ cipher.decrypt(value[i * bsize:(i + 1) * bsize]) for i in range(len(value) / bsize)
                         ]).rstrip(chr(8))


if __name__ == '__main__':
    import sys
    d = PersistentCryptoDict('pcd.db')
    if len(sys.argv) == 3:
        d[sys.argv[1]] = sys.argv[2]
    elif len(sys.argv) == 2:
        print d[sys.argv[1]]
    else:
        print d['my key']
        d['my key'] = 'secret value'
        print d['my key']
        d['my key'] = 'top secret value'
        print d['my key']