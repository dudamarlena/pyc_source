# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/common/SSHkey.py
# Compiled at: 2017-04-23 10:30:41
from __future__ import print_function
import base64, hashlib, struct
from os.path import basename
from cloudmesh_client.common.ConfigDict import Config

class SSHkey(object):

    def __init__(self, file_path=None, keyname=None):
        self.__key__ = None
        self.read(file_path, keyname)
        return

    def get(self):
        return self.__key__

    def __str__(self):
        return self.__key__['key']

    def __repr__(self):
        return self.__key__['key']

    def read(self, file_path, keyname=None):
        self.__key__ = {}
        if file_path is not None:
            orig_path = file_path
            file_path = Config.path_expand(file_path)
            uri = ('file://{}').format(file_path)
            self.__key__ = {'uri': uri, 
               'path': orig_path, 
               'string': open(file_path, 'r').read().rstrip()}
            self.__key__['type'], self.__key__['key'], self.__key__['comment'] = self._parse(self.__key__['string'])
            self.__key__['fingerprint'] = self._fingerprint(self.__key__['string'])
            if keyname is None:
                name = basename(file_path).replace('.pub', '').replace('id_', '')
            else:
                name = keyname
            self.__key__['name'] = name
            self.__key__['comment'] = self.__key__['comment']
            self.__key__['source'] = 'ssh'
        return self.__key__

    @property
    def fingerprint(self):
        return self.__key__['fingerprint']

    @property
    def key(self):
        return self.__key__['string']

    @property
    def type(self):
        return self.__key__['type']

    @property
    def comment(self):
        return self.__key__['comment']

    @classmethod
    def _fingerprint(cls, entirekey):
        """returns the fingerprint of a key.
        :param entirekey: the key
        :type entirekey: string
        """
        t, keystring, comment = cls._parse(entirekey)
        if keystring is not None:
            return cls._key_fingerprint(keystring)
        else:
            return ''
            return

    @classmethod
    def _key_fingerprint(cls, key_string):
        """create the fingerprint form just the key.

        :param key_string: the key
        :type key_string: string
        """
        key_padding = key_string.strip() + '=' * (4 - len(key_string.strip()) % 4)
        key = base64.b64decode(key_padding.encode('ascii'))
        fp_plain = hashlib.md5(key).hexdigest()
        return (':').join(a + b for a, b in zip(fp_plain[::2], fp_plain[1::2]))

    @classmethod
    def _parse(cls, keystring):
        """
        parse the keystring/keycontent into type,key,comment
        :param keystring: the content of a key in string format
        """
        keysegments = keystring.split(' ', 2)
        keytype = keysegments[0]
        key = None
        comment = None
        if len(keysegments) > 1:
            key = keysegments[1]
            if len(keysegments) > 2:
                comment = keysegments[2]
        return (
         keytype, key, comment)

    def _validate(self, keytype, key):
        """reads the key string from a file. THIS FUNCTION HAS A BUG.

        :param key: either the name of  a file that contains the key, or the entire contents of such a file
        :param keytype: if 'file' the key is read form the file specified in key.
                        if 'string' the key is passed as a string in key
        """
        keystring = None
        if keytype.lower() == 'file':
            try:
                keystring = open(key, 'r').read()
            except:
                return False

        else:
            if keytype.lower() == 'string':
                keystring = key
            try:
                keytype, key_string, comment = self._parse(keystring)
                data = base64.decodestring(key_string)
                int_len = 4
                str_len = struct.unpack('>I', data[:int_len])[0]
                if data[int_len:int_len + str_len] == keytype:
                    return True
            except Exception as e:
                return False

        return

    def _keyname_sanitation(self, username, keyname):
        keynamenew = '%s_%s' % (
         username, keyname.replace('.', '_').replace('@', '_'))
        return keynamenew


def main():
    from pprint import pprint
    sshkey = SSHkey('~/.ssh/id_rsa.pub')
    pprint(sshkey.key)
    print('Fingerprint:', sshkey.fingerprint)
    pprint(sshkey.__key__)
    print('sshkey', sshkey)
    print('str', str(sshkey))
    print(sshkey.type)
    print(sshkey.__key__['key'])
    print(sshkey.key)
    print(sshkey.comment)


if __name__ == '__main__':
    main()