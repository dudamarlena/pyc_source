# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wafw00f/plugins/sucuri.py
# Compiled at: 2020-02-20 22:34:09
# Size of source mod 2**32: 873 bytes
"""
Copyright (C) 2020, WAFW00F Developers.
See the LICENSE file for copying permission.
"""
NAME = 'Sucuri CloudProxy (Sucuri Inc.)'

def is_waf(self):
    schemes = [
     self.matchHeader(('X-Sucuri-ID', '.+?')),
     self.matchHeader(('X-Sucuri-Cache', '.+?')),
     self.matchHeader(('Server', 'Sucuri(\\-Cloudproxy)?')),
     self.matchHeader(('X-Sucuri-Block', '.+?'), attack=True),
     self.matchContent('Access Denied.{0,6}?Sucuri Website Firewall'),
     self.matchContent('<title>Sucuri WebSite Firewall.{0,6}?(CloudProxy)?.{0,6}?Access Denied'),
     self.matchContent('sucuri\\.net/privacy\\-policy'),
     self.matchContent('cdn\\.sucuri\\.net/sucuri[-_]firewall[-_]block\\.css'),
     self.matchContent('cloudproxy@sucuri\\.net')]
    if any(i for i in schemes):
        return True
    else:
        return False