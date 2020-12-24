# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/picalo/lib/pyExcelerator/Column.py
# Compiled at: 2008-03-17 12:58:00
__rev_id__ = '$Id: Column.py,v 1.4 2005/07/20 07:24:11 rvk Exp $'
from BIFFRecords import ColInfoRecord
from Deco import *
from Worksheet import Worksheet

class Column(object):

    @accepts(object, int, Worksheet)
    def __init__(self, indx, parent_sheet):
        self._index = indx
        self._parent = parent_sheet
        self._parent_wb = parent_sheet.get_parent()
        self._xf_index = 15
        self.width = 2962
        self.hidden = 0
        self.level = 0
        self.collapse = 0

    def get_biff_record(self):
        options = (self.hidden & 1) << 0
        options |= (self.level & 7) << 8
        options |= (self.collapse & 1) << 12
        return ColInfoRecord(self._index, self._index, self.width, self._xf_index, options).get()