# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \.\cx_Freeze\samples\asmodule\asmodule.py
# Compiled at: 2019-08-29 22:24:38
# Size of source mod 2**32: 755 bytes
import datetime, sys

def SayHello():
    sys.stdout.write('Hello from cx_Freeze\n')
    sys.stdout.write('The current date is %s\n\n' % datetime.datetime.today().strftime('%B %d, %Y %H:%M:%S'))
    sys.stdout.write('Executable: %r\n' % sys.executable)
    sys.stdout.write('Prefix: %r\n' % sys.prefix)
    sys.stdout.write('File system encoding: %r\n\n' % sys.getfilesystemencoding())
    sys.stdout.write('ARGUMENTS:\n')
    for a in sys.argv:
        sys.stdout.write('%s\n' % a)

    sys.stdout.write('\n')
    sys.stdout.write('PATH:\n')
    for p in sys.path:
        sys.stdout.write('%s\n' % p)

    sys.stdout.write('\n')


if __name__ == '__main__':
    SayHello()