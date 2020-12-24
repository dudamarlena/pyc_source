# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wafw00f/plugins/siteguard.py
# Compiled at: 2020-02-20 22:34:09
# Size of source mod 2**32: 378 bytes
"""
Copyright (C) 2020, WAFW00F Developers.
See the LICENSE file for copying permission.
"""
NAME = 'SiteGuard (Sakura Inc.)'

def is_waf(self):
    schemes = [
     self.matchContent('Powered by SiteGuard'),
     self.matchContent('The server refuse to browse the page')]
    if any(i for i in schemes):
        return True
    else:
        return False