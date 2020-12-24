# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/virtualkeyring.py
# Compiled at: 2013-07-21 08:33:16
"""Utility script to build a set of strong yet rebuildable passwords

:author: Olivier Grisel <olivier.grisel@ensta.org>

The final password is build from a potentialy weak but easy to remember yet
secret master password and a domain-specific key like the name of the website
you are building a password for.

The password is then the 8th first characters of the letters + digits encoding
of sha1 digest of the concatenation of the master password and the domain key::

  >>> make_password("myprecious", "paypal")
  'muvcEizM'

  >>> make_password("myprecious", "jdoe@example.com", uppercase=False,
  ...               length=6)
  'ykn0nu'

  >>> make_password("myprecious", "jdoe@example.com", digits=False, length=10)
  'bdnrAGgJqe'

"""
from __future__ import print_function
import subprocess, optparse, pexpect, socket, string, sys, os
from time import sleep
from itertools import izip
from getpass import getpass
try:
    from hashlib import sha1
except ImportError:
    from sha import new as sha1

try:
    import xerox as clipboard
except ImportError:
    clipboard = None

ONE_BYTE = 256
DEFAULT_LENGTH = 8
DEFAULT_ALPHABET = string.lowercase + string.uppercase + string.digits

def bytes2number(bs):
    """Convert a python string (of bytes) into a python integer

    >>> bytes2number('0')
    48
    >>> bytes2number('00')
    12336
    >>> bytes2number('a0')
    24880

    """
    n = 0
    for i, c in izip(xrange(len(bs)), reversed(bs)):
        n += ord(c) * ONE_BYTE ** i

    return n


def number2string(n, alphabet='01'):
    """Compute the string representation of ``n`` in letters in ``alphabet``

    >>> number2string(0)
    '0'
    >>> number2string(1, '01')
    '1'
    >>> number2string(2, '01')
    '10'
    >>> number2string(3)
    '11'
    >>> number2string(4, '01')
    '100'

    >>> number2string(58, string.digits + 'abcdef')
    '3a'

    >>> number2string(-1, '01') #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    ValueError: -1 is not a natural number

    """
    base = len(alphabet)
    if n == 0:
        return alphabet[n]
    if n < 0:
        raise ValueError('%d is not a natural number' % n)
    acc = []
    while n != 0:
        n, remainder = divmod(n, base)
        acc.append(alphabet[remainder])

    return ('').join(reversed(acc))


def bytes2string(bs, alphabet):
    """Transcode a string of bytes into an arbitrary alphabet"""
    return number2string(bytes2number(bs), alphabet)


def make_password(master_password, domain_key, lowercase=True, uppercase=True, digits=True, length=DEFAULT_LENGTH, alphabet=None):
    """Build a password out of a master key and a domain key"""
    hash = sha1(master_password + domain_key).digest()
    if alphabet is None:
        alphabet = ''
        alphabet += lowercase and string.lowercase or ''
        alphabet += uppercase and string.uppercase or ''
        alphabet += digits and string.digits or ''
    if not alphabet:
        raise ValueError('empty alphabet')
    return bytes2string(hash, alphabet)[:length]


def get_password(domain_key=None, lowercase=True, uppercase=True, digits=True, length=DEFAULT_LENGTH, alphabet=None):
    """Prompt for master password and domain key. Return a password"""
    master_password = getpass('master password: ')
    if domain_key is None:
        domain_key = raw_input("domain key [e.g. 'login@host']: ")
    return make_password(master_password, domain_key, uppercase=uppercase, digits=digits, length=length, alphabet=alphabet)


def add_key():
    """print key and launch ssh-add
    """
    filename = os.path.expanduser('~/.virtualkeyring')
    if os.path.isfile(filename):
        host = open(filename).read()
        host = host.strip()
    else:
        host = socket.gethostname()
    try:
        passwd = get_password(host, length=20)
        child = pexpect.spawn('ssh-add')
        if child.expect('Enter passphrase for .*: ', timeout=3) == 0:
            child.sendline(passwd)
            if child.expect(pexpect.EOF, timeout=3) == 0:
                subprocess.call(['ssh-add', '-l'])
    except KeyboardInterrupt:
        pass


def parse_args(args):
    usage = 'vkr -l 10 -a abcdefghijklmnopqrstuvwyz0123456789'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-l', '--length', dest='length', default=DEFAULT_LENGTH, type='int', help='Lenght of the generated password (default: %d)' % DEFAULT_LENGTH)
    parser.add_option('-a', '--alphabet', dest='alphabet', default=DEFAULT_ALPHABET, help='Characters to be used for the generated password (default: %s)' % DEFAULT_ALPHABET)
    parser.add_option('-o', '--stdout', action='store_true', dest='stdout', default=False, help='Display the password to stdout')
    return parser.parse_args(args=args)


def main():
    options, _ = parse_args(sys.argv)
    use_clipboard = clipboard is not None and not options.stdout
    if use_clipboard:
        original_clipboard_content = clipboard.paste()
    try:
        try:
            passwd = get_password(length=options.length, alphabet=options.alphabet)
            if clipboard is None or options.stdout:
                print(passwd)
            else:
                clipboard.copy(passwd)
                print('Your password is available in the clipboard. You have 10s to paste it.')
                for i in range(10):
                    sleep(1)

        except KeyboardInterrupt:
            pass

    finally:
        if use_clipboard and original_clipboard_content:
            print('Restauring original clipboard content.')
            clipboard.copy(original_clipboard_content)

    return


if __name__ == '__main__':
    main()