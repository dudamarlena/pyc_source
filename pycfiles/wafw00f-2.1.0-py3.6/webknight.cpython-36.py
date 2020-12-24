# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wafw00f/plugins/webknight.py
# Compiled at: 2020-02-20 22:34:09
# Size of source mod 2**32: 932 bytes
"""
Copyright (C) 2020, WAFW00F Developers.
See the LICENSE file for copying permission.
"""
NAME = 'WebKnight (AQTRONIX)'

def is_waf(self):
    schema1 = [
     self.matchStatus(999),
     self.matchReason('No Hacking')]
    schema2 = [
     self.matchStatus(404),
     self.matchReason('Hack Not Found')]
    schema3 = [
     self.matchContent('WebKnight Application Firewall Alert'),
     self.matchContent('What is webknight\\?'),
     self.matchContent('AQTRONIX WebKnight is an application firewall'),
     self.matchContent('WebKnight will take over and protect'),
     self.matchContent('aqtronix\\.com/WebKnight'),
     self.matchContent('AQTRONIX.{0,10}?WebKnight')]
    if all(i for i in schema1):
        return True
    if all(i for i in schema2):
        return True
    else:
        if any(i for i in schema3):
            return True
        return False