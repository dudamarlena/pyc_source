
__author__ = 'Arno-Can Uestuensoez'
__author_email__ = 'acue_sf2@sourceforge.net'
__license__ = "Artistic-License-2.0 + Forced-Fairplay-Constraints"
__copyright__ = "Copyright (C) 2015-2016 Arno-Can Uestuensoez @Ingenieurbuero Arno-Can Uestuensoez"
__version__ = '0.1.1'
__uuid__='e2b97b67-4649-49a3-9944-9fe69dc33b66'

_NAME = 'pystackinfo'

# some debug
if __debug__:
    __DEVELTEST__ = True

#
#***
#
import os,sys
from setuptools import setup #, find_packages
import fnmatch
import re, shutil, tempfile

version = '{0}.{1}'.format(*sys.version_info[:2])
version = '{0}.{1}'.format(*sys.version_info[:2])
if not version in ('2.6','2.7',):  # pragma: no cover
    raise Exception("Requires Python-2.6(.6+) or 2.7")




_name='iobricks'
_description=("The '" + _name + "' package provides utilities for simplified analysis YAML.")
_platforms='any'
_classifiers = [
    "Development Status :: 1 - Planning",
    "Intended Audience :: Developers",
    "License :: Free To Use But Restricted",
    "License :: OSI Approved :: Artistic License",
    "Natural Language :: English",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: OS Independent",
    "Operating System :: POSIX :: BSD :: OpenBSD",
    "Operating System :: POSIX :: Linux",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: POSIX :: SunOS/Solaris",
    "Operating System :: POSIX",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Unix Shell",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Utilities"
]

_keywords  = ' Python Syntax Packages Modules Files Linenumbers Filenames Modulenames Packagenames'
_keywords += ' RTTI PYTHONPATH inspect import imp dis qualname __qualname__'

_packages = [_name]
_scripts = []

#_download_url="https://github.com/ArnoCan/pystackinfo/"
_download_url="https://sourceforge.net/projects/pystackinfo/files/"
_url='https://sourceforge.net/projects/pystackinfo/'

#
#*** do it now...
#
setup(name=_name,
      version=__version__,
      author=__author__,
      author_email=__author_email__,
      classifiers=_classifiers,
      description=_description,
      download_url=_download_url,
      # install_requires=_install_requires,
      keywords=_keywords,
      license=__license__,
      # long_description=_long_description,
      platforms=_platforms,
      url=_url,
      # scripts=_scripts,
      packages=_packages,
      # package_data=_package_data,
)

