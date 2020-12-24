# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/hysia/Code/Pocsuite/pocsuite/api/rcGen.py
# Compiled at: 2018-12-07 04:32:38
__doc__ = "\nCopyright (c) 2014-2016 pocsuite developers (https://seebug.org)\nSee the file 'docs/COPYING' for copying permission\n"
import os

def initial():
    currentUserHomePath = os.path.expanduser('~')
    _ = '[Telnet404]\nAccount = Your Telnet404 Account\npassword = Your Telnet404 Password'
    if not os.path.isfile(currentUserHomePath + '/.pocsuiterc'):
        with open(currentUserHomePath + '/.pocsuiterc', 'w') as (fp):
            fp.write(_)


initial()