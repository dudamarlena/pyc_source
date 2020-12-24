# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/code/pyutil/pyutil/version_class.py
# Compiled at: 2019-06-26 11:58:00
# Size of source mod 2**32: 5497 bytes
"""
extended version number class
"""
from pyutil.verlib import NormalizedVersion
import functools, re
VERSION_BASE_RE_STR = '(\\d+)(\\.(\\d+)(\\.(\\d+))?)?((a|b|c)(\\d+))?(\\.dev(\\d+))?'
VERSION_SUFFIX_RE_STR = '(-(\\d+|r\\d+)|.post\\d+)?'
VERSION_RE_STR = VERSION_BASE_RE_STR + VERSION_SUFFIX_RE_STR
VERSION_RE = re.compile('^' + VERSION_RE_STR + '$')

@functools.total_ordering
class Version(object):

    def __init__(self, vstring=None):
        self.major = None
        self.minor = None
        self.micro = None
        self.prereleasetag = None
        self.prerelease = None
        self.nano = None
        self.revision = None
        if vstring:
            try:
                self.parse(vstring)
            except ValueError as le:
                le.args = tuple(le.args + ('vstring:', vstring))
                raise

    def parse(self, vstring):
        mo = VERSION_RE.search(vstring)
        if not mo:
            raise ValueError('Not a valid version string for pyutil.version_class.Version(): %r' % (vstring,))
        self.major = int(mo.group(1))
        self.minor = mo.group(3) and int(mo.group(3)) or 0
        self.micro = mo.group(5) and int(mo.group(5)) or 0
        reltag = mo.group(6)
        if reltag:
            reltagnum = int(mo.group(8))
            self.prereleasetag = mo.group(7)
            self.prerelease = reltagnum
        if mo.group(11):
            if mo.group(11)[0] == '-':
                if mo.group(12)[0] == 'r':
                    self.revision = int(mo.group(12)[1:])
            else:
                self.nano = int(mo.group(12))
        else:
            assert mo.group(11).startswith('.post'), mo.group(11)
            self.revision = int(mo.group(11)[5:])
        self.fullstr = '%d.%d.%d%s%s' % (self.major, self.minor, self.micro, self.prereleasetag and '%s%d' % (self.prereleasetag, self.prerelease) or '', self.nano and '-%d' % (self.nano,) or self.revision and '-r%d' % (self.revision,) or '')

    def user_str(self):
        return self.full_str()

    def full_str(self):
        if hasattr(self, 'fullstr'):
            return self.fullstr
        else:
            return 'None'

    def __str__(self):
        return self.full_str()

    def __repr__(self):
        return self.__str__()

    def __cmp__(self, other):
        return cmp(NormalizedVersion(str(self)), NormalizedVersion(str(other)))

    def __eq__(self, other):
        return NormalizedVersion(str(self)) == NormalizedVersion(str(other))

    def __lt__(self, other):
        return NormalizedVersion(str(self)) < NormalizedVersion(str(other))