# -*- coding: utf-8 -*-
"""Distribute 'setupjavax', multi-platform support for regression tests.

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
import re

import setuptools

import yapyutils.help
#
# setup extension modules
#

import setupjavax.build_java
import setupjavax.build_jy

#***
# the following parts are required as for the setupjavax itself
# others may use the entry points
#***

#***********************************************************************
# REMARK:
#   documents and regression tests
#
#   the classes are required here for setupjavax only
#   others should use the entry point, so do not need to import classes
#
#***********************************************************************
import setupdocx.build_docx
import setupdocx.dist_docx
import setupdocx.install_docx
import setupdocx.build_apiref
import setupdocx.build_apidoc

# unittests
import setuptestx.testx


__author__ = 'Arno-Can Uestuensoez'
__author_email__ = 'acue_sf2@sourceforge.net'
__license__ = "Artistic-License-2.0 + Forced-Fairplay-Constraints"
__copyright__ = "Copyright (C) 2015-2019 Arno-Can Uestuensoez @Ingenieurbuero Arno-Can Uestuensoez"
__uuid__ = "1ba7bffb-c00b-4691-a3e9-e392f968e437"

__vers__ = [0, 1, 37, ]
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


#--------------------------------------
#
# Package parameters for setuptools
#
#--------------------------------------

_name = 'setupjavax'
"""package name"""

__pkgname__ = "setupjavax"
"""package name"""

_version = "%d.%d.%d" % (__vers__[0], __vers__[1], __vers__[2],)
"""assembled version string"""

_author = __author__
"""author of the package"""

_author_email = __author_email__
"""author's email """

_license = __license__
"""license"""

#_packages = setuptools.find_packages('setupjavax')
_packages = ['setupjavax',]
"""Python packages to be installed."""

_packages_sdk = _packages

_scripts = [
]
"""Scripts to be installed."""

_package_data = {
    'setupjavax': [
        'README.md', 'ArtisticLicense20.html', 'licenses-amendments.txt',
    ],
}
"""Provided data of the package."""

_url = 'https://sourceforge.net/projects/setupjavax/'
"""URL of this package"""

# _download_url="https://github.com/ArnoCan/setupjavax/"
_download_url = "https://sourceforge.net/projects/setupjavax/files/"


_install_requires = [
    'pythonids >= 0.1.31',
    'yapyutils >= 0.1.0',
    'yapydata >= 0.1.0',
    'sourceinfo >= 0.1.0',
]
"""prerequired non-standard packages"""


_description = "Support Java extensions for setuptools / distutils."

_README = os.path.join(os.path.dirname(__file__), 'README.md')
_long_description = open(_README).read()
"""detailed description of this package"""


if __sdk:  # pragma: no cover
    try:
        import sphinx_rtd_theme  # @UnusedImport
    except:
        sys.stderr.write(
            "WARNING: Cannot import package 'sphinx_rtd_theme', cannot create local 'ReadTheDocs' style.")

    _install_requires.extend(
        [
            'sphinx >= 1.4',
            'epydoc >= 3.0',
        ]
    )

    _packages = _packages_sdk

_test_suite = "tests.CallCase"

# Help on addons.
if '--help-setupjavax' in sys.argv:
    yapyutils.help.usage('setup')
    sys.exit(0)

__no_install_requires = False
if '--no-install-requires' in sys.argv:
    __no_install_requires = True
    sys.argv.remove('--no-install-requires')

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
        print("#   " + str(ir))
    print("#")
    _install_requires = []


class build_java(setupjavax.build_java.BuildJava):
    """For pre-installation, and test and debug of setupjavax.
    Standard application sshould use the provided entry points. 
    """
    def __init__(self, *args, **kargs):
        setupjavax.build_java.BuildJava.__init__(self, *args, **kargs)


class build_jy(setupjavax.build_jy.BuildJy):
    """For pre-installation, and test and debug of setupjavax.
    Standard application sshould use the provided entry points. 
    """
    def __init__(self, *args, **kargs):
        setupjavax.build_jy.TestX.__init__(self, *args, **kargs)


class build_docx(setupdocx.build_docx.BuildDocX):
    """For pre-installation, and test and debug of setupdocx. 
    Standard application should use the provided entry points. 
    """
    def __init__(self, *args, **kargs):
        setupdocx.build_docx.BuildDocX.__init__(self, *args, **kargs)


class install_docx(setupdocx.install_docx.InstallDocX):
    """For pre-installation, and test and debug of setupdocx. 
    Standard application should use the provided entry points. 
    """
    def __init__(self, *args, **kargs):
        setupdocx.install_docx.InstallDocX.__init__(self, *args, **kargs)


class dist_docx(setupdocx.dist_docx.DistDocX):
    """For pre-installation, and test and debug of setupdocx. 
    Standard application should use the provided entry points. 
    """
    def __init__(self, *args, **kargs):
        setupdocx.dist_docx.DistDocX.__init__(self, *args, **kargs)


class build_apidoc(setupdocx.build_apidoc.BuildApidocX):
    """For pre-installation, and test and debug of setupdocx. 
    Standard application should use the provided entry points. 
    """
    def __init__(self, *args, **kargs):
        setupdocx.build_apidoc.BuildApidocX.__init__(self, *args, **kargs)


class build_apiref(setupdocx.build_apiref.BuildApirefX):
    """For pre-installation, and test and debug of setupdocx. 
    Standard application should use the provided entry points. 
    """
    def __init__(self, *args, **kargs):
        setupdocx.build_apiref.BuildApirefX.__init__(self, *args, **kargs)


class testx(setuptestx.testx.TestX):
    """For pre-installation, and test and debug of setuptestx. 
    Standard application should use the provided entry points. 
    """
    def __init__(self, *args, **kargs):
        setuptestx.testx.TestX.__init__(self, *args, **kargs)


#
# see setup.py for remaining parameters
#
setuptools.setup(
    author=_author,
    author_email=_author_email,
    cmdclass={
        'build_apidoc': build_apidoc,  # for bootstrap of setuplib - not required for applications
        'build_apiref': build_apiref,  # for bootstrap of setuplib - not required for applications
        'build_docx': build_docx,      # for bootstrap of setuplib - not required for applications
        'dist_docx': dist_docx,        # for bootstrap of setuplib - not required for applications
        'install_docx': install_docx,  # for bootstrap of setuplib - not required for applications
        'testx': testx,                # for bootstrap of setuplib - not required for applications
        'build_java': build_java,      # for bootstrap of setuplib - not required for applications
        'build_jy': build_jy,          # for bootstrap of setuplib - not required for applications
    },
    description=_description,
#    distclass=setupjavax.dist.Distribution,  # extends the standard help-display of setuptools
    download_url=_download_url,
    entry_points={                    # for standard application
        'distutils.commands': 'build_java = setupjavax.build_java:BuildJava',
        'distutils.commands': 'build_jy = setupjavax.build_jy:BuildJy',
    },
    install_requires=_install_requires,
    license=_license,
    long_description=_long_description,
    name=_name,
    package_data=_package_data,
    packages=_packages,
    scripts=_scripts,
    url=_url,
    version=_version,
    zip_safe=False,
)


if '--help' in sys.argv or '-h' in sys.argv:
    print()
    print("Help on usage extensions by " + str(_name))
    print("   --help-" + str(_name))
    print()

sys.exit(0)

