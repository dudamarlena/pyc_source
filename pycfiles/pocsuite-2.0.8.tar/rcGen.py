# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hysia/Code/Pocsuite/pocsuite/api/rcGen.py
# Compiled at: 2018-12-07 04:32:38
"""
Copyright (c) 2014-2016 pocsuite developers (https://seebug.org)
See the file 'docs/COPYING' for copying permission
"""
import os

def initial():
    currentUserHomePath = os.path.expanduser('~')
    _ = '[Telnet404]\nAccount = Your Telnet404 Account\npassword = Your Telnet404 Password'
    if not os.path.isfile(currentUserHomePath + '/.pocsuiterc'):
        with open(currentUserHomePath + '/.pocsuiterc', 'w') as (fp):
            fp.write(_)


initial()