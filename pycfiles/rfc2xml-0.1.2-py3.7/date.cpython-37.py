# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/rfc2xml/elements/date.py
# Compiled at: 2019-09-08 12:19:27
# Size of source mod 2**32: 1073 bytes
from . import Element

class Date(Element):
    tag_name = 'date'
    tag_name: str
    year = None
    year: int
    month = None
    month: str
    day = None
    day: int

    def get_attributes(self):
        attributes = {}
        if self.year is not None:
            attributes['year'] = self.year
        if self.month is not None:
            attributes['month'] = self.month
        if self.day is not None:
            attributes['day'] = self.day
        return attributes

    def __init__(self, year=None, month=None, day=None):
        super().__init__()
        self.year = year
        self.month = month
        self.day = day

    def __str__(self):
        if None not in (self.year, self.month, self.day):
            return str(self.month) + ' ' + str(self.day) + ', ' + str(self.year)
        output = ''
        if self.month is not None:
            output += str(self.month) + ' '
        if self.day is not None:
            output += str(self.day) + ' '
        if self.year is not None:
            output += str(self.year) + ' '
        return output.strip()