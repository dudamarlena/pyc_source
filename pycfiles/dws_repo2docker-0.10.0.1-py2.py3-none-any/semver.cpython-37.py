# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jfischer/code/repo2docker/repo2docker/buildpacks/julia/semver.py
# Compiled at: 2019-09-18 03:20:22
# Size of source mod 2**32: 5039 bytes
"""
Julia specific handling of SemVer strings

It uses the python "semver" package to do most version string comparisons, but
the places where julia's SemVer handling differs from the semver package have
been implemented directly.

We use tuples to represent a Version, and functors as "matchers". The
matcher functors take a version string and return True if it passes its
constraints.
"""
import re, semver

def find_semver_match(constraint, versions_list):
    matcher = create_semver_matcher(constraint)
    for vstr in reversed(versions_list):
        if matcher.match(str_to_version(vstr)):
            return vstr


def str_to_version(vstr):
    return tuple([int(n) for n in vstr.split('.')])


def major(v):
    return v[0]


def minor(v):
    if len(v) >= 2:
        return v[1]
    return 0


def patch(v):
    if len(v) >= 3:
        return v[2]
    return 0


def create_semver_matcher(constraint_str):
    """Create a matcher that can be used to match version tuples

    Version tuples are matched against the provided regex `constraint_str`.
    """
    constraint_str = constraint_str.strip()
    first_digit = re.search('\\d', constraint_str)
    if not first_digit:
        return ''
    constraint = str_to_version(constraint_str[first_digit.start():])
    comparison_symbol = constraint_str[0:first_digit.start()].strip()
    if first_digit.start() == 0 or comparison_symbol == '^':
        if major(constraint) == 0:
            for i, n in enumerate(constraint):
                if n != 0 or i == len(constraint) - 1:
                    upper = constraint[0:i] + (n + 1,)
                    break

            return VersionRange(constraint, upper, True)
        return VersionRange(constraint, (major(constraint) + 1,), True)
    if comparison_symbol == '~':
        return VersionRange(constraint,
          (constraint[:-1] + (constraint[(-1)] + 1,)), exclusive=False)
    if len(constraint) < 3:
        while len(constraint) < 3:
            constraint = constraint + (0, )

        constraint_str = constraint_str[0:first_digit.start()] + '.'.join(map(str, constraint))
    constraint_str = constraint_str.replace('≥', '>=').replace('≤', '<=')
    constraint_str = re.sub('(^|\\b)=\\b', '==', constraint_str)
    return SemverMatcher(constraint_str)


class SemverMatcher:
    __doc__ = 'Provides a utility for using `semver` package to do version matching.\n\n    The `SemverMatcher` takes a `constraint_str` to represent a regex to\n    determine if a version tuple matches the constraint.\n\n    The matching is handled via the `semver` package.\n    '

    def __init__(self, constraint_str):
        self.constraint_str = constraint_str

    def match(self, v):
        """Check if `v` matches the constraint"""
        while len(v) < 3:
            v = v + (0, )

        v_str = '.'.join(map(str, v))
        return semver.match(v_str, self.constraint_str)

    def __eq__(self, rhs):
        return self.constraint_str == rhs.constraint_str

    def __repr__(self):
        return self.constraint_str


class VersionRange:
    __doc__ = 'Represents a range of release versions.\n\n    A `VersionRange` contains versions from a `lower` to `upper` bound\n    which may be inclusive (default: `exclusive=False`) or exclusive (`exclusive=True`).\n\n    A release version (represented by a tuple) can be checked to see if it\n    falls within a `VersionRange`\n    '

    def __init__(self, lower, upper, exclusive=False):
        self.lower = lower
        self.upper = upper
        self.exclusive = exclusive

    def match(self, v):
        """Check if `v` falls into the version range"""
        if self.exclusive:
            return self.lower <= v < self.upper
        return self.lower <= v <= self.upper

    def __eq__(self, rhs):
        return self.lower == rhs.lower and self.upper == rhs.upper and self.exclusive == rhs.exclusive

    def __repr__(self):
        return '[' + '.'.join(map(str, self.lower)) + '-' + '.'.join(map(str, self.upper)) + (')' if self.exclusive else ']')