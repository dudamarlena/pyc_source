# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\mcs\versioninfo.py
# Compiled at: 2011-11-21 18:59:07
__all__ = 'VersionInfo'
import collections, datetime, re

class VersionInfo(object):
    __slots__ = ('data', )
    sexpr_labels = re.compile('\\w+(?!\\w)')
    sexpr_strings = re.compile("'((?:[^']+|'')*)'")
    date_fmt = re.compile('(\\d{1,2}) (\\w+) (\\d{4})$')
    time_fmt = re.compile('(\\d{1,2}):(\\d{2})(?::(\\d{2})(?:(.\\d+))?)? ?([a|p]m)?$')
    months = ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
              'September', 'October', 'November', 'December')

    @classmethod
    def parse(cls, contents):
        pos = 0
        current = []
        stack = collections.deque()
        while pos < len(contents):
            c = contents[pos]
            if c.isspace():
                pos += 1
                continue
            if contents[pos] == '(':
                pos += 1
                stack.append(current)
                current = []
                continue
            if contents[pos] == ')':
                pos += 1
                old, current = current, stack.pop()
                current.append(tuple(old))
                continue
            if contents[pos].isalpha():
                m = cls.sexpr_labels.match(contents[pos:])
                current.append(m.group(0))
                pos += m.end(0)
                continue
            if contents[pos] == "'":
                m = cls.sexpr_strings.match(contents[pos:])
                current.append(m.group(1).replace("''", "'"))
                pos += m.end(0)
                continue

        return VersionInfo(current[0])

    def __init__(self, data):
        self.data = dict(zip(data[0::2], data[1::2]))

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.name)

    def __getattr__(self, key):
        if key in self.data:
            return self.data[key]
        return getattr(super(VersionInfo, self), key)

    def ancestors(self):
        return [ VersionInfo(p) for p in self.data['ancestors'] ]

    def timestamp(self):
        day, month, year = self.date_fmt.match(self.date).groups()
        hour, minute, second, fraction, ampm = self.time_fmt.match(self.time).groups()
        return datetime.datetime(int(year), self.months.index(month) + 1, int(day), (int(hour) + (12 if ampm == 'pm' else 0)) % 24, int(minute), int(second or 0), int(float(fraction or 0.0) * 1000000.0))