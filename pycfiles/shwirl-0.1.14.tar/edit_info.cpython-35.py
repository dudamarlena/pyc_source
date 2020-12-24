# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/code/shwirl/extern/vispy/ext/_bundled/cassowary/edit_info.py
# Compiled at: 2017-04-05 22:12:59
# Size of source mod 2**32: 622 bytes
from __future__ import print_function, unicode_literals, absolute_import, division

class EditInfo(object):

    def __init__(self, constraint, edit_plus, edit_minus, prev_edit_constant, index):
        self.constraint = constraint
        self.edit_plus = edit_plus
        self.edit_minus = edit_minus
        self.prev_edit_constant = prev_edit_constant
        self.index = index

    def __repr__(self):
        return '<cn=%s ep=%s em=%s pec=%s index=%s>' % (
         self.constraint,
         self.edit_plus,
         self.edit_minus,
         self.prev_edit_constant,
         self.index)