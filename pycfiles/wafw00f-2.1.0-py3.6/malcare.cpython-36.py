# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wafw00f/plugins/malcare.py
# Compiled at: 2020-02-20 22:34:09
# Size of source mod 2**32: 406 bytes
"""
Copyright (C) 2020, WAFW00F Developers.
See the LICENSE file for copying permission.
"""
NAME = 'Malcare (Inactiv)'

def is_waf(self):
    schemes = [
     self.matchContent('firewall.{0,15}?powered.by.{0,15}?malcare.{0,15}?pro'),
     self.matchContent('blocked because of malicious activities')]
    if any(i for i in schemes):
        return True
    else:
        return False