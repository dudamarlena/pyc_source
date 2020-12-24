# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /rbpowerpack/sshdb/models.py
# Compiled at: 2019-06-17 15:11:31
from __future__ import unicode_literals
import logging
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

import paramiko
from Crypto import Random
from Crypto.Cipher import AES
from django.db import models
from django.utils import six
from djblets.util.fields import Base64Field, Base64DecodedValue
from reviewboard.ssh.errors import UnsupportedSSHKeyError
from rbpowerpack.sshdb.secrets import get_sshdb_secret_key

class StoredHostKeys(models.Model):
    namespace = models.CharField(max_length=128, blank=True, null=True, unique=True)
    host_keys = models.TextField()


class StoredUserKey(models.Model):
    KEY_TYPES = {b'rsa': {b'name': b'RSA', 
                b'class': paramiko.RSAKey}, 
       b'dsa': {b'name': b'DSA', 
                b'class': paramiko.DSSKey}}
    KEY_CHOICES = [ (key, info[b'name']) for key, info in six.iteritems(KEY_TYPES)
                  ]
    namespace = models.CharField(max_length=128, blank=True, null=True)
    name = models.CharField(max_length=64, default=b'default')
    key_type = models.CharField(max_length=3, choices=KEY_CHOICES)
    enc_private_key = Base64Field(default=b'')
    timestamp = models.DateTimeField(auto_now=True)

    def get_key(self):
        info = self.KEY_TYPES.get(self.key_type, None)
        if not info:
            logging.critical(b'Invalid SSH key type "%s" stored in database (ID %d)' % (
             self.key_type, self.pk))
            return
        else:
            cls = info[b'class']
            key_data = self._decrypt(self.enc_private_key)
            fp = StringIO(key_data)
            key = cls.from_private_key(fp)
            fp.close()
            return key

    def set_key(self, key):
        found = False
        for key_type, info in six.iteritems(self.KEY_TYPES):
            if isinstance(key, info[b'class']):
                self.key_type = key_type
                found = True
                break

        if not found:
            raise UnsupportedSSHKeyError()
        fp = StringIO()
        key = key.write_private_key(fp)
        key_data = fp.getvalue()
        fp.close()
        self.enc_private_key = Base64DecodedValue(self._encrypt(key_data))

    def _encrypt(self, data):
        iv = Random.new().read(AES.block_size)
        cipher = self._create_cipher(iv)
        return iv + cipher.encrypt(data)

    def _decrypt(self, data):
        cipher = self._create_cipher(data[:AES.block_size])
        return cipher.decrypt(data[AES.block_size:])

    def _create_cipher(self, iv):
        return AES.new(get_sshdb_secret_key(), AES.MODE_CFB, iv)

    class Meta:
        unique_together = (('namespace', 'name'), )