# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\django_auth_pubtkt\auth_pubtkt.py
# Compiled at: 2018-03-10 14:37:29
from M2Crypto import RSA, DSA
import hashlib, time, base64, six

class Authpubtkt(object):
    filename = None
    pub_key = None

    def __init__(self, filename=None, pub_key=None):
        if filename:
            self.filename = filename
            try:
                pub_key = DSA.load_pub_key(filename)
            except DSA.DSAError:
                pass

            if pub_key is None:
                pub_key = RSA.load_pub_key(filename)
        if pub_key is None:
            raise ValueError('Please specify filename or public key')
        if not isinstance(pub_key, RSA.RSA_pub) and not isinstance(pub_key, DSA.DSA_pub):
            raise ValueError('Unknown key type: %s' % type(pub_key))
        self.pub_key = pub_key
        return

    def verify_ticket_signature(self, data, sig):
        """Verify ticket signature. """
        try:
            signature = base64.b64decode(sig)
        except TypeError as e:
            if hasattr(self, 'debug'):
                print 'Exception in function base64.b64decode. File %s' % __file__
                print '%s' % e
            return False

        if six.PY3:
            data = data.encode('utf-8')
        digest = hashlib.sha1(data).digest()
        if isinstance(self.pub_key, RSA.RSA_pub):
            try:
                self.pub_key.verify(digest, signature, 'sha1')
            except RSA.RSAError:
                return False

            return True
        if isinstance(self.pub_key, DSA.DSA_pub):
            try:
                return self.pub_key.verify_asn1(digest, signature)
            except DSA.DSAError as e:
                if hasattr(self, 'debug'):
                    print 'Exception in function self.pub_key.verify_asn1(digest, signature). File %s' % __file__
                    print '%s' % e
                return False

        return False

    def verify_cookie(self, cookie):
        data = cookie.rsplit(';', 1)[0]
        signature = cookie.rsplit(';', 1)[1][4:]
        if not self.verify_ticket_signature(data, signature):
            return
        else:
            data = data.split(';')
            ticket_keys = dict()
            for item in data:
                ticket_keys[item.split('=')[0]] = item.split('=')[1]

            try:
                if float(ticket_keys['validuntil']) < time.time():
                    if hasattr(self, 'debug'):
                        print 'Ticket expired: %s' % ticket_keys['validuntil']
                    return
            except KeyError:
                return

            return ticket_keys