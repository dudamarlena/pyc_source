# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/pdbparser/setup.py
# Compiled at: 2020-01-07 15:39:15
# Size of source mod 2**32: 8859 bytes
"""
In order to work properly, this script must be put one layer/folder/directory
outside of pdbparser package directory.
"""
try:
    from setuptools import setup
except:
    from distutils.core import setup

import fnmatch
from distutils.util import convert_path
import os, sys, glob
PACKAGE_PATH = '.'
PACKAGE_NAME = 'pdbparser'
major, minor = sys.version_info[:2]
if major == 2:
    if minor != 7:
        raise RuntimeError('Python version 2.7.x or >=3.x is required.')
commands = [
 '# include this file, to ensure we can recreate source distributions',
 'include MANIFEST.in\n# exclude all logs',
 'global-exclude *.log',
 '\n# exclude all pdbparserParams files',
 'global-exclude *pdbparserParams.*',
 '\n# exclude all other non necessary files ',
 'global-exclude .project',
 'global-exclude .pydevproject',
 '\n# exclude all of the subversion metadata',
 'global-exclude *.svn*',
 'global-exclude .svn/*',
 'global-exclude *.git*',
 'global-exclude .git/*',
 '\n# include all license files found',
 'global-include %s/*LICENSE.*' % PACKAGE_NAME,
 '\n# include all readme files found',
 'global-include %s/*README.*' % PACKAGE_NAME,
 'global-include %s/*readme.*' % PACKAGE_NAME]
with open('MANIFEST.in', 'w') as (fd):
    for l in commands:
        fd.write(l)
        fd.write('\n')

CLASSIFIERS = 'Development Status :: 4 - Beta\nIntended Audience :: Science/Research\nIntended Audience :: Developers\nLicense :: OSI Approved :: GNU Affero General Public License v3\nProgramming Language :: Python :: 2.7\nProgramming Language :: Python :: 3\nTopic :: Software Development\nTopic :: Software Development :: Build Tools\nTopic :: Scientific/Engineering\nOperating System :: Microsoft :: Windows\nOperating System :: POSIX\nOperating System :: Unix\nOperating System :: MacOS\n'
LONG_DESCRIPTION = [
 "It's a Protein Data Bank (.pdb) files manipulation package that is mainly developed to parse and load, duplicate, manipulate and create pdb files.",
 'A full description of a pdb file can be found here: http://deposit.rcsb.org/adit/docs/pdb_atom_format.html',
 "pdbparser atoms configuration can be visualized by vmd software (http://www.ks.uiuc.edu/Research/vmd/) by simply pointing 'VMD_PATH' global variable to the exact path of vmd executable, and using 'visualize' method.",
 'At any time and stage of data manipulation, a pdb file of all atoms or a subset of atoms can be exported to a pdb file.']
DESCRIPTION = [LONG_DESCRIPTION[0]]
from pdbparser import __version__
DATA_EXCLUDE = ('*.py', '*.pyc', '*~', '.*', '*.so', '*.pyd')
EXCLUDE_DIRECTORIES = ('*svn', '*git', 'dist', 'EGG-INFO', '*.egg-info')

def is_package(path):
    return os.path.isdir(path) and os.path.isfile(os.path.join(path, '__init__.py'))


def get_packages(path, base='', exclude=None):
    if exclude is None:
        exclude = []
    assert isinstance(exclude, (list, set, tuple)), 'exclude must be a list'
    exclude = [os.path.abspath(e) for e in exclude]
    packages = {}
    for item in os.listdir(path):
        d = os.path.join(path, item)
        if sum([e in os.path.abspath(d) for e in exclude]):
            continue
        if is_package(d):
            if base:
                module_name = '%(base)s.%(item)s' % vars()
            else:
                module_name = item
            packages[module_name] = d
            packages.update(get_packages(d, module_name, exclude))

    return packages


def find_package_data(where='.', package='', exclude=DATA_EXCLUDE, exclude_directories=EXCLUDE_DIRECTORIES, only_in_packages=True, show_ignored=False):
    out = {}
    stack = [(convert_path(where), '', package, only_in_packages)]
    while stack:
        where, prefix, package, only_in_packages = stack.pop(0)
        for name in os.listdir(where):
            fn = os.path.join(where, name)
            if os.path.isdir(fn):
                bad_name = False
                for pattern in exclude_directories:
                    if not fnmatch.fnmatchcase(name, pattern):
                        if fn.lower() == pattern.lower():
                            bad_name = True
                            if show_ignored:
                                (
                                 print >> sys.stderr, 'Directory %s ignored by pattern %s' % (fn, pattern))
                        break

                if bad_name:
                    continue
                if os.path.isfile(os.path.join(fn, '__init__.py')):
                    if not prefix:
                        if not package:
                            new_package = name
                        else:
                            new_package = package + '.' + name
                        stack.append((fn, '', new_package, False))
                    else:
                        stack.append((fn, prefix + name + '/', package, only_in_packages))
                else:
                    if not package:
                        bad_name = only_in_packages or False
                        for pattern in exclude:
                            if not fnmatch.fnmatchcase(name, pattern):
                                if fn.lower() == pattern.lower():
                                    bad_name = True
                                    if show_ignored:
                                        (
                                         print >> sys.stderr, 'File %s ignored by pattern %s' % (fn, pattern))
                                break

                        if bad_name:
                            continue
                    out.setdefault(package, []).append(prefix + name)

    return out


def find_data(where='.', exclude=DATA_EXCLUDE, exclude_directories=EXCLUDE_DIRECTORIES, prefix=''):
    out = {}
    stack = [convert_path(where)]
    while stack:
        where = stack.pop(0)
        for name in os.listdir(where):
            fn = os.path.join(where, name)
            d = os.path.join(prefix, os.path.dirname(fn))
            if os.path.isdir(fn):
                stack.append(fn)
            else:
                bad_name = False
                for pattern in exclude:
                    if fnmatch.fnmatchcase(name, pattern) or fn.lower() == pattern.lower():
                        bad_name = True
                        break

                if bad_name:
                    continue
                out.setdefault(d, []).append(fn)

    out = [(k, v) for k, v in out.items()]
    return out


PACKAGES = get_packages(path=PACKAGE_PATH, exclude=(os.path.join(PACKAGE_NAME, 'AMD'),
 os.path.join(PACKAGE_NAME, 'docs')))
for package in list(PACKAGES):
    if PACKAGE_NAME not in package:
        PACKAGES.pop(package)

metadata = dict(name=PACKAGE_NAME, packages=(PACKAGES.keys()),
  package_dir=PACKAGES,
  version=__version__,
  author='Bachir AOUN',
  author_email='bachir.aoun@e-aoun.com',
  description=('\n'.join(DESCRIPTION)),
  long_description=('\n'.join(LONG_DESCRIPTION)),
  license='GNU',
  classifiers=[_f for _f in CLASSIFIERS.split('\n') if _f],
  platforms=[
 'Windows', 'Linux', 'Solaris', 'Mac OS-X', 'Unix'],
  install_requires=[
 'pysimplelog', 'pypref'],
  setup_requires=[
 ''])
setup(**metadata)