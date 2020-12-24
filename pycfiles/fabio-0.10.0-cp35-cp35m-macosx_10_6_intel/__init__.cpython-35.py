# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/__init__.py
# Compiled at: 2020-04-03 09:02:03
# Size of source mod 2**32: 3827 bytes
"""FabIO module"""
from __future__ import absolute_import, print_function, division
__author__ = 'Jérôme Kieffer'
__contact__ = 'Jerome.Kieffer@ESRF.eu'
__license__ = 'GPLv3+'
__copyright__ = 'European Synchrotron Radiation Facility, Grenoble, France'
__date__ = '19/08/2019'
__status__ = 'stable'
import sys, logging
if 'ps1' in dir(sys):
    logging.basicConfig()
import os
project = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
try:
    from ._version import __date__ as date
    from ._version import version, version_info, hexversion, strictversion
except ImportError:
    raise RuntimeError('Do NOT use %s from its sources: build it and use the built version' % project)

from . import fabioformats as _fabioformats
factory = _fabioformats.factory
_fabioformats.register_default_formats()
from . import fabioimage
from . import openimage
from .fabioutils import COMPRESSORS, jump_filename, FilenameObject, previous_filename, next_filename, deconstruct_filename, extract_filenumber, getnum, construct_filename, exists
filename_object = FilenameObject
from .openimage import openimage as open
from .openimage import open_series
from .openimage import openheader

def register(codec_class):
    """
    Register a codec class with the set of formats supported by fabio.

    It is a transitional function to prepare the next comming version of fabio.

    - On the current fabio library, when a module is imported, all the formats
        inheriting FabioImage are automatically registred. And this function is
        doing nothing.
    - On the next fabio library. Importing a module containing classes
        inheriting FabioImage will not be registered. And this function will
        register the class.

    The following source code will then provide the same behaviour on both
    fabio versions, and it is recommended to use it.

    .. code-block:: python

        @fabio.register
        class MyCodec(fabio.fabioimage.FabioImage):
            pass
    """
    assert issubclass(codec_class, fabioimage.FabioImage)
    _fabioformats.register(codec_class)
    return codec_class


def tests():
    """
    Run the FabIO test suite.

    If the test-images are not already installed (via the debian package for example),
    they need to be downloaded from sourceforge.net, which make take a while.
    Ensure your network connection is operational and your proxy settings are correct,
    for example:

    export http_proxy=http://proxy.site.com:3128
    """
    from . import test
    test.run_tests()


def benchmarks():
    """
    Run the benchmarks
    """
    from . import benchmark
    res = benchmark.run()
    return res