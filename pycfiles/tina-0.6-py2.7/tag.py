# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tina/tag.py
# Compiled at: 2013-04-10 10:01:21
import re, sys

class Tag:

    def __init__(self, version_str):
        match = re.match('(\\D*)(\\d+)\\.(\\d+)\\.(\\d+)', version_str)
        if not match:
            raise Exception('Error: malformed tag: ' + version_str)
        self.pretext = match.group(1)
        self.major = int(match.group(2))
        self.minor = int(match.group(3))
        self.build = int(match.group(4))

    def __lt__(self, other):
        if self.major != other.major:
            return self.major < other.major
        else:
            if self.minor != other.minor:
                return self.minor < other.minor
            return self.build < other.build

    def __gt__(self, other):
        if self.major != other.major:
            return self.major > other.major
        else:
            if self.minor != other.minor:
                return self.minor > other.minor
            return self.build > other.build

    def __eq__(self, other):
        return self.major == other.major and self.minor == other.minor and self.build == other.build

    def __ne__(self, other):
        return not self == other

    def __le__(self, other):
        return self < other or self == other

    def __ge__(self, other):
        return self > other or self == other

    def __repr__(self):
        return '%s%d.%d.%d' % (self.pretext, self.major, self.minor,
         self.build)

    def version_str(self):
        return '%d.%d.%d' % (self.major, self.minor, self.build)

    def build_bump(self):
        self.build = self.build + 1

    def minor_bump(self):
        self.minor = self.minor + 1
        self.build = 0

    def major_bump(self):
        self.major = self.major + 1
        self.minor = 0
        self.build = 0

    def increment(self):
        self.build_bump()

    def decrement(self):
        self.build = self.build - 1
        if self.build < 0:
            self.build = sys.maxint
            self.minor = self.minor - 1
            if self.minor < 0:
                self.minor = sys.maxint
                self.major = self.major - 1

    @staticmethod
    def max_tag():
        t = Tag('0.0.0')
        t.major = sys.maxint
        t.minor = sys.maxint
        t.build = sys.maxint
        return t

    @staticmethod
    def min_tag():
        return Tag('0.0.0')