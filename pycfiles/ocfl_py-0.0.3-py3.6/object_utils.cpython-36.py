# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ocfl/object_utils.py
# Compiled at: 2020-03-27 17:33:06
# Size of source mod 2**32: 3291 bytes
"""Utility functions to support the OCFL Object library."""
import copy, hashlib, os, os.path, re, logging, sys
try:
    from urllib.parse import quote as urlquote
except ImportError:
    from urllib import quote as urlquote

NORMALIZATIONS = [
 'uri', 'md5']

def add_object_args(parser):
    """Add Object settings to argparse or argument group instance parser."""
    parser.add_argument('--skip', action='append', default=['README.md', '.DS_Store'], help='directories and files to ignore')
    parser.add_argument('--normalization', '--norm', default=None, help=('filepath normalization strategy (None, %s)' % ', '.join(NORMALIZATIONS)))
    parser.add_argument('--no-forward-delta', action='store_true', help='do not use forward deltas')
    parser.add_argument('--no-dedupe', '--no-dedup', action='store_true', help='do not use deduplicate files within a version')
    parser.add_argument('--lax-digests', action='store_true', help='allow use of any known digest')
    parser.add_argument('--objdir', '--obj', help='read from or write to OCFL object directory objdir')
    parser.add_argument('--ocfl-version', default='draft', help='OCFL specification version')


def next_version(version):
    """Next version identifier following existing pattern.

    Must deal with both zero-prefixed and non-zero prefixed versions.
    """
    m = re.match('v((\\d)\\d*)$', version)
    if not m:
        raise ObjectException("Bad version '%s'" % version)
    next = int(m.group(1)) + 1
    if m.group(2) == '0':
        next_version = ('v0%0' + str(len(version) - 2) + 'd') % next
        if len(next_version) != len(version):
            raise ObjectException('Version number overflow for zero-padded version %d to %d' % (version, next_version))
        return next_version
    else:
        return 'v' + str(next)


def remove_first_directory(path):
    """Remove first directory from input path.

    The return value will not have a trailing parh separator, even if
    the input path does. Will return an empty string if the input path
    has just one path segment.
    """
    rpath = ''
    while True:
        head, tail = os.path.split(path)
        if head == path or tail == path:
            break
        else:
            path = head
            rpath = tail if rpath == '' else os.path.join(tail, rpath)

    return rpath


def make_unused_filepath(filepath, used, separator='__'):
    """Find filepath with string appended that makes it disjoint from those in used."""
    n = 1
    while 1:
        n += 1
        f = filepath + separator + str(n)
        if f not in used:
            return f