# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rgeda/project/repo/webbpsf/astropy_helpers/astropy_helpers/__init__.py
# Compiled at: 2019-07-20 17:47:20
# Size of source mod 2**32: 1738 bytes
try:
    from .version import version as __version__
    from .version import githash as __githash__
except ImportError:
    __version__ = ''
    __githash__ = ''

import sys
if 'ah_bootstrap' in sys.modules:
    del sys.modules['ah_bootstrap']
else:
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot
    except:
        pass

    import os
    if '__main__' in sys.modules and hasattr(sys.modules['__main__'], '__file__'):
        filename = os.path.basename(sys.modules['__main__'].__file__)
        if filename.rstrip('co') == 'setup.py':
            import builtins
            builtins._ASTROPY_SETUP_ = True
        del filename