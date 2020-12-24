# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wafw00f/plugins/aspnetgen.py
# Compiled at: 2020-02-20 22:34:09
# Size of source mod 2**32: 569 bytes
"""
Copyright (C) 2020, WAFW00F Developers.
See the LICENSE file for copying permission.
"""
NAME = 'ASP.NET Generic (Microsoft)'

def is_waf(self):
    schemes = [
     self.matchContent('iis (\\d+.)+?detailed error'),
     self.matchContent('potentially dangerous request querystring'),
     self.matchContent('application error from being viewed remotely (for security reasons)?'),
     self.matchContent('An application error occurred on the server')]
    if any(i for i in schemes):
        return True
    else:
        return False