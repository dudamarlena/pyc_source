# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/buzz/__init__.py
# Compiled at: 2019-09-06 08:48:34
# Size of source mod 2**32: 684 bytes
import warnings
from .corpus import Corpus
try:
    from .dashview import DashSite
except ImportError:
    pass

from .dataset import Dataset
from .file import File
from .parse import Parser
warnings.filterwarnings('ignore', message='numpy.dtype size changed')
warnings.filterwarnings('ignore', message='numpy.ufunc size changed')
warnings.filterwarnings('ignore', message='registration of accessor')
warnings.filterwarnings('ignore', message="Attribibute 'is_copy")
warnings.filterwarnings('ignore')
__version__ = '3.1.0'