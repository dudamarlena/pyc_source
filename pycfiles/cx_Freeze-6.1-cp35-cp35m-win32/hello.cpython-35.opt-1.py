# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \.\cx_Freeze\samples\simple\hello.py
# Compiled at: 2019-08-29 22:24:39
# Size of source mod 2**32: 680 bytes
from datetime import datetime
import sys
from sys import stdout
stdout.write('Hello from cx_Freeze\n')
stdout.write('The current date is %s\n\n' % datetime.today().strftime('%B %d, %Y %H:%M:%S'))
stdout.write('Executable: %r\n' % sys.executable)
stdout.write('Prefix: %r\n' % sys.prefix)
stdout.write('Default encoding: %r\n' % sys.getdefaultencoding())
stdout.write('File system encoding: %r\n\n' % sys.getfilesystemencoding())
stdout.write('ARGUMENTS:\n')
for a in sys.argv:
    stdout.write('%s\n' % a)

stdout.write('\n')
stdout.write('PATH:\n')
for p in sys.path:
    stdout.write('%s\n' % p)

stdout.write('\n')