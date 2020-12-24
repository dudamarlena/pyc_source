# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/zensols/pybuild/version.py
# Compiled at: 2018-09-14 14:26:08
# Size of source mod 2**32: 1807 bytes
import re

class Version(object):

    def __init__(self, major=0, minor=0, debug=1):
        self.major = major
        self.minor = minor
        self.debug = debug

    @classmethod
    def from_string(clz, s):
        m = re.search('^v?(\\d+)\\.(\\d+)\\.(\\d+)$', s)
        if m is not None:
            return Version(int(m.group(1)), int(m.group(2)), int(m.group(3)))

    def format(self, prefix='v'):
        return prefix + ('{major}.{minor}.{debug}'.format)(**self.__dict__)

    def increment(self, decimal='debug', inc=1):
        if decimal == 'major':
            self.major += inc
        else:
            if decimal == 'minor':
                self.minor += inc
            else:
                if decimal == 'debug':
                    self.debug += inc
                else:
                    raise ValueError('uknown decimal type: {}'.format(decimal))

    def __lt__(self, o):
        if self.major < o.major:
            return True
        else:
            if self.major > o.major:
                return False
            else:
                if self.minor < o.minor:
                    return True
                else:
                    if self.minor > o.minor:
                        return False
                    if self.debug < o.debug:
                        return True
                if self.debug > o.debug:
                    return False
            return False

    def __le__(self, o):
        if self.major <= o.major:
            return True
        else:
            if self.major >= o.major:
                return False
            else:
                if self.minor <= o.minor:
                    return True
                else:
                    if self.minor >= o.minor:
                        return False
                    if self.debug <= o.debug:
                        return True
                if self.debug >= o.debug:
                    return False
            return False

    def __eq__(self, o):
        return self.__dict__ == o.__dict__

    def __str__(self):
        return self.format()

    def __repr__(self):
        return self.__str__()