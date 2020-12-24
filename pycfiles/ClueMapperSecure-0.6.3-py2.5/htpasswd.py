# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/clue/secure/htpasswd.py
# Compiled at: 2008-07-05 05:23:14
"""Replacement for htpasswd"""
import crypt, os, random

class HtpasswdFile:
    """A class for manipulating htpasswd files.

      >>> import tempfile
      >>> h, t = tempfile.mkstemp()
      >>> passwd = HtpasswdFile(t, True)

      >>> passwd.update('abc', 'def')
      >>> passwd.update('foo', 'bar')
      >>> passwd.update('abc', 'xyz')
      >>> passwd.delete('abc')
      >>> passwd.save()

      >>> passwd = HtpasswdFile(t, False)
      >>> os.remove(t)

      >>> passwd = HtpasswdFile(t, False)
      Traceback (most recent call last):
      Exception: ... does not exist

    """
    SALT_CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/.'

    def __init__(self, filename, create=False):
        self.entries = []
        self.filename = filename
        if not create:
            if os.path.exists(self.filename):
                self.load()
            else:
                raise Exception('%s does not exist' % self.filename)

    def gen_salt(self):
        return random.choice(self.SALT_CHARS) + random.choice(self.SALT_CHARS)

    def load(self):
        """Read the htpasswd file into memory."""
        lines = open(self.filename, 'r').readlines()
        self.entries = []
        for line in lines:
            (username, pwhash) = line.split(':')
            entry = [username, pwhash.rstrip()]
            self.entries.append(entry)

    def save(self):
        """Write the htpasswd file to disk"""
        open(self.filename, 'w').writelines([ '%s:%s\n' % (entry[0], entry[1]) for entry in self.entries
                                            ])

    def update(self, username, password):
        """Replace the entry for the given user, or add it if new."""
        pwhash = crypt.crypt(password, self.gen_salt())
        matching_entries = [ entry for entry in self.entries if entry[0] == username
                           ]
        if matching_entries:
            matching_entries[0][1] = pwhash
        else:
            self.entries.append([username, pwhash])

    def delete(self, username):
        """Remove the entry for the given user."""
        self.entries = [ entry for entry in self.entries if entry[0] != username
                       ]