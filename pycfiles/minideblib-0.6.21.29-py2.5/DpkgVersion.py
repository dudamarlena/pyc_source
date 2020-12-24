# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/minideblib/DpkgVersion.py
# Compiled at: 2007-11-06 15:08:00
"""Parse and compare Debian version strings.

This module contains a class designed to sit in your Python code pretty
naturally and represent a Debian version string.  It implements various
special methods to make dealing with them sweet.
"""
__author__ = 'Scott James Remnant <scott@netsplit.com>'
import re
valid_epoch = re.compile('^[0-9]+$')
valid_upstream = re.compile('^[0-9][A-Za-z0-9+:.~-]*$')
valid_revision = re.compile('^[A-Za-z0-9+.~]+$')
cmp_table = '~ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+-.:'

class VersionError(Exception):
    pass


class BadInputError(VersionError):
    pass


class BadEpochError(BadInputError):
    pass


class BadUpstreamError(BadInputError):
    pass


class BadRevisionError(BadInputError):
    pass


class DpkgVersion(object):
    """
    Debian version number.

    This class is designed to be reasonably transparent and allow you to write code like:

    >>> s.version >= '1.100-1'

    The comparison will be done according to Debian rules, so '1.2' will compare lower.

    Properties:
     - epoch: Epoch
     - upstream: Upstream version
     - revision: Debian/local revision
    """

    def __init__(self, ver):
        """Parse a string or number into the three components."""
        self.epoch = None
        self.upstream = None
        self.revision = None
        ver = str(ver)
        if not len(ver):
            raise BadInputError, 'Input cannot be empty'
        idx = ver.find(':')
        if idx != -1:
            self.epoch = ver[:idx]
            if not len(self.epoch):
                raise BadEpochError, 'Epoch cannot be empty'
            if not valid_epoch.search(self.epoch):
                raise BadEpochError, 'Bad epoch format'
            ver = ver[idx + 1:]
        idx = ver.rfind('-')
        if idx != -1:
            self.revision = ver[idx + 1:]
            if not len(self.revision):
                raise BadRevisionError, 'Revision cannot be empty'
            if not valid_revision.search(self.revision):
                raise BadRevisionError, 'Bad revision format'
            ver = ver[:idx]
        self.upstream = ver
        if not len(self.upstream):
            raise BadUpstreamError, 'Upstream version cannot be empty'
        if not valid_upstream.search(self.upstream):
            raise BadUpstreamError, 'Bad upstream version format'
        if self.epoch is not None:
            self.epoch = int(self.epoch)
        return

    def getWithoutEpoch(self):
        """Return the version without the epoch."""
        str = self.upstream
        if self.revision is not None:
            str += '-%s' % (self.revision,)
        return str

    without_epoch = property(getWithoutEpoch)

    def __str__(self):
        """Return the class as a string for printing."""
        str = ''
        if self.epoch is not None:
            str += '%d:' % (self.epoch,)
        str += self.upstream
        if self.revision is not None:
            str += '-%s' % (self.revision,)
        return str

    def __repr__(self):
        """Return a debugging representation of the object."""
        return '<%s epoch: %r, upstream: %r, revision: %r>' % (
         self.__class__.__name__, self.epoch,
         self.upstream, self.revision)

    def __cmp__(self, other):
        """Compare two Version classes."""
        other = DpkgVersion(other)
        if self.epoch != other.epoch:
            sepoch = self.epoch
            oepoch = other.epoch
            if sepoch is None:
                sepoch = 0
            if oepoch is None:
                oepoch = 0
            result = cmp(sepoch, oepoch)
            if result != 0:
                return result
        result = deb_cmp(self.upstream, other.upstream)
        if result != 0:
            return result
        result = deb_cmp(self.revision or '', other.revision or '')
        if result != 0:
            return result
        return 0

    def is_native(self):
        native = False
        if not self.revision:
            native = True
        return native


def strcut(str, idx, accept):
    """Cut characters from str that are entirely in accept."""
    ret = ''
    while idx < len(str) and str[idx] in accept:
        ret += str[idx]
        idx += 1

    return (ret, idx)


def deb_order(str, idx):
    """Return the comparison order of two characters."""
    if idx >= len(str):
        return 0
    elif str[idx] == '~':
        return -1
    else:
        return cmp_table.index(str[idx])


def deb_cmp_str(x, y):
    """Compare two strings in a deb version."""
    idx = 0
    while idx < len(x) or idx < len(y):
        result = deb_order(x, idx) - deb_order(y, idx)
        if result < 0:
            return -1
        elif result > 0:
            return 1
        idx += 1

    return 0


def deb_cmp(x, y):
    """Implement the string comparison outlined by Debian policy."""
    x_idx = y_idx = 0
    while x_idx < len(x) or y_idx < len(y):
        (x_str, x_idx) = strcut(x, x_idx, cmp_table)
        (y_str, y_idx) = strcut(y, y_idx, cmp_table)
        result = deb_cmp_str(x_str, y_str)
        if result != 0:
            return result
        (x_str, x_idx) = strcut(x, x_idx, '0123456789')
        (y_str, y_idx) = strcut(y, y_idx, '0123456789')
        result = cmp(int(x_str or '0'), int(y_str or '0'))
        if result != 0:
            return result

    return 0