# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wafw00f/plugins/greywizard.py
# Compiled at: 2020-02-20 22:34:09
# Size of source mod 2**32: 550 bytes
"""
Copyright (C) 2020, WAFW00F Developers.
See the LICENSE file for copying permission.
"""
NAME = 'Greywizard (Grey Wizard)'

def is_waf(self):
    schemes = [
     self.matchHeader(('Server', 'greywizard')),
     self.matchContent('<(title|h\\d{1})>Grey Wizard'),
     self.matchContent('contact the website owner or Grey Wizard'),
     self.matchContent('We.ve detected attempted attack or non standard traffic from your ip address')]
    if any(i for i in schemes):
        return True
    else:
        return False