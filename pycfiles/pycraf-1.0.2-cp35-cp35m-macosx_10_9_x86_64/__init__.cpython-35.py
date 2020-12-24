# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/runner/runners/2.166.2/work/1/s/build/lib.macosx-10.9-x86_64-3.5/pycraf/__init__.py
# Compiled at: 2020-04-16 04:29:51
# Size of source mod 2**32: 2080 bytes
"""
Top-level functionality:
"""
from ._astropy_init import *
import sys
__minimum_python_version__ = '3.5'

class UnsupportedPythonError(Exception):
    pass


if sys.version_info < tuple(int(val) for val in __minimum_python_version__.split('.')):
    raise UnsupportedPythonError('pycraf does not support Python < {}'.format(__minimum_python_version__))
if not _ASTROPY_SETUP_:
    import astropy
    if astropy.__version__ >= '4':
        try:
            astropy.physical_constants.set('astropyconst20')
            astropy.astronomical_constants.set('astropyconst20')
        except RuntimeError as e:
            if 'astropy.units is already imported' in e.args:
                e.args = ('Please note that pycraf uses the astropy.constants from Astropy v2 for backwards compatibility. Starting from Astropy v4, a "ScienceState" is used to allow versioning of physical constants. For technical reasons, it is necessary to import the astropy.units sub-package *after* pycraf.(see https://github.com/bwinkel/pycraf/issues/24)', )
                raise e

        from . import antenna
        from . import atm
        from . import conversions
        from . import geometry
        from . import geospatial
        from . import mc
        from . import pathprof
        from . import protection
        from . import satellite
        from . import utils