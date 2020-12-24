# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/doubanfm/dal/dal_lrc.py
# Compiled at: 2016-06-22 17:23:26
from doubanfm.dal.dal_main import MainDal

class LrcDal(MainDal):

    def __init__(self, data, offset):
        super(LrcDal, self).__init__(data)
        self.lrc = data.lrc
        self.lrc_offset = offset

    @property
    def lines(self):
        return [ line[1] for line in self.sort_lrc_dict if line[1] ]

    @property
    def sort_lrc_dict(self):
        return sorted(self.lrc.iteritems(), key=lambda x: x[0])

    @property
    def title(self):
        if self.lrc_offset != 0:
            title_offset = '+' if self.lrc_offset > 0 else ''
            title_offset += str(self.lrc_offset) + 's'
        else:
            title_offset = ''
        return super(LrcDal, self).title + ' ' + title_offset