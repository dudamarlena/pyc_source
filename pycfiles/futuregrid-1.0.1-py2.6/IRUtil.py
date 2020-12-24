# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/futuregrid/image/repository/server/IRUtil.py
# Compiled at: 2012-09-06 11:03:15
"""
utility class for static methods
"""
import sys, os
from random import randrange
import hashlib
from futuregrid.utils import FGTypes, FGAuth

def getImgId():
    imgId = str(randrange(999999999999999999999999))
    return imgId


def auth(userId, cred):
    return FGAuth.auth(userId, cred)


if __name__ == '__main__':
    m = hashlib.md5()
    m.update('REMOVED')
    passwd_input = m.hexdigest()
    cred = FGTypes.FGCredential('ldappassmd5', passwd_input)
    if auth('USER', cred):
        print 'logged in'
    else:
        print 'access denied'