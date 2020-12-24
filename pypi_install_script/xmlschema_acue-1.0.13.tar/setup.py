# -*- coding: utf-8 -*-
"""Distribute 'xmlschema_acue', a patched version of 'xmlschema' for the processing of XML data structures.

Additional Options:
   --no-install-requires: 
       Suppresses installation dependency checks,
       requires appropriate PYTHONPATH.

   --offline: 
       Sets online dependencies to offline, or ignores online
       dependencies.

"""
from __future__ import absolute_import
from __future__ import print_function

import os
import sys

from setuptools import setup


__author__ = 'Arno-Can Uestuensoez'
__author_email__ = 'acue_sf2@sourceforge.net'
__license__ = "Artistic-License-2.0 + Forced-Fairplay-Constraints"
__copyright__ = "Copyright (C) 2015-2019 Arno-Can Uestuensoez @Ingenieurbuero Arno-Can Uestuensoez"
__uuid__ = "5e5e8a98-c0ae-47a9-8429-bf7e352f0763"

__vers__ = [1, 0, 13,]
__version__ = "%02d.%02d.%03d"%(__vers__[0],__vers__[1],__vers__[2],)
__release__ = "%d.%d.%d" % (__vers__[0], __vers__[1], __vers__[2],) + '-patch0'
__status__ = 'beta'

__sdk = False
"""Set by the option "--sdk". Controls the installation environment."""
if '--sdk' in sys.argv:
    _sdk = True
    sys.argv.remove('--sdk')

# required for various interfaces, thus just do it
_mypath = os.path.dirname(os.path.abspath(__file__))
"""Path of this file."""
sys.path.insert(0,os.path.abspath(_mypath))


_name='xmlschema_acue'
__pkgname__ = "xmlschema_acue"
_version = "%d.%d.%d"%(__vers__[0],__vers__[1],__vers__[2],)


_install_requires = [
    'filesysobjects >=0.1.35',
    'sourceinfo >=0.1.34',
    'platformids >=0.1.0',
    'pythonids >=0.1.0',
    'setuplib >= 0.1.0',
]


if sys.version_info[0] != 3:
    _install_requires.append('configparser')  # use the backport from Python3 - need __getitem__


if __sdk: # pragma: no cover
    _install_requires.extend(
        [
            'sphinx >= 1.4',
            'epydoc >= 3.0',
        ]
    )


# Intentional HACK: ignore (online) dependencies, mainly foreseen for developement
__no_install_requires = False
if '--no-install-requires' in sys.argv:
    __no_install_requires = True
    sys.argv.remove('--no-install-requires')

# Intentional HACK: offline only, mainly foreseen for developement
__offline = False
if '--offline' in sys.argv:
    __offline = True
    __no_install_requires = True
    sys.argv.remove('--offline')


if __no_install_requires:
    print("#")
    print("# Changed to offline mode, ignore install dependencies completely.")
    print("# Requires appropriate PYTHONPATH.")
    print("# Ignored dependencies are:")
    print("#")
    for ir in _install_requires:
        print("#   "+str(ir))
    print("#")
    _install_requires=[]


setup(
    author=__author__,
    author_email=__author_email__,
    description="Provide patche for the package XML Schema. ",
    download_url="https://sourceforge.net/projects/xmlschema_acue/files/",
    install_requires=_install_requires,
    license=__license__,
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    name=_name,
    packages=['xmlschema_acue', ],
    url='https://sourceforge.net/projects/xmlschema_acue/',
    version=_version,
    zip_safe=False,
)


