# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wafw00f/plugins/yxlink.py
# Compiled at: 2020-02-20 22:34:09
# Size of source mod 2**32: 414 bytes
"""
Copyright (C) 2020, WAFW00F Developers.
See the LICENSE file for copying permission.
"""
NAME = 'YXLink (YxLink Technologies)'

def is_waf(self):
    schemes = [
     self.matchCookie('^yx_ci_session='),
     self.matchCookie('^yx_language='),
     self.matchHeader(('Server', 'Yxlink([\\-_]?WAF)?'))]
    if any(i for i in schemes):
        return True
    else:
        return False