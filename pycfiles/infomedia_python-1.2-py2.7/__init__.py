# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/exedre/Dropbox/exedre@gmail.com/Dropbox/Work/GeCo-dev/infomedia-1.0/build/lib/infomedia/__init__.py
# Compiled at: 2012-07-20 16:36:33


def find_version(source_file, num_levels=3):
    """
    Given the path to a Python source file, read in a version number
    from a file VERSION in the same directory, or look for a setup.py
    file in up to num_levels directories above the file and attempt to
    find the version there.
    """
    import os.path
    source_dir = os.path.dirname(source_file)
    version_file = os.path.join(source_dir, 'VERSION')
    if os.path.exists(version_file):
        version = open(version_file).read().strip()
        return version
    import re
    setup_version_re = re.compile('\n            set_version\\s*\\(\\s*[\'"]([^\'"]+)[\'"]\\s*\\)\n        ', re.VERBOSE)
    for i in xrange(num_levels):
        setup_path = [
         source_dir] + ['..'] * (i + 1) + ['setup.py']
        setup_file = os.path.join(*setup_path)
        if os.path.exists(setup_file):
            for l in open(setup_file, 'r'):
                m = setup_version_re.search(l)
                if m:
                    version = m.group(1)
                    return version

    return 'UNKNOWN'


__version__ = find_version(__file__)
DEBUG = False
import sys

def DEBUG_print(*args):
    if DEBUG:
        print >> sys.stderr, (' ').join(str(x) for x in args)


__all__ = ('\n').split()