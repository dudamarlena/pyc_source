# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nearl/projects/specutils/build/lib/specutils/__init__.py
# Compiled at: 2020-03-17 18:47:05
# Size of source mod 2**32: 1561 bytes
"""
Specutils: an astropy package for spectroscopy.
"""
from ._astropy_init import *
from astropy import config as _config
import sys
__minimum_python_version__ = '3.5'

class UnsupportedPythonError(Exception):
    pass


if sys.version_info < tuple((int(val) for val in __minimum_python_version__.split('.'))):
    raise UnsupportedPythonError('packagename does not support Python < {}'.format(__minimum_python_version__))
if not _ASTROPY_SETUP_:
    from .spectra import *
    from .io.default_loaders import *
    from io.registers import _load_user_io
    _load_user_io()
__citation__ = 'https://doi.org/10.5281/zenodo.1421356'

class Conf(_config.ConfigNamespace):
    __doc__ = '\n    Configuration parameters for specutils.\n    '
    do_continuum_function_check = _config.ConfigItem(True, 'Whether to check the spectrum baseline value is closeto zero. If it is not within ``threshold`` then a warning is raised.')


conf = Conf()