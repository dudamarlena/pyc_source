# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wafw00f/plugins/fortiweb.py
# Compiled at: 2020-02-20 22:34:09
# Size of source mod 2**32: 652 bytes
"""
Copyright (C) 2020, WAFW00F Developers.
See the LICENSE file for copying permission.
"""
NAME = 'FortiWeb (Fortinet)'

def is_waf(self):
    schema1 = [
     self.matchCookie('^FORTIWAFSID='),
     self.matchContent('.fgd_icon')]
    schema2 = [
     self.matchContent('fgd_icon'),
     self.matchContent('web.page.blocked'),
     self.matchContent('url'),
     self.matchContent('attack.id'),
     self.matchContent('message.id'),
     self.matchContent('client.ip')]
    if any(i for i in schema1):
        return True
    else:
        if all(i for i in schema2):
            return True
        return False