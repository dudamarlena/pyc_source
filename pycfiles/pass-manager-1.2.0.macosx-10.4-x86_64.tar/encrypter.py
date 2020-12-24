# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Komurasaki/.anyenv/envs/pyenv/versions/2.7.6/lib/python2.7/site-packages/src/encrypter.py
# Compiled at: 2014-04-23 00:22:27
"""
file Encrypter for pass-manager
"""
import crypto, os

class Encrypter(object):
    """ file encrypter
    """
    PRIVATE = ('{home}/.ssh/.pass-manager_rsa').format(home=os.environ['HOME'])
    PUBLIC = ('{home}/.ssh/.pass-manager_rsa.pub').format(home=os.environ['HOME'])

    def __init__(self):
        self.public = None
        self.private = None
        if not os.path.exists(self.PRIVATE) or not os.path.exists(self.PUBLIC):
            self.public, self.private = crypto.newkeys(512)
            self.save_secret_files()
        return

    def save_secret_files(self):
        """ save public, private keys
        """
        crypto.export_key_file(self.public, self.PUBLIC)
        crypto.export_key_file(self.private, self.PRIVATE)
        return True

    def load_secret_files(self):
        """ set public, private keys to self
        """
        if not self.public and not self.private:
            self.public = crypto.load_key_file(self.PUBLIC)
            self.private = crypto.load_key_file(self.PRIVATE)

    def decrypt(self, encrypted_file_content):
        """ decrypt encrypted_file_content
        """
        self.load_secret_files()
        decrypted_file_content = crypto.decrypt(encrypted_file_content, self.private)
        return decrypted_file_content

    def encrypt(self, file_content):
        """ encrypt not_encrypted_file_content
        """
        self.load_secret_files()
        encrypted_file_content = crypto.encrypt(file_content, self.public)
        return encrypted_file_content