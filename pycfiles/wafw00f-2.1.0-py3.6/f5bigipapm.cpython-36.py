# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wafw00f/plugins/f5bigipapm.py
# Compiled at: 2020-02-20 22:34:09
# Size of source mod 2**32: 733 bytes
"""
Copyright (C) 2020, WAFW00F Developers.
See the LICENSE file for copying permission.
"""
NAME = 'BIG-IP AP Manager (F5 Networks)'

def is_waf(self):
    schema1 = [
     self.matchCookie('^LastMRH_Session'),
     self.matchCookie('^MRHSession')]
    schema2 = [
     self.matchCookie('^MRHSession'),
     self.matchHeader(('Server', 'Big([-_])?IP'), attack=True)]
    schema3 = [
     self.matchCookie('^F5_fullWT'),
     self.matchCookie('^F5_fullWT'),
     self.matchCookie('^F5_HT_shrinked')]
    if all(i for i in schema1):
        return True
    if all(i for i in schema2):
        return True
    else:
        if any(i for i in schema3):
            return True
        return False