# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wafw00f/plugins/sophos.py
# Compiled at: 2020-02-20 22:34:09
# Size of source mod 2**32: 810 bytes
"""
Copyright (C) 2020, WAFW00F Developers.
See the LICENSE file for copying permission.
"""
NAME = 'UTM Web Protection (Sophos)'

def is_waf(self):
    schema1 = [
     self.matchContent('www\\.sophos\\.com'),
     self.matchContent('Powered by.?(Sophos)? UTM Web Protection')]
    schema2 = [
     self.matchContent('<title>Access to the requested URL was blocked'),
     self.matchContent('Access to the requested URL was blocked'),
     self.matchContent('incident was logged with the following log identifier'),
     self.matchContent('Inbound Anomaly Score exceeded'),
     self.matchContent('Your cache administrator is')]
    if any(i for i in schema1):
        return True
    else:
        if all(i for i in schema2):
            return True
        return False