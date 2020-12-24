# -*- coding: utf-8 -*-
"""The *rdbg* package supports for multi platform remodte debugging.

Installs 'rdbg', adds/modifies the following helper features to standard
'setuptools' options.

Additional Args:
    build_docx: 
        Creates Sphinx based documentation with embeded javadoc-style
        API documentation by epydoc. Supported doc types are:
           
            # primary formats:
            html, singlehtml, pdf, epub, man,
            
            # secondary formats:
            dirhtml, 
            latex, latexpdf, latexpdfja, 
            devhelp, htmlhelp, qthelp,

   dist_docx: 
       Creates distribution packages for offline documents. Supported
       archive types are:
       
           bzip2, lzma, tar, targz, tgz, zip,
           gzip
           

   install_docx: 
       Install a local copy of the previously build documents in
       accordance to PEP-370. Calls 'create_sphinx.sh' and 'epydoc'.

    build_apiref: 
        Creates Epydoc based documentation of javadoc-style.
        Supported doc types are:
           
            # primary formats:
            html, pdf,
            
            # secondary formats:
            pdflatex, latexpdf, auto,
            latex, tex, dvi, ps  

   testx: 
       Runs PyUnit tests by discovery of 'tests'.

Additional Options:
   --sdk:
       Requires sphinx, epydoc, and dot-graphics.

   --no-install-requires: 
       Suppresses installation dependency checks,
       requires appropriate PYTHONPATH.

   --offline: 
       Sets online dependencies to offline, or ignores online
       dependencies.

   --help-rdbg: 
       Displays this help.

"""
from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import re

import setuptools


try:
    #
    # optional remote debug only
    #
    from rdbg import start        # load a slim bootstrap module
    start.start_remote_debug()    # check whether '--rdbg' option is present, if so accomplish bootstrap
except:
    pass

#
# setup extension modules
#
import setupdocx

# documents
from setupdocx.build_docx import BuildDocX
from setupdocx.dist_docx import DistDocX
from setupdocx.install_docx import InstallDocX
from setupdocx.build_apiref import BuildApirefX

# unittests
from setuptestx.testx import TestX


__author__ = 'Arno-Can Uestuensoez'
__author_email__ = 'acue_sf2@sourceforge.net'
__license__ = "Artistic-License-2.0 + Forced-Fairplay-Constraints"
__copyright__ = "Copyright (C) 2015-2019 Arno-Can Uestuensoez @Ingenieurbuero Arno-Can Uestuensoez"
__uuid__ = '7f464182-b723-4e6e-869d-80a16b9cfaca'

__vers__ = [0, 2, 22,]
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

_name = 'rdbg'
"""package name"""

__pkgname__ = "rdbg"
"""package name"""

_version = "%d.%d.%d" % (__vers__[0], __vers__[1], __vers__[2],)
"""assembled version string"""

_author = __author__
"""author of the package"""

_author_email = __author_email__
"""author's email """

_license = __license__
"""license"""

_packages = setuptools.find_packages(include=['rdbg', ])
"""Python packages to be installed."""

_packages_sdk = setuptools.find_packages(include=['rdbg'])
"""Python packages to be installed."""

_scripts = [
    "bin/rdbgcli.py",
    "bin/rdbgcli",
]
"""Scripts to be installed."""

_package_data = {
    'rdbg': [
        'README.md', 'ArtisticLicense20.html', 'licenses-amendments.txt',
    ],
}
"""Provided data of the package."""

_url = 'https://sourceforge.net/projects/rdbg/'
"""URL of this package"""

# _download_url="https://github.com/ArnoCan/rdbg/"
_download_url = "https://sourceforge.net/projects/rdbg/files/"


_install_requires = [
    'jsondata >=0.2.24',
    'multiconf >=0.2.21',
    'filesysobjects >=0.1.36',
    'sourceinfo >=0.1.34',
    'pyrdbg >=0.1.0',
    'pythonids >=0.1.0',
    'setuplib >= 0.1.0',
    'namedtupledefs >= 0.1.0',
]
"""prerequired non-standard packages"""


_description = (
    "The 'pyrdbg' package provides remote debugging."
)

_README = os.path.join(os.path.dirname(__file__), 'README.md')
_long_description = open(_README).read() + 'nn'
"""detailed description of this package"""

_classifiers = [
    "Framework :: Setuptools Plugin",
    "Development Status :: 3 - Alpha",
    "Environment :: Console",
    "Environment :: MacOS X",
    "Environment :: Other Environment",
    "Environment :: Win32 (MS Windows)",
    "Environment :: X11 Applications",
    "Framework :: IPython",
    "Intended Audience :: Developers",
    "Intended Audience :: System Administrators",
    "License :: Free To Use But Restricted",
    "License :: OSI Approved :: Artistic License",
    "Natural Language :: English",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: Other OS",
    "Operating System :: POSIX :: BSD :: FreeBSD",
    "Operating System :: POSIX :: BSD :: OpenBSD",
    "Operating System :: POSIX :: Linux",
    "Operating System :: POSIX :: Other",
    "Operating System :: POSIX :: SunOS/Solaris",
    "Operating System :: POSIX",
    "Operating System :: Unix",
    "Programming Language :: C",
    "Programming Language :: C++",
    "Programming Language :: Cython",
    "Programming Language :: Java",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: IronPython",
    "Programming Language :: Python :: Implementation :: Jython",
    "Programming Language :: Python :: Implementation :: PyPy",
    "Programming Language :: Python",
    "Programming Language :: Unix Shell",
    "Topic :: Home Automation",
    "Topic :: Internet",
    "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator",
    "Topic :: Scientific/Engineering",
    "Topic :: Security",
    "Topic :: Software Development :: Build Tools",
    "Topic :: Software Development :: Code Generators",
    "Topic :: Software Development :: Compilers",
    "Topic :: Software Development :: Debuggers",
    "Topic :: Software Development :: Embedded Systems",
    "Topic :: Software Development :: Interpreters",
    "Topic :: Software Development :: Libraries :: Application Frameworks",
    "Topic :: Software Development :: Libraries :: Java Libraries",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Software Development :: Libraries :: pygame",
    "Topic :: Software Development :: Libraries",
    "Topic :: Software Development :: Pre-processors",
    "Topic :: Software Development :: Testing",
    "Topic :: Software Development",
    "Topic :: System :: Distributed Computing",
    "Topic :: System :: Installation/Setup",
    "Topic :: System :: Logging",
    "Topic :: System :: Monitoring",
    "Topic :: System :: Networking",
    "Topic :: System :: Operating System",
    "Topic :: System :: Shells",
    "Topic :: System :: Software Distribution",
    "Topic :: System :: System Shells",
    "Topic :: System :: Systems Administration",
    "Topic :: Utilities",
]
"""the classification of this package"""

_epydoc_api_patchlist = [
    'shortcuts.html',
]
"""Patch list of Sphinx documents for the insertion of links to API documentation."""

_profiling_components = _mypath + os.sep + 'bin' + os.sep + '*.py ' + _mypath + os.sep + __pkgname__ + os.sep + '*.py'
"""Components to be used for the creation of profiling information for Epydoc."""

_doc_subpath = 'en' + os.path.sep + 'html' + os.path.sep + 'man7'
"""Relative path under the documents directory."""

if __sdk:  # pragma: no cover
    try:
        import sphinx_rtd_theme  # @UnusedImport
    except:
        sys.stderr.write("WARNING: Cannot import package 'sphinx_rtd_theme', cannot create local 'ReadTheDocs' style.")

    _install_requires.extend(
        [
            'pythonids',
            'sphinx >= 1.4',
            'epydoc >= 3.0',
        ]
    )

    _packages = _packages_sdk

_test_suite = "tests.CallCase"

__no_install_requires = False
if '--no-install-requires' in sys.argv:
    __no_install_requires = True
    sys.argv.remove('--no-install-requires')

__offline = False
if '--offline' in sys.argv:
    __offline = True
    __no_install_requires = True
    sys.argv.remove('--offline')

# Help on addons.
if '--help-rdbg' in sys.argv:
    setupdocx.usage('setup')
    sys.exit(0)

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


class build_docx(BuildDocX):
    """Defines additional text processing.
    """
    
    def __init__(self, *args, **kargs):
        self.name = 'rdbg'
        self.copyright = __copyright__
        self.status = __status__
        self.release = __release__
        BuildDocX.__init__(self, *args, **kargs)

    def join_sphinx_mod_sphinx(self, dirpath):
        """Integrates links for *epydoc* into the the sidebar of the default style,
        and adds links to *sphinx* into the output of *epydoc*. This method needs to 
        be adapted to the actual used theme and templates by the application. Thus
        no generic method is supported, but a call interface. The call is activated
        when the option *--apiref* is set.  

        Adds the following entries before the "Table of Contents" to 
        the *sphinx* document:
        
        * API
          Before "Previous topic", "Next topic"

        .. note::
        
           This method is subject to be changed.
           Current version is hardcoded, see documents.
           Following releases will add customization.
        
        Args:
            **dirpath**:
                Directory path to the file 'index.html'.
        
        Returns;
            None

        Raises:
            None
                
        """
    
        pt = """<a target="moduleFrame" href="toc-everything.html">Everything</a>"""
        rp  = r"""<a href="../index.html" target="_top">Home</a>"""
        rp += r' - '
        rp += r"""<a href="./index.html" target="_top">Top</a>"""
        rp += r' - '
        rp += pt
        fn = dirpath + os.sep + 'epydoc' + os.sep + 'toc.html'
        sed(fn, pt, rp, re.MULTILINE)  # @UndefinedVariable
        
        pt = """<h4>Next topic</h4>"""
        rp  = r"""<h4>API</h4><p class="topless"><a href="epydoc/index.html" title="API">Programming Interface</a></p>"""
        rp += pt
        fn = dirpath + os.sep + 'index.html'
        sed(fn, pt, rp, re.MULTILINE)  # @UndefinedVariable
        
        pt = r'<li><a class="reference internal" href="#table-of-contents">Table of Contents</a></li>'
        rp = r'<li><a class="reference internal" href="shortcuts.html">Shortcuts</a></li>'
        rp += r'<li><a class="reference internal" href="howto.html">Howto</a></li>'
        rp += r'<li><a class="reference internal" href="install.html">Install</a></li>'
        rp += pt
        fn = dirpath + os.sep + 'index.html'
        sed(fn, pt, rp, re.MULTILINE)  # @UndefinedVariable
        
        patchlist = [
            'rdbg.html',
            'rdbg_cli_options.html',
            'checkrdbg.html',
            'pydevrdc.html',
            'shortcuts.html',
            'software_design.html',
        ]
        pt = """<h4>Previous topic</h4>"""
        rp  = r"""<h4>API</h4><p class="topless"><a href="epydoc/index.html" title="API">Programming Interface</a></p>"""
        rp += pt
        for px in patchlist:
            fn = dirpath + os.sep + px
            sed(fn, pt, rp, re.MULTILINE)  # @UndefinedVariable
        
        pt1 = """<h4>Next topic</h4>"""
        rp1  = r"""<h4>API</h4><p class="topless"><a href="epydoc/index.html" title="API">Programming Interface</a></p>"""
        rp1 += pt1
        for px in patchlist:
            fn = dirpath + os.sep + px
            sed(fn, pt1, rp1, re.MULTILINE)  # @UndefinedVariable
        
        pt2 = r"""<div role="note" aria-label="source link">"""
        rp2  = r"""<h4>API</h4><p class="topless"><a href="epydoc/index.html" title="API">Programming Interface</a></p>"""
        rp2 += pt2
        for px in patchlist:
            fn = dirpath + os.sep + px
            sed(fn, pt2, rp2, re.MULTILINE)  # @UndefinedVariable


class install_docx(InstallDocX):
    """Defines the package name.
    """

    def __init__(self, *args, **kargs):
        self.name = 'rdbg'
        self.copyright = __copyright__
        self.status = __status__
        self.release = __release__
        InstallDocX.__init__(self, *args, **kargs)


class dist_docx(DistDocX):
    """Defines the package name.
    """

    def __init__(self, *args, **kargs):
        self.name = 'rdbg'
        self.copyright = __copyright__
        self.status = __status__
        self.release = __release__
        DistDocX.__init__(self, *args, **kargs)


class build_apiref(BuildApirefX):
    """Defines the package name.
    """

    def __init__(self, *args, **kargs):
        self.name = 'rdbg'
        self.copyright = __copyright__
        self.status = __status__
        self.release = __release__
        BuildApirefX.__init__(self, *args, **kargs)


class testx(TestX):
    """Defines the package name.
    """

    def __init__(self, *args, **kargs):
        self.name = 'setuplib'
        self.copyright = __copyright__
        self.status = __status__
        self.release = __release__
        TestX.__init__(self, *args, **kargs)


#
# see setup.py for remaining parameters
#
setuptools.setup(
    author=_author,
    author_email=_author_email,
    classifiers=_classifiers,
    cmdclass={
        'build_apiref': build_apiref,
        'build_docx': build_docx,
        'install_docx': install_docx,
        'dist_docx': dist_docx,
        'testx': testx,
    },
    description=_description,
    download_url=_download_url,
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

if '--help' in sys.argv:
    print()
    print("Help on usage extensions by " + str(_name))
    print("   --help-" + str(_name))
    print()

sys.exit(0)

