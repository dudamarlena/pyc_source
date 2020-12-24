# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/sflib/finddata.py
# Compiled at: 2009-10-21 10:42:48
import os, sys
from fnmatch import fnmatchcase
from distutils.util import convert_path
standard_exclude = ('*.py', '*.pyc', '*$py.class', '*~', '.*', '*.bak')
standard_exclude_directories = ('.*', 'CVS', '_darcs', './build', './dist', 'EGG-INFO',
                                '*.egg-info')

def find_package_data(where='.', package='', exclude=standard_exclude, exclude_directories=standard_exclude_directories, only_in_packages=True, show_ignored=False):
    """
    Return a dictionary suitable for use in ``package_data``
    in a distutils ``setup.py`` file.

    The dictionary looks like::

        {'package': [files]}

    Where ``files`` is a list of all the files in that package that
    don't match anything in ``exclude``.

    If ``only_in_packages`` is true, then top-level directories that
    are not packages won't be included (but directories under packages
    will).

    Directories matching any pattern in ``exclude_directories`` will
    be ignored; by default directories with leading ``.``, ``CVS``,
    and ``_darcs`` will be ignored.

    If ``show_ignored`` is true, then all the files that aren't
    included in package data are shown on stderr (for debugging
    purposes).

    Note patterns use wildcards, or can be exact paths (including
    leading ``./``), and all searching is case-insensitive.
    """
    out = {}
    stack = [
     (
      convert_path(where), '', package, only_in_packages)]
    while stack:
        (where, prefix, package, only_in_packages) = stack.pop(0)
        for name in os.listdir(where):
            fn = os.path.join(where, name)
            if os.path.isdir(fn):
                bad_name = False
                for pattern in exclude_directories:
                    if fnmatchcase(name, pattern) or fn.lower() == pattern.lower():
                        bad_name = True
                        if show_ignored:
                            print >> sys.stderr, 'Directory %s ignored by pattern %s' % (fn, pattern)
                        break

                if bad_name:
                    continue
                if os.path.isfile(os.path.join(fn, '__init__.py')):
                    if not prefix:
                        new_package = package or name
                    else:
                        new_package = package + '.' + name
                    stack.append((fn, '', new_package, False))
                else:
                    stack.append((fn, prefix + name + '/', package, only_in_packages))
            elif package or not only_in_packages:
                bad_name = False
                for pattern in exclude:
                    if fnmatchcase(name, pattern) or fn.lower() == pattern.lower():
                        bad_name = True
                        if show_ignored:
                            print >> sys.stderr, 'File %s ignored by pattern %s' % (fn, pattern)
                        break

                if bad_name:
                    continue
                out.setdefault(package, []).append(prefix + name)

    return out


if __name__ == '__main__':
    import pprint
    pprint.pprint(find_package_data(show_ignored=True))