# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/nacl/ldap/password.py
# Compiled at: 2007-12-02 16:26:58
import base64, string, md5, sha
from random import choice
from salamoia.h2o.logioni import *

class PasswordHasher(object):
    __module__ = __name__

    def __init__(self, password):
        self.password = password

    def hash(self, algo='SHA'):
        salt = ''
        password = self.password
        if algo == 'CLEARTEXT':
            return self.password
        if 'SHA' in algo:
            module = sha
        elif 'MD5' in algo:
            module = md5
        else:
            raise 'unsupported encryption'
        if algo == 'SSHA' or algo == 'SMD5':
            for i in range(0, 4):
                salt += choice(string.ascii_letters + string.digits)

            password += salt
        if type(password) == list:
            Ione.log("PASSSWORD '%s' e' lista" % password)
        return '{%s}%s' % (algo, base64.encodestring(module.new(password).digest() + salt))


from salamoia.tests import *
runDocTests()