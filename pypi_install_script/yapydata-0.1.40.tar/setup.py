# -*- coding: utf-8 -*-
"""Distribute 'yapydata', a low-level data syntax processing for Python.

Additional local options for this *setup.py* module:
   --no-install-requires: 
       Suppresses installation dependency checks,
       requires appropriate PYTHONPATH.

   --offline: 
       Sets online dependencies to offline, or ignores online
       dependencies.

"""
from __future__ import absolute_import
from __future__ import print_function

#
# setup extension modules -  pip install setuplib / pip install pysetuplib 
#
import os
import sys

import setuptools

if sys.version_info[:2] == (2, 7,):
    ModuleLoadError = ImportError
else:
    ModuleLoadError = ModuleNotFoundError  # @UndefinedVariable

__author__ = 'Arno-Can Uestuensoez'
__author_email__ = 'acue_sf2@sourceforge.net'
__license__ = "Artistic-License-2.0 + Forced-Fairplay-Constraints"
__copyright__ = "Copyright (C) 2015-2019 Arno-Can Uestuensoez @Ingenieurbuero Arno-Can Uestuensoez"
__uuid__ = "60cac28d-efe6-4a8d-802f-fa4fc94fa741"

__vers__ = [0, 1, 40,]
__version__ = "%02d.%02d.%03d"%(__vers__[0],__vers__[1],__vers__[2],)
__release__ = "%d.%d.%d" % (__vers__[0], __vers__[1], __vers__[2],) + '-rc0'
__status__ = 'beta'


# required for various interfaces, thus just do it
_mypath = os.path.dirname(os.path.abspath(__file__))
"""Path of this file."""
sys.path.insert(0, os.path.abspath(_mypath))


_name='yapydata'
"""package name"""

__pkgname__ = "yapydata"
"""package name"""


_README = os.path.join(os.path.dirname(__file__), 'README.md')
_long_description = open(_README).read()
"""detailed description of this package"""

__no_install_requires = False
if '--no-install-requires' in sys.argv:
    __no_install_requires = True
    sys.argv.remove('--no-install-requires')

__offline = False
if '--offline' in sys.argv:
    __offline = True
    __no_install_requires = True
    sys.argv.remove('--offline')


_install_requires = ["yapyutils"],
if __no_install_requires:
    print("#")
    print("# Changed to offline mode, ignore install dependencies completely.")
    print("# Requires appropriate PYTHONPATH.")
    print("# Ignored dependencies are:")
    print("#")
    for ir in _install_requires:
        print("#   " + str(ir))
    print("#")
    _install_requires = []


#
# see setup.py for remaining parameters
#
setuptools.setup(
    author=__author__,
    author_email=__author_email__,
    description="The 'yapydata provides miscellaneous low-level *Python* data access APIs.",
    download_url="https://sourceforge.net/projects/yapydata/files/",
    install_requires=_install_requires,
    license=__license__,
    long_description=_long_description,
    name=_name,
    packages=['yapydata', 'yapydata/datatree', ],
    url='https://sourceforge.net/projects/yapydata/',
    version="%d.%d.%d"%(__vers__[0],__vers__[1],__vers__[2],),
    zip_safe=False,
)

sys.exit(0)
