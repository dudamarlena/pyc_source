# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\GitHub\django-encrypted-cookie-session-py3\encrypted_cookies\keygen.py
# Compiled at: 2015-10-17 16:30:34
# Size of source mod 2**32: 605 bytes
import optparse, sys
from cryptography.fernet import Fernet

def main(stdout=sys.stdout, argv=sys.argv[1:]):
    p = optparse.OptionParser(usage='%prog [options]\n\nGenerates a suitable value to put in your ENCRYPTED_COOKIE_KEYS=[...] setting.')
    options, args = p.parse_args(argv)
    stdout.write(Fernet.generate_key().decode('utf-8'))


if __name__ == '__main__':
    main()