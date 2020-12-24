# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/travis/build/tgsmith61591/pyramid/pyramid/__init__.py
# Compiled at: 2018-11-02 11:39:14
import os as _os
__version__ = '0.9.0'
try:
    __PYRAMID_SETUP__
except NameError:
    __PYRAMID_SETUP__ = False

if __PYRAMID_SETUP__:
    import sys
    sys.stderr.write('Partial import of pyramid during the build process.' + _os.linesep)
else:
    from . import __check_build
    from .arima import auto_arima, ARIMA
    from .utils import acf, autocorr_plot, c, pacf, plot_acf, plot_pacf
    from . import arima
    from . import datasets
    from . import utils
    __all__ = [
     'arima',
     'compat',
     'datasets',
     'utils',
     'ARIMA',
     'acf',
     'autocorr_plot',
     'auto_arima',
     'c',
     'pacf',
     'plot_acf',
     'plot_pacf']
    import warnings
    warnings.warn("\n    The 'pyramid' package will be migrating to a new namespace beginning in \n    version 1.0.0: 'pmdarima'. This is due to a package name collision with the\n    Pyramid web framework. For more information, see Issue #34:\n    \n        https://github.com/tgsmith61591/pyramid/issues/34\n        \n    The package will subsequently be installable via the name 'pmdarima'; the\n    only functional change to the user will be the import name. All imports\n    from 'pyramid' will change to 'pmdarima'.\n    ", UserWarning)
    from ._config import _warn_for_cache_size
    _warn_for_cache_size()
    del _os
    del warnings
    del _warn_for_cache_size
    del __check_build
    del __PYRAMID_SETUP__

def setup_module(module):
    import numpy as np, random
    _random_seed = int(np.random.uniform() * 2147483647)
    np.random.seed(_random_seed)
    random.seed(_random_seed)