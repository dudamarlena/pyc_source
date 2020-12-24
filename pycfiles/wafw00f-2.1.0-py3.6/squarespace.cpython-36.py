# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wafw00f/plugins/squarespace.py
# Compiled at: 2020-02-20 22:34:09
# Size of source mod 2**32: 580 bytes
"""
Copyright (C) 2020, WAFW00F Developers.
See the LICENSE file for copying permission.
"""
NAME = 'Squarespace (Squarespace)'

def is_waf(self):
    schemes = [
     self.matchHeader(('Server', 'Squarespace')),
     self.matchCookie('^SS_ANALYTICS_ID='),
     self.matchCookie('^SS_MATTR='),
     self.matchCookie('^SS_MID='),
     self.matchCookie('SS_CVT='),
     self.matchContent('status\\.squarespace\\.com'),
     self.matchContent('BRICK\\-\\d{2}')]
    if any(i for i in schemes):
        return True
    else:
        return False