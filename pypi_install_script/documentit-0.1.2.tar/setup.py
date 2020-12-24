# -*- coding: utf-8 -*-
"""Distribute 'documentit', the core library for extensions of *setuptools*.
Provides detailed information on Python packages and their entry points.

Additional local options for this *setup.py* module:
   --sdk:
       Requires sphinx, epydoc, and dot-graphics.

   --no-install-requires: 
       Suppresses installation dependency checks,
       requires appropriate PYTHONPATH.

   --offline: 
       Sets online dependencies to offline, or ignores online
       dependencies.

"""
from __future__ import absolute_import
from __future__ import print_function

try:
    # optional remote debug
    from rdbg import start        # load a slim bootstrap module
    start.start_remote_debug()    # check whether '--rdbg' option is present, if so accomplish bootstrap
except:
    pass


import os
import sys

import setuptools


__author__ = 'Arno-Can Uestuensoez'
__author_email__ = 'acue_sf2@sourceforge.net'
__license__ = "Artistic-License-2.0 + Forced-Fairplay-Constraints"
__copyright__ = "Copyright (C) 2015-2019 Arno-Can Uestuensoez @Ingenieurbuero Arno-Can Uestuensoez"
__uuid__ = "239b0bf7-674a-4f53-a646-119f591af806"

__vers__ = [0, 1, 2, ]
__version__ = "%02d.%02d.%03d" % (__vers__[0], __vers__[1], __vers__[2],)
__release__ = "%d.%d.%d" % (__vers__[0], __vers__[1], __vers__[2],) + '-rc0'
__status__ = 'beta'


__sdk = False
"""Set by the option "--sdk". Controls the installation environment."""
if '--sdk' in sys.argv:
    __sdk = True
    sys.argv.remove('--sdk')


# required for various interfaces, thus just do it
_mypath = os.path.dirname(os.path.abspath(__file__))
"""Path of this file."""
sys.path.insert(0, os.path.abspath(_mypath))

_name = 'documentit'
__pkgname__ = _name
_version = "%d.%d.%d" % (__vers__[0], __vers__[1], __vers__[2],)


#
# see setup.py for remaining parameters
#
setuptools.setup(
    author=__author__,
    author_email=__author_email__,
    description="Placeholder for package in preparation.",
    download_url="https://sourceforge.net/projects/documentit/files/",
    license=__license__,
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    name=_name,
    packages=['dummy',],
    scripts=[],
    url='https://sourceforge.net/projects/documentit/',
    version=_version,
    zip_safe=False,
)

sys.exit(0)

