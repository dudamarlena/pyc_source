# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trac_captcha/lib/version.py
# Compiled at: 2011-02-04 14:10:44
__all__ = [
 'Version']

class Version(object):

    def __init__(self, major=0, minor=0, patch_level=0):
        self.major = major
        self.minor = minor
        self.patch_level = patch_level

    def __repr__(self):
        repr_values = tuple(map(repr, (self.major, self.minor, self.patch_level)))
        return 'Version(major=%s, minor=%s, patch_level=%s)' % repr_values

    def __eq__(self, other):
        if not isinstance(other, Version):
            return False
        return self.major == other.major and self.minor == other.minor and self.patch_level == other.patch_level

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        if self.major != other.major:
            return self.major < other.major
        if self.minor != other.minor:
            return self.minor < other.minor
        return self.patch_level < other.patch_level

    def __le__(self, other):
        return self == other or self < other

    def __ge__(self, other):
        return self == other or self > other