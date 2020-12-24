# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wafw00f/plugins/uewaf.py
# Compiled at: 2020-02-20 22:34:09
# Size of source mod 2**32: 413 bytes
"""
Copyright (C) 2020, WAFW00F Developers.
See the LICENSE file for copying permission.
"""
NAME = 'UEWaf (UCloud)'

def is_waf(self):
    schemes = [
     self.matchHeader(('Server', 'uewaf(/[0-9\\.]+)?')),
     self.matchContent('/uewaf_deny_pages/default/img/'),
     self.matchContent('ucloud\\.cn')]
    if any(i for i in schemes):
        return True
    else:
        return False