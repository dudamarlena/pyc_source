# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/code/pyutil/pyutil/verlib.py
# Compiled at: 2019-06-26 11:58:00
"""
"Rational" version definition and parsing for DistutilsVersionFight
discussion at PyCon 2009.
"""
import re
try:
    unicode = unicode
except NameError:
    basestring = (
     str, bytes)

class IrrationalVersionError(Exception):
    """This is an irrational version."""
    pass


class HugeMajorVersionNumError(IrrationalVersionError):
    """An irrational version because the major version number is huge
    (often because a year or date was used).

    See `error_on_huge_major_num` option in `NormalizedVersion` for details.
    This guard can be disabled by setting that option False.
    """
    pass


class PreconditionViolationException(Exception):
    pass


FINAL_MARKER = ('f', )
VERSION_RE = re.compile("\n    ^\n    (?P<version>\\d+\\.\\d+)          # minimum 'N.N'\n    (?P<extraversion>(?:\\.\\d+)*)   # any number of extra '.N' segments\n    (?:\n        (?P<prerel>[abc]|rc)       # 'a'=alpha, 'b'=beta, 'c'=release candidate\n                                   # 'rc'= alias for release candidate\n        (?P<prerelversion>\\d+(?:\\.\\d+)*)\n    )?\n    (?P<postdev>(\\.post(?P<post>\\d+)|-r(?P<oldpost>\\d+))?(\\.dev(?P<dev>\\d+))?)?\n    $", re.VERBOSE)

class NormalizedVersion(object):
    """A rational version.

    Good:
        1.2         # equivalent to "1.2.0"
        1.2.0
        1.2a1
        1.2.3a2
        1.2.3b1
        1.2.3c1
        1.2.3.4
        TODO: fill this out

    Bad:
        1           # mininum two numbers
        1.2a        # release level must have a release serial
        1.2.3b
    """

    def __init__(self, s, error_on_huge_major_num=True):
        """Create a NormalizedVersion instance from a version string.

        @param s {str} The version string.
        @param error_on_huge_major_num {bool} Whether to consider an
            apparent use of a year or full date as the major version number
            an error. Default True. One of the observed patterns on PyPI before
            the introduction of `NormalizedVersion` was version numbers like this:
                2009.01.03
                20040603
                2005.01
            This guard is here to strongly encourage the package author to
            use an alternate version, because a release deployed into PyPI
            and, e.g. downstream Linux package managers, will forever remove
            the possibility of using a version number like "1.0" (i.e.
            where the major number is less than that huge major number).
        """
        self._parse(s, error_on_huge_major_num)

    @classmethod
    def from_parts(cls, version, prerelease=FINAL_MARKER, devpost=FINAL_MARKER):
        return cls(cls.parts_to_str((version, prerelease, devpost)))

    def _parse(self, s, error_on_huge_major_num=True):
        """Parses a string version into parts."""
        if not isinstance(s, basestring):
            raise PreconditionViolationException('s is required to be a string: %s :: %s' % (s, type(s)))
        match = VERSION_RE.search(s)
        if not match:
            raise IrrationalVersionError(s)
        groups = match.groupdict()
        parts = []
        block = self._parse_numdots(groups['version'], s, False, 2)
        extraversion = groups.get('extraversion')
        if extraversion not in ('', None):
            block += self._parse_numdots(extraversion[1:], s)
        parts.append(tuple(block))
        prerel = groups.get('prerel')
        if prerel is not None:
            block = [
             prerel]
            block += self._parse_numdots(groups.get('prerelversion'), s, pad_zeros_length=1)
            parts.append(tuple(block))
        else:
            parts.append(FINAL_MARKER)
        if groups.get('postdev'):
            post = groups.get('post') or groups.get('oldpost')
            dev = groups.get('dev')
            postdev = []
            if post is not None:
                postdev.extend([FINAL_MARKER[0], 'post', int(post)])
                if dev is None:
                    postdev.append(FINAL_MARKER[0])
            if dev is not None:
                postdev.extend(['dev', int(dev)])
            parts.append(tuple(postdev))
        else:
            parts.append(FINAL_MARKER)
        self.parts = tuple(parts)
        if error_on_huge_major_num and self.parts[0][0] > 1980:
            raise HugeMajorVersionNumError('huge major version number, %r, which might cause future problems: %r' % (
             self.parts[0][0], s))
        return

    def _parse_numdots(self, s, full_ver_str, drop_trailing_zeros=True, pad_zeros_length=0):
        """Parse 'N.N.N' sequences, return a list of ints.

        @param s {str} 'N.N.N...' sequence to be parsed
        @param full_ver_str {str} The full version string from which this
            comes. Used for error strings.
        @param drop_trailing_zeros {bool} Whether to drop trailing zeros
            from the returned list. Default True.
        @param pad_zeros_length {int} The length to which to pad the
            returned list with zeros, if necessary. Default 0.
        """
        nums = []
        for n in s.split('.'):
            if len(n) > 1 and n[0] == '0':
                raise IrrationalVersionError("cannot have leading zero in version number segment: '%s' in %r" % (
                 n, full_ver_str))
            nums.append(int(n))

        if drop_trailing_zeros:
            while nums and nums[(-1)] == 0:
                nums.pop()

        while len(nums) < pad_zeros_length:
            nums.append(0)

        return nums

    def __str__(self):
        return self.parts_to_str(self.parts)

    @classmethod
    def parts_to_str(cls, parts):
        """Transforms a version expressed in tuple into its string
        representation."""
        main, prerel, postdev = parts
        s = ('.').join(str(v) for v in main)
        if prerel is not FINAL_MARKER:
            s += prerel[0]
            s += ('.').join(str(v) for v in prerel[1:])
        if postdev and postdev is not FINAL_MARKER:
            if postdev[0] == 'f':
                postdev = postdev[1:]
            i = 0
            while i < len(postdev):
                if i % 2 == 0:
                    s += '.'
                s += str(postdev[i])
                i += 1

        return s

    def __repr__(self):
        return "%s('%s')" % (self.__class__.__name__, self)

    def _cannot_compare(self, other):
        raise TypeError('cannot compare %s and %s' % (
         type(self).__name__, type(other).__name__))

    def __eq__(self, other):
        if not isinstance(other, NormalizedVersion):
            self._cannot_compare(other)
        return self.parts == other.parts

    def __lt__(self, other):
        if not isinstance(other, NormalizedVersion):
            self._cannot_compare(other)
        return self.parts < other.parts

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return not (self.__lt__(other) or self.__eq__(other))

    def __le__(self, other):
        return self.__eq__(other) or self.__lt__(other)

    def __ge__(self, other):
        return self.__eq__(other) or self.__gt__(other)


def suggest_normalized_version(s):
    """Suggest a normalized version close to the given version string.

    If you have a version string that isn't rational (i.e. NormalizedVersion
    doesn't like it) then you might be able to get an equivalent (or close)
    rational version from this function.

    This does a number of simple normalizations to the given string, based
    on observation of versions currently in use on PyPI. Given a dump of
    those version during PyCon 2009, 4287 of them:
    - 2312 (53.93%) match NormalizedVersion without change
    - with the automatic suggestion
    - 3474 (81.04%) match when using this suggestion method

    @param s {str} An irrational version string.
    @returns A rational version string, or None, if couldn't determine one.
    """
    try:
        NormalizedVersion(s)
        return s
    except IrrationalVersionError:
        pass

    rs = s.lower()
    for orig, repl in (('-alpha', 'a'), ('-beta', 'b'), ('alpha', 'a'),
     ('beta', 'b'), ('rc', 'c'), ('-final', ''),
     ('-pre', 'c'),
     ('-release', ''), ('.release', ''), ('-stable', ''),
     ('+', '.'), ('_', '.'), (' ', ''), ('.final', ''),
     ('final', '')):
        rs = rs.replace(orig, repl)

    rs = re.sub('pre$', 'pre0', rs)
    rs = re.sub('dev$', 'dev0', rs)
    rs = re.sub('([abc|rc])[\\-\\.](\\d+)$', '\\1\\2', rs)
    rs = re.sub('[\\-\\.](dev)[\\-\\.]?r?(\\d+)$', '.\\1\\2', rs)
    rs = re.sub('[.~]?([abc])\\.?', '\\1', rs)
    if rs.startswith('v'):
        rs = rs[1:]
    rs = re.sub('\\b0+(\\d+)(?!\\d)', '\\1', rs)
    rs = re.sub('(\\d+[abc])$', '\\g<1>0', rs)
    rs = re.sub('\\.?(dev-r|dev\\.r)\\.?(\\d+)$', '.dev\\2', rs)
    rs = re.sub('-(a|b|c)(\\d+)$', '\\1\\2', rs)
    rs = re.sub('[\\.\\-](dev|devel)$', '.dev0', rs)
    rs = re.sub('(?![\\.\\-])dev$', '.dev0', rs)
    rs = re.sub('(final|stable)$', '', rs)
    rs = re.sub('\\.?(r|-|-r)\\.?(\\d+)$', '.post\\2', rs)
    rs = re.sub('\\.?(dev|git|bzr)\\.?(\\d+)$', '.dev\\2', rs)
    rs = re.sub('\\.?(pre|preview|-c)(\\d+)$', 'c\\g<2>', rs)
    rs = re.sub('p(\\d+)$', '.post\\1', rs)
    try:
        NormalizedVersion(rs)
        return rs
    except IrrationalVersionError:
        pass

    return