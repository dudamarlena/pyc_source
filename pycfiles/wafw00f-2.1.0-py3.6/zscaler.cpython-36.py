# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wafw00f/plugins/zscaler.py
# Compiled at: 2020-02-20 22:34:09
# Size of source mod 2**32: 733 bytes
"""
Copyright (C) 2020, WAFW00F Developers.
See the LICENSE file for copying permission.
"""
NAME = 'ZScaler (Accenture)'

def is_waf(self):
    schemes = [
     self.matchHeader(('Server', 'ZScaler')),
     self.matchContent('Access Denied.{0,10}?Accenture Policy'),
     self.matchContent('policies\\.accenture\\.com'),
     self.matchContent('login\\.zscloud\\.net/img_logo_new1\\.png'),
     self.matchContent('Zscaler to protect you from internet threats'),
     self.matchContent('Internet Security by ZScaler'),
     self.matchContent('Accenture.{0,10}?webfilters indicate that the site likely contains')]
    if any(i for i in schemes):
        return True
    else:
        return False