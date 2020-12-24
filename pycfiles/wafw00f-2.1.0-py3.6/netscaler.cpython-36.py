# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wafw00f/plugins/netscaler.py
# Compiled at: 2020-02-20 22:34:09
# Size of source mod 2**32: 957 bytes
"""
Copyright (C) 2020, WAFW00F Developers.
See the LICENSE file for copying permission.
"""
NAME = 'NetScaler AppFirewall (Citrix Systems)'

def is_waf(self):
    schemes = [
     self.matchHeader(('Via', 'NS\\-CACHE')),
     self.matchCookie('^(ns_af=|citrix_ns_id|NSC_)'),
     self.matchContent('(NS Transaction|AppFW Session) id'),
     self.matchContent('Violation Category.{0,5}?APPFW_'),
     self.matchContent('Citrix\\|NetScaler'),
     self.matchHeader(('Cneonction', '^(keep alive|close)'), attack=True),
     self.matchHeader(('nnCoection', '^(keep alive|close)'), attack=True)]
    if any(i for i in schemes):
        return True
    else:
        return False