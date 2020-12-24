# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wafw00f/plugins/yundun.py
# Compiled at: 2020-02-20 22:34:09
# Size of source mod 2**32: 595 bytes
"""
Copyright (C) 2020, WAFW00F Developers.
See the LICENSE file for copying permission.
"""
NAME = 'Yundun (Yundun)'

def is_waf(self):
    schemes = [
     self.matchHeader(('Server', 'YUNDUN')),
     self.matchHeader(('X-Cache', 'YUNDUN')),
     self.matchCookie('^yd_cookie='),
     self.matchContent('Blocked by YUNDUN Cloud WAF'),
     self.matchContent('yundun\\.com/yd[-_]http[_-]error/'),
     self.matchContent('www\\.yundun\\.com/(static/js/fingerprint\\d{1}?\\.js)?')]
    if any(i for i in schemes):
        return True
    else:
        return False