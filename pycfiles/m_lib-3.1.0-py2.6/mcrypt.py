# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/lib.linux-i686-2.6/m_lib/mcrypt.py
# Compiled at: 2016-07-25 13:26:50
from __future__ import print_function
import random, crypt
saltchars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcedfghijklmnopqrstuvwxyz0123456789./'
len_salt = len(saltchars)

def gen_salt():
    """
      There are some difference among modern unicies. BSD/OS, for example,
      uses MD5 hash, and ignores salt completely. FreeBSD uses 3 different
      versions of crypt() - with standard salt, with extended 9-byte salt,
      and MD5 (again, ignoring salt at all).
      This function generates salt for standard "Broken DES"-based crypt().
   """
    r1 = random.randint(0, len_salt - 1)
    r2 = random.randint(0, len_salt - 1)
    return '%s%s' % (saltchars[r1], saltchars[r2])


def test():
    try:
        raw_input
    except NameError:
        raw_input = input

    passwd = raw_input('Enter password: ')
    salt = gen_salt()
    encrypted = crypt.crypt(passwd, salt)
    pwd_file = open('test.pwd', 'w')
    pwd_file.write('%s:%s' % ('user', encrypted))
    pwd_file.close()
    print('Password file written')
    pwd_file = open('test.pwd', 'r')
    (username, encrypted) = pwd_file.readline()[:-1].split(':')
    pwd_file.close()
    if crypt.crypt(encrypted, encrypted):
        print('Password verified Ok')
    else:
        print('BAD password')


if __name__ == '__main__':
    test()