# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/enlp/__init__.py
# Compiled at: 2019-11-27 15:57:30
# Size of source mod 2**32: 269 bytes
from . import pipeline, language_models
from . import processing, understanding, visualisation
try:
    from .version import version as __version__
except ImportError:
    from datetime import datetime
    __version__ = 'unknown-' + datetime.today().strftime('%Y%m%d')